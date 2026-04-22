---
title: "Convert any video format to a animated gif using ffmpeg on Linux"
alias: "convert-any-video-format-to-a-animated-gif-using-ffmpeg-on-linux"
tags:
  - "Automation"
  - "Informatics"
  - "Linux"
weight: 0
created_at: "2017-05-10T00:00:00Z"
updated_at: "2017-05-10T00:00:00Z"
---

I needed a quick way of converting videos to gifs on Linux -ffmpeg and [this post on stackexchange](https://unix.stackexchange.com/a/298656) to the rescue!

The result is this neat little bash script:

```
#!/bin/bash

if [[ $# -eq 0 ]] ; then
 echo "Usage: videoToGif inputFile [outputFile] [FPS] [WIDTH]"
 echo "Example: videoToGif inputFile.ext outputFile.gif 60 360"
 exit 0
fi

inputFile=$1
outputFile=${2:-output.gif}

FPS=${3:-30}
WIDTH=${4:-360}

#Generate palette for better quality
ffmpeg -i $inputFile -vf fps=$FPS,scale=$WIDTH:-1:flags=lanczos,palettegen tmp_palette.png

#Generate gif using palette
ffmpeg -i $inputFile -i tmp_palette.png -loop 0 -filter_complex "fps=$FPS,scale=$WIDTH:-1:flags=lanczos[x];[x][1:v]paletteuse" $outputFile

rm tmp_palette.png
```

I used it to convert a Screencast created with "recordMyDesktop" (from OGV format) to a GIF.