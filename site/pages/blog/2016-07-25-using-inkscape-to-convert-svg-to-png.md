---
title: "Using Inkscape to Convert SVG to PNG"
alias: "using-inkscape-to-convert-svg-to-png"
tags:
  - "Uncategorized"
weight: 0
created_at: "2016-07-25T00:00:00Z"
updated_at: "2016-07-25T00:00:00Z"
---

While in [my previous post I explained how to mass convert images](/blog/shell-script-for-converting-multiple-images-at-once) using the convert command line tool, I've found another solution using inkscape.

```
inkscape yourfile.svg --export-png=yourfile.png -w256 -h256
```