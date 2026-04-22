---
title: "Download YouTube MPD Files"
alias: "download-youtube-mpd-files"
tags:
  - "Uncategorized"
weight: 0
created_at: "2016-02-23T00:00:00Z"
updated_at: "2016-02-23T00:00:00Z"
---

Ever wondered which representations YouTube is using for your video? Is it worth uploading your YouTube video with 20 Mbit/s at 1080p and 30 fps?

Find out by analyzing your YouTube videos MPD (Media Presentation Description) file, as explained in my new open source repository here: https://github.com/ChristianKreuzberger/extract-youtube-mpd

This is the result of one of my videos:

```
python extract.py https://www.youtube.com/watch?v=GTGUa4J8XKw aspen.mpd
```

```
Downloading HTML of https://www.youtube.com/watch?v=GTGUa4J8XKw 
Extracted MPDURL from HTML:  
https://manifest.googlevideo.com/api/manifest/dash/sparams/..... 
AdaptationSet,RepresentationID,Bitrate,Codec,ExtraInformation 
audio/mp4,140,127570,mp4a.40.2
video/mp4,133,247800,avc1.4d4015,426/240/24
video/mp4,134,601944,avc1.4d401e,640/360/24
video/mp4,135,1103336,avc1.4d401e,854/480/24
video/mp4,160,109967,avc1.42c00c,256/144/12
video/mp4,136,2206969,avc1.4d401f,1280/720/24
video/mp4,137,4144774,avc1.640028,1920/1080/24
```

This means my video is available at 4.1 Mbit/s at 1080p and 24 fps, 2.2 Mbit/s and 720p, 1 Mbit/s and 480p, etc... We have a paper submitted to NOSSDAV that shows a full analysis of YouTubes representations, so stay tuned for more information.