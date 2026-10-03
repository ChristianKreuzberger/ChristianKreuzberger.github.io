---
title: "Remove X-Powered-By Header in Apache2"
alias: "remove-x-powered-by-header-in-apache2"
tags:
  - "Linux"
  - "Security"
weight: 0
created_at: "2018-02-21T00:00:00Z"
updated_at: "2018-02-21T00:00:00Z"
---

# Remove X-Powered-By Header in Apache2

First you need to enable the headers modification:

```bash
a2enmod headers
```

Then you need to add the following to your apache2 configuration (e.g., to your vhost config):

```apache
Header always unset "X-Powered-By"
```