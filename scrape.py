#!/usr/bin/env python3
"""
WordPress to Static Site Scraper

Fetches all blog posts via paginated RSS feed and static pages via HTML scraping.
Converts content to Markdown, downloads assets.

Output layout:
  site/blog/<YYYY-MM-DD>-<slug>.md
  site/blog/assets/<YYYY-MM-DD>-<slug>/<image-files>
  site/<page-slug>.md

Usage:
    python scrape.py [--url URL] [--output OUTPUT] [--delay SECONDS]
"""

import argparse
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import markdownify as md_lib


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert arbitrary text to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    text = text.strip("-")
    return text or "untitled"


def make_session(user_agent: str = "WP-Scraper/1.0 (+https://github.com)") -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = user_agent
    return s


# ---------------------------------------------------------------------------
# RSS / Post fetching
# ---------------------------------------------------------------------------

RSS_NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "slash": "http://purl.org/rss/1.0/modules/slash/",
}


def fetch_rss_page(base_url: str, page: int, session: requests.Session) -> list[dict]:
    """Fetch one page of the RSS feed; returns [] when there are no more items."""
    url = f"{base_url}?feed=rss2&paged={page}"
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  RSS page {page} fetch error: {exc}", file=sys.stderr)
        return []

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as exc:
        print(f"  RSS page {page} parse error: {exc}", file=sys.stderr)
        return []

    channel = root.find("channel")
    if channel is None:
        return []

    items = []
    for item in channel.findall("item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        pub_date = item.findtext("pubDate", "").strip()
        categories = [c.text.strip() for c in item.findall("category") if c.text]
        content_html = (
            item.findtext("content:encoded", namespaces=RSS_NS) or ""
        ).strip()

        # Parse the date
        date_str = "unknown"
        for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S +0000"):
            try:
                dt = datetime.strptime(pub_date, fmt)
                date_str = dt.strftime("%Y-%m-%d")
                break
            except ValueError:
                pass

        items.append(
            {
                "title": title,
                "link": link,
                "date": date_str,
                "categories": categories,
                "content_html": content_html,
                "slug": slugify(title),
            }
        )

    return items


def fetch_all_posts(base_url: str, session: requests.Session, delay: float = 0.5) -> list[dict]:
    """Walk all RSS pages and return every post."""
    posts: list[dict] = []
    page = 1
    seen_links: set[str] = set()

    while True:
        print(f"  RSS page {page} …", end=" ", flush=True)
        items = fetch_rss_page(base_url, page, session)
        if not items:
            print("(empty — done)")
            break

        new_items = [i for i in items if i["link"] not in seen_links]
        if not new_items:
            print("(duplicate — done)")
            break

        for i in new_items:
            seen_links.add(i["link"])
        posts.extend(new_items)
        print(f"{len(new_items)} posts")

        page += 1
        time.sleep(delay)

    return posts


# ---------------------------------------------------------------------------
# Asset downloading
# ---------------------------------------------------------------------------

WP_EMOJI_HOST = "s.w.org"  # skip WordPress CDN emoji images


def is_skippable_asset(url: str) -> bool:
    return urlparse(url).netloc == WP_EMOJI_HOST


def download_asset(url: str, dest_dir: Path, session: requests.Session) -> str | None:
    """Download *url* into *dest_dir*.  Returns the local filename on success."""
    if is_skippable_asset(url):
        return None
    try:
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        if not filename or "." not in filename:
            return None

        dest_path = dest_dir / filename
        if dest_path.exists():
            return filename  # already fetched

        resp = session.get(url, timeout=30, stream=True)
        resp.raise_for_status()
        dest_path.write_bytes(resp.content)
        return filename
    except Exception as exc:
        print(f"    ⚠ asset download failed ({url}): {exc}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# HTML → Markdown conversion
# ---------------------------------------------------------------------------

class CustomMarkdownConverter(md_lib.MarkdownConverter):
    """Extend markdownify with nicer iframe / code block handling."""

    def convert_iframe(self, el, text, parent_tags):
        src = el.get("src", "")
        title = el.get("title", "Embedded video")
        if "youtube" in src:
            # Extract video id for a clean embed link
            m = re.search(r"embed/([A-Za-z0-9_-]+)", src)
            vid = m.group(1) if m else ""
            yt_url = f"https://www.youtube.com/watch?v={vid}" if vid else src
            return f"\n\n[{title}]({yt_url})\n\n"
        return f"\n\n[{title}]({src})\n\n" if src else ""

    def convert_pre(self, el, text, parent_tags):
        # Detect language hint from a child <code> class
        code_el = el.find("code")
        lang = ""
        if code_el:
            for cls in (code_el.get("class") or []):
                if cls.startswith("language-"):
                    lang = cls[len("language-"):]
                    break
        inner = (code_el.get_text() if code_el else el.get_text()).strip("\n")
        return f"\n\n```{lang}\n{inner}\n```\n\n"


def html_to_markdown(html: str, asset_dir: Path, asset_url_prefix: str,
                     session: requests.Session) -> str:
    """
    Parse *html*, download embedded images into *asset_dir*, rewrite their
    src to *asset_url_prefix*/<filename>, then return Markdown.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Download images; rewrite src
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src or is_skippable_asset(src):
            # Remove WordPress emoji <img> entirely — keep the alt text as emoji char
            alt = img.get("alt", "")
            img.replace_with(alt)
            continue
        local = download_asset(src, asset_dir, session)
        if local:
            img["src"] = f"{asset_url_prefix}/{local}"

    result = CustomMarkdownConverter(
        heading_style="ATX",
        strip=["script", "style"],
        newline_style="backslash",
    ).convert(str(soup))

    # Collapse excess blank lines
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


# ---------------------------------------------------------------------------
# Front-matter helpers
# ---------------------------------------------------------------------------

def _escape_yaml_string(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def build_post_frontmatter(post: dict) -> str:
    cats = "\n".join(f"  - {c}" for c in post["categories"]) if post["categories"] else "  []"
    return (
        "---\n"
        f'title: "{_escape_yaml_string(post["title"])}"\n'
        f'date: {post["date"]}\n'
        f'slug: {post["slug"]}\n'
        f"categories:\n{cats}\n"
        "---\n\n"
    )


def build_page_frontmatter(title: str, slug: str) -> str:
    return (
        "---\n"
        f'title: "{_escape_yaml_string(title)}"\n'
        f"slug: {slug}\n"
        "---\n\n"
    )


# ---------------------------------------------------------------------------
# Pages (non-blog static pages)
# ---------------------------------------------------------------------------

# Known WordPress pages: (slug, page_id)
WP_PAGES = [
    ("cv", "8"),
    ("imprint", "6"),
    ("privacy-policy", "214"),
]


def scrape_wp_page(base_url: str, page_id: str, session: requests.Session) -> dict | None:
    url = f"{base_url}?page_id={page_id}"
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  page {page_id} fetch error: {exc}", file=sys.stderr)
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Try common WP theme selectors for title + content
    title_el = (
        soup.find("h1", class_="entry-title")
        or soup.find("h1", class_=re.compile("page-title"))
        or soup.find("article", id=re.compile("page-")) and soup.find("h1")
        or soup.find("h1")
    )
    title = title_el.get_text(strip=True) if title_el else f"Page {page_id}"

    content_el = (
        soup.find("div", class_="entry-content")
        or soup.find("div", class_=re.compile("page-content"))
        or soup.find("article")
    )
    content_html = str(content_el) if content_el else ""

    return {"title": title, "content_html": content_html}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape a WordPress blog and convert to Markdown static site files."
    )
    parser.add_argument(
        "--url",
        default="https://chkr.at/wordpress/",
        help="WordPress base URL (default: https://chkr.at/wordpress/)",
    )
    parser.add_argument(
        "--output",
        default="site",
        help="Output root directory (default: site/)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Seconds to wait between requests (default: 0.5)",
    )
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    output_dir = Path(args.output)
    blog_dir = output_dir / "blog"
    blog_dir.mkdir(parents=True, exist_ok=True)

    session = make_session()

    # ------------------------------------------------------------------ posts
    print(f"\n=== Fetching blog posts from {base_url} ===")
    posts = fetch_all_posts(base_url, session, delay=args.delay)
    print(f"Total posts: {len(posts)}\n")

    # Deduplicate slugs (two posts could produce the same slug)
    slug_counts: dict[str, int] = {}
    for post in posts:
        slug_counts[post["slug"]] = slug_counts.get(post["slug"], 0) + 1

    slug_used: dict[str, int] = {}
    for post in posts:
        s = post["slug"]
        if slug_counts[s] > 1:
            slug_used[s] = slug_used.get(s, 0) + 1
            post["slug"] = f"{s}-{slug_used[s]}"

    written_posts = 0
    for post in posts:
        filename = f"{post['date']}-{post['slug']}.md"
        asset_dir_name = f"{post['date']}-{post['slug']}"
        asset_dir = blog_dir / "assets" / asset_dir_name
        asset_dir.mkdir(parents=True, exist_ok=True)
        asset_url_prefix = f"assets/{asset_dir_name}"

        print(f"  → {filename}")
        try:
            content_md = html_to_markdown(
                post["content_html"], asset_dir, asset_url_prefix, session
            )
        except Exception as exc:
            print(f"    ⚠ conversion error: {exc}", file=sys.stderr)
            content_md = post["content_html"]  # fallback: raw HTML

        md_file = blog_dir / filename
        md_file.write_text(
            build_post_frontmatter(post) + content_md, encoding="utf-8"
        )
        written_posts += 1
        time.sleep(args.delay)

    # ------------------------------------------------------------------ pages
    print(f"\n=== Fetching static pages ===")
    written_pages = 0
    for slug, page_id in WP_PAGES:
        print(f"  → {slug}.md (page_id={page_id})")
        page_data = scrape_wp_page(base_url, page_id, session)
        if page_data is None:
            continue

        asset_dir = output_dir / "assets" / slug
        asset_dir.mkdir(parents=True, exist_ok=True)
        asset_url_prefix = f"assets/{slug}"

        try:
            content_md = html_to_markdown(
                page_data["content_html"], asset_dir, asset_url_prefix, session
            )
        except Exception as exc:
            print(f"    ⚠ conversion error: {exc}", file=sys.stderr)
            content_md = page_data["content_html"]

        md_file = output_dir / f"{slug}.md"
        md_file.write_text(
            build_page_frontmatter(page_data["title"], slug) + content_md,
            encoding="utf-8",
        )
        written_pages += 1
        time.sleep(args.delay)

    # ------------------------------------------------------------------ summary
    print(f"\n=== Done ===")
    print(f"  Output dir  : {output_dir.resolve()}")
    print(f"  Blog posts  : {written_posts}")
    print(f"  Static pages: {written_pages}")

    # List what was created
    md_files = sorted(output_dir.rglob("*.md"))
    print(f"\n  Files written ({len(md_files)}):")
    for f in md_files:
        rel = f.relative_to(output_dir)
        print(f"    {rel}")


if __name__ == "__main__":
    main()
