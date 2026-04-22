---
title: "Phusion Passenger, Apache and SystemD’s PrivateTmp Folder"
alias: "phusion-passenger-apache-and-systemds-privatetmp-folder"
tags:
  - "Informatics"
  - "Linux"
weight: 0
created_at: "2018-01-23T00:00:00Z"
updated_at: "2018-01-23T00:00:00Z"
---

If you have ever gotten this error with your mod passenger installation:

```
$ passenger-config restart-app
*** ERROR: Phusion Passenger doesn't seem to be running. If you are sure that it
is running, then the causes of this problem could be one of:

1. You customized the instance registry directory using Apache's
 PassengerInstanceRegistryDir option, Nginx's
 passenger_instance_registry_dir option, or Phusion Passenger Standalone's
 --instance-registry-dir command line argument. If so, please set the
 environment variable PASSENGER_INSTANCE_REGISTRY_DIR to that directory
 and run this command again.
 2. The instance directory has been removed by an operating system background
 service. Please set a different instance registry directory using Apache's
 PassengerInstanceRegistryDir option, Nginx's passenger_instance_registry_dir
 option, or Phusion Passenger Standalone's --instance-registry-dir command
 line argument.
```

Then you most likely have SystemD running, which uses PrivateTmp folders instead of /tmp folders.

It's annoying, but easy to fix, see this blog post:\
<https://www.pistolfly.com/weblog/en/2016/01/passenger-config-and-passenger-status-result-in-an-error-on-centos7.html>