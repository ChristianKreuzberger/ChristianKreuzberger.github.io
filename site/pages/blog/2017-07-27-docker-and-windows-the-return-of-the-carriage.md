---
title: "Docker and Windows – the return of the carriage…"
alias: "docker-and-windows-the-return-of-the-carriage"
tags:
  - "Docker"
  - "Informatics"
weight: 0
created_at: "2017-07-27T00:00:00Z"
updated_at: "2017-07-27T00:00:00Z"
---

One major difference when using Windows vs. Linux is that Windows "prefers" \r\n (CRLF) for newlines. This has been a known fact for years, and most tools will automatically handle this  (e.g., Filezilla). However, docker on Windows does not handle this, which will cause massive issues that are literally impossible to debug. For instance, you might get this error:

standard\_init\_linux.go:175: exec user process caused "no such file or directory"

This issue is really easy to fix: Convert your files from \r\n (CRLF) to just \n (LF). Most editors/IDEs on Windows can do that for you (including Notepad++). However, this will not be a permanent solution. If you are using GIT, you need to configure either your repository or your global GIT configuration to prefer \n over \r\n:

<https://help.github.com/articles/dealing-with-line-endings/>

Unless you really need to keep your \r\n, I recommend to change this globally with

```
git config --global core.autocrlf input
```