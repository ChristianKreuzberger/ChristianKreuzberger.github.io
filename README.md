# personalWebsite

Personal website built with [press](https://github.com/ChristianKreuzberger/press), a single-binary static site generator.

## Structure

```
site/
  template.html       # HTML template used for all pages
  pages/
    index.md          # Homepage
    cv.md             # CV page
    blog/             # Blog posts (section)
    portfolio/        # Portfolio entries (section)
    assets/           # Static assets (images, etc.)
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

Build output is in `site/dist/`. Deploy that folder to any static host.
