---
title: "Compile, link and run ndnSIM with ndn-cxx as a shared library"
alias: "compile-link-and-run-ndnsim-with-ndn-cxx-as-a-shared-library"
tags:
  - "Uncategorized"
weight: 0
created_at: "2015-06-25T00:00:00Z"
updated_at: "2015-06-25T00:00:00Z"
---

A while ago, the build process of ndn-cxx and ndnSIM was modified to building a shared library in favour of a static library. Unfortunately, there are some problems with (re-)building ndnSIM in its current version ([dd516fe9ed73992d2f253a53fc5b21523c99a72a, June 24](https://github.com/named-data/ndnSIM/commits/master)):\
`\
error while loading shared libraries: libndn-cxx.so.0.3.2: cannot open shared object file: No such file or directory\`\
This is caused by the build process in combination with the location of libndn-cxx.so. On my system (ubuntu 14.04) the library is located at /usr/local/lib/, however, this is not a standard-path that waf/wscript looks for the library.\
Nevertheless, with PKG CONFIG in place, this should not be a problem, all we need to do is use the information from PKG CONFIG and put it into the NS3\_MODULE\_PATH.\
This can be achieved by modifying the ndnSIM wscript file (usually located in ns-3/src/ndnSIM).\
 `conf.check_cfg(package='libndn-cxx', mandatory=True, uselib_store='NDN_CXX', args=['--libs', '--cflags'])\
conf.env.append_value('NS3_MODULE_PATH',conf.env['LIBPATH_NDN_CXX'])`

The change to the scenario template is exactly the same.

An alternative change is to create a symbolic link to libndn-cxx.so in /usr/lib/x86\_64-linux-gnu (however I have not tested this).