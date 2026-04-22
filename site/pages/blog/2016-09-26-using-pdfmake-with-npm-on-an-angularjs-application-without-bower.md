---
title: "Using pdfmake with npm on an AngularJS Application (without bower)"
alias: "using-pdfmake-with-npm-on-an-angularjs-application-without-bower"
tags:
  - "Informatics"
weight: 0
created_at: "2016-09-26T00:00:00Z"
updated_at: "2016-09-26T00:00:00Z"
---

While people on the Internet are still fighting about npm vs bower, there are some packages that are only available for npm and some that are only available for bower. Unfortunately you will run into problems, sooner or later, just like I did today.

The package [pdfmake](http://pdfmake.org/) enables JavaScript applications to convert text to PDF, both within a website as well as a NodeJS server application. However, they explicitly state that the bower version should be used for web applications, and the npm version for server applications.

But if you want to use npm and want to avoid bower (for whatever reason), then you will run into a problem.\
Thankfully, somebody created a wrapper package for npm: <https://github.com/AaronBuxbaum/pdfmake-client>

You can install it via\
`\
npm install pdfmake-client --save`