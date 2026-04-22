---
title: "How good is my password?"
alias: "how-good-is-my-password"
tags:
  - "Cryptology"
  - "Security"
weight: 0
created_at: "2014-03-28T00:00:00Z"
updated_at: "2014-03-28T00:00:00Z"
---

There are several tools on the Internet that rate the quality of a password, though the reliability of those tools is questionable. How can one guarantee that the entered password is not transmitted to a 3rd party and added to a password database? In my master thesis I have analyzed the strength of passwords and here I want to give a short overview of what I consider a good password.

To start with, a good password must not be short. I do realize this is a very unobjective statement, hence I am going to be a little bit more precise. A lot of websites consider a password of length 8 as secure. I don't. The reason is simple: Considering alphanumerical letters only - both upper- and lowercase -, we only have an entropy of approximately 48 bits. An attacker would have to guess between 0 and 1, a total of 48 times in a row, or in other words there are approximatley 2^48 = 2.8 \* 10^14 possible passwords. Each password requires 48 bits to store it. If we wanted to generate all passwords and store them, it would require us approximatley 1,536 TerraBytes of disk space. Needless to say, when using a hash-function, the amount of disk-space will increase (e.g. with a 32 Byte Hash to 2,560 TerraBytes). For a single person this might look like a lot of disk space, though considering cloud storage and the fact that this is a one time computation, one could rent 2,560 cloud instances, each providing 1 TerraByte of disk space, and let them run for a day. While there certainly is some money involved, it is less expensive and it certainly does not take several years to crack a password of length 8.

If we consider the same calculation with alphanumerical letters and a password of length 12, we get an entropy of approx. 72 bits, which in short results in a lot more possibilities. The amount of disk space is about 10^8 higher than in the last example, meaning one would require 256 billion cloud instances.

NIST provides a definition of a passwords entropy without looking at the actual content, but by specifying rules. Following these rules, it would be advisable to have above 12 characters for a password. Furthermore, they advise the use of both, upper- and lowercase characters, numbers and special characters (such as $, @, ...), and they discourage the usage of words that can be found in a book.

My personal rules for a good password are similar to what NIST specifies:

* Must not be a word in a book or a combination of words
* Must contain some numbers (more than one)
* Must contain upper- and lowercase characters
* Must be at least of length 12, preferably 15
* Must be unique (as in: do not use the same password anywhere else)

Unfortunately those rules make it hard if not even impossible to remember a good password (without tricks).