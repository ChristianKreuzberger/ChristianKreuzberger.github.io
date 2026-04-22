---
title: "Container size matters – Optimize the size of your Python/Django Containers"
alias: "container-size-matters-optimize-the-size-of-your-pythondjango-containers"
tags:
  - "Uncategorized"
weight: 0
created_at: "2019-02-24T00:00:00Z"
updated_at: "2019-02-24T00:00:00Z"
---

In one of my recent videos I've disussed the size of the Django/Python Docker Containers and how to decrease it:

[Embedded video](https://www.youtube.com/watch?v=Ex3B8FU6uxc)

I failed to successfully create an image based on alpine, which is known to be very slim. With the help of Aaron Goodrich, who posted a comment with a Dockerfile for alpine, I was able to finally create such an image 🙂 Thanks for the help!

Without further ado, here are the results (and the respective Dockerfiles).

Please note that I have slightly changed the Dockerfile compared to the video above.

Based on Python 3.5 Jessie: 740 MB

```
FROM python:3.5-jessie

COPY ./app /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements/dev.txt
```

Based on Python 3.5 Slim: 188 MB

```
FROM python:3.5-slim

COPY ./app /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements/dev.txt
```

Based on Python 3.5 with Alpine: 248 MB

```
FROM python:3.5-alpine

COPY ./app /app
WORKDIR /app

RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .temp-build-deps gcc libc-dev linux-headers postgresql-dev

RUN pip install --no-cache-dir -r requirements/dev.txt

RUN apk del .temp-build-deps gcc libc-dev linux-headers postgresql-dev
```