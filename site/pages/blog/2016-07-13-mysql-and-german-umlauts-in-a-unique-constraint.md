---
title: "MySQL and German Umlauts in a Unique Constraint"
alias: "mysql-and-german-umlauts-in-a-unique-constraint"
tags:
  - "Informatics"
  - "MySQL"
weight: 0
created_at: "2016-07-13T00:00:00Z"
updated_at: "2016-07-13T00:00:00Z"
---

I recently came across some very odd behaviour in MySQL with [German Umlauts](http://joycep.myweb.port.ac.uk/abinitio/alphabet/umlautsz.html) (ö ä ü ß) and Unique Constraints. The problem is even documented as [Bug #57860](https://bugs.mysql.com/bug.php?id=57860) on mysql.com. In short, MySQL (or rather *utf8\_unicode\_ci*) would suggest that `foobär` is the same as `foobar`. So the statement\
`INSERT INTO test (test) VALUES ('foobar'),('foobär');` \
where *test* is a column with a unique index/constraint would fail.

This behaviour might be desired in some languages, but particularly for the german language this behaviour is not optimal. I'm sure if you find this blog post, you came across the same problem so I do not need to come up with another example.

The solution is simple, though you should think twice before you use it:\
Instead of *utf8\_unicode\_ci*, you could use *utf8\_general\_ci* or even the newer and more appropriate *utf8\_german2\_ci* (available starting with MySQL 5.6).