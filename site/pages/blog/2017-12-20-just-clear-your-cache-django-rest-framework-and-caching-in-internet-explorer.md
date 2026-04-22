---
title: "Just… clear… your… cache… – Django Rest Framework and Caching in Internet Explorer"
alias: "just-clear-your-cache-django-rest-framework-and-caching-in-internet-explorer"
tags:
  - "Django"
  - "Informatics"
  - "Linux"
  - "Python"
weight: 0
created_at: "2017-12-20T00:00:00Z"
updated_at: "2017-12-20T00:00:00Z"
---

Inspired by a recent commitstrip: <http://www.commitstrip.com/en/2017/05/06/bugs-of-the-future/>

Like almost everyone else I had to test my Single Page AngularJS Application, which uses Django Rest Framework as a Backend, with Internet Explorer (11, thankfully). While my SPA works fine in Chrome and Firefox, it does not work very well in Internet Explorer (shocking, lmao).

Anyway, the obvious errors, ranging from needing polyfils to some CSS quirks, were fixed quickly.

But at some point I noticed: Why the hell are changes I make via PUT/POST/PATCH not shown when I make a GET request (retrieving all instances of a model) to the same endpoint afterwards? It kept returning the same data again and again. Where the hell did my changes go? Is my database broken? Is Internet Explorer not firing the PUT/POST/PATCH calls properly?

None of that was true. As it turns out, Internet Explorer 11 caches almost all GET requests to my REST API. I submit a change, I reload the page, and the change has disappeared. Caching at its best.

So I googled and stackoverflowed (is that a word?), and I found some people talking about cache headers. And they are god damn right... Django aswell as Django Rest Framework do not set any cache headers in the response (most likely for a good reason, better be explicit than implicit).

So I tried a couple of the provided solutions, and I must say, I was really unhappy with those approaches. They were either very repetitive (like the ``@never\_cache`` decorator added to all my viewsets), or required monkey patches and other sorts of things that I do not like to see. Btw, a cache buster within my JavaScript SPA was a no-go for me.

So I thought to myself: How about I make my whole Django Rest Framework Application "uncachable"? And so I did, with a very few lines of code and as a Django Middleware:

```
from django.utils.cache import add_never_cache_headers

class DisableClientSideCachingMiddleware(object):
    """
    Internet Explorer / Edge tends to cache REST API calls, unless some specific HTTP headers are added by our
    application.

    - no_cache
    - no_store
    - must_revalidate
    """
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response
```

Don't forget to also add this middleware to your settings.

```
MIDDLEWARE_CLASSES = (
    ...
    'yourapp.middlewares.DisableClientSideCachingMiddleware',
)
```

Please note that this disables caching of ALL requests coming to your Django Application. If you are serving static files from your Django Application (instead of serving them directly from your webserver), this will affect your performance.

This middleware works for me. I later discovered that somebody else has already [had a similar idea](https://stackoverflow.com/questions/2095520/fighting-client-side-caching-in-django), too. The obvious disadvantage here is that it disables caching for all parts of my Django Application. This is fine for me, as I am only using Django Rest Framework and I do not want caching on client side to happen at all, but it might not be okay for some other applications.

Nevertheless, I hope this piece of code helps people that have similar problems. Also, please feel free to share your experiences and solutions to such caching problems with Internet Explorer.