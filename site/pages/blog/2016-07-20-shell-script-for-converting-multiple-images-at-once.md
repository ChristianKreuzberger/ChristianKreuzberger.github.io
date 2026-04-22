---
title: "Shell Script for converting multiple images at once"
alias: "shell-script-for-converting-multiple-images-at-once"
tags:
  - "Automation"
  - "Linux"
weight: 0
created_at: "2016-07-20T00:00:00Z"
updated_at: "2016-07-20T00:00:00Z"
---

One of the tasks I come across often is converting images from one format into another. For instance, I need to convert SVG to PNG.

This can be achieved easily by using the "convert" commandline tool (ImageMagick) and a standard for loop in linux (note that I wrote the \*.svg statement in the for command on purpose and that I use "$f" on purpose):

```
for f in *.svg ; do
    convert "$f" "$f.png"
done
```

However, this produces ugly file names like "file1.svg.png", which could be desireable in some scenarios, but not in my case when I deploy it for a website. You can bypass this by using `${f%svg}png:`

```
for f in *.svg ; do
    convert "$f" "${f%svg}png"
done
```

Essentially this tool can handle a lot of use cases, for instance you can specify the picture density and which color should be used as transparent:

```
for f in *.svg ; do
    convert "$f" -density 300 -transparent white "${f%svg}png"
done
```

If you only want your pictures to have a certain size, you can resize them, e.g. using -resize 64x64:

```
for f in *.svg ; do
    convert "$f" -resize 64x64 -density 300 -transparent white "${f%svg}png"
done
```

However, you need to be careful when doing this. For instance, when the source image is smaller than the destination image, you might run into problems, and need to use the command like this:

```
for f in *.svg ; do
    convert  -resize 64x64 -density 300  "$f" -resize 64x64 -density 300 -transparent white "${f%svg}png"
done
```