---
title: "Docker + Pycharm Problem + Fix"
alias: "docker-pycharm-problem-fix"
tags:
  - "Django"
  - "Docker"
  - "Linux"
  - "Python"
weight: 0
created_at: "2018-11-26T00:00:00Z"
updated_at: "2018-11-26T00:00:00Z"
---

Ever had one of these issues with Pycharm 2018 and Docker?

Couldn't refresh skeletons for remote interpreter\
The docker-compose process terminated unexpectedly: /usr/local/bin/docker-compose -f docker-compose.yml -f .PyCharm2018.3/system/tmp/docker-compose.override.8.yml run --rm --name skeleton\_generator\_643129755 python\
Regenerate skeletons

or

can't open file '/opt/.pycharm\_helpers/pycharm/django\_test\_manage.py' + "No such file or directory"

Then you should clear all pycharm helpers from your docker containers and images:

`docker ps -a | grep -i pycharm | awk '{print $1}' | xargs docker rm\
docker images | grep -i pycharm | awk '{print $3}' | xargs docker rmi\`