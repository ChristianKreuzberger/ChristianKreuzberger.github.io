# personalWebsite

Personal website built with [press](https://github.com/ChristianKreuzberger/press), a single-binary static site generator.

> **License:** All content (blog posts, portfolio, text, images), unless stated otherwise, is © Christian Kreuzberger and licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) — you may share it unchanged, with attribution, for non-commercial purposes; derivatives and commercial use need permission. This repo exists as an example of how to use `press`.

## Structure

```
site/
  template.html       # HTML template used for all pages
  pages/
    index.md          # Homepage
    cv.md             # CV page
    imprint.md        # Imprint / Impressum
    privacy-policy.md # Privacy policy
    blog/             # Blog posts (section)
    portfolio/        # Portfolio entries (section)
    assets/           # Static assets (images, etc.), one folder per section
  dist/               # Build output (git-ignored)
```

## Prerequisites

Install `press`:

```bash
curl -fsSL https://raw.githubusercontent.com/ChristianKreuzberger/press/main/install.sh | bash
```

## Workflow

```bash
cd site

# Serve locally with live rebuild
press serve

# Build to dist/
press build
```

## Adding Content

```bash
# New blog post
press create page blog/YYYY-MM-DD-my-post-title

# New portfolio entry
press create page portfolio/my-project

# List all pages
press tree
```

## Deploying

The live site ([chkr.at](https://chkr.at)) is hosted on a server in Germany. Build it with `press build` in `site/`; the output is in `site/dist/`.

Every push to `main` also publishes a demo copy to GitHub Pages (see `.github/workflows/deploy.yml`). The workflow installs the latest `press` release.
