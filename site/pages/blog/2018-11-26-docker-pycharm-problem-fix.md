---
title: "Docker + PyCharm Problem + Fix"
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

# Docker + PyCharm Problem + Fix

Ever had one of these issues with PyCharm 2018 and Docker?

```text
Couldn't refresh skeletons for remote interpreter
The docker-compose process terminated unexpectedly: /usr/local/bin/docker-compose -f docker-compose.yml -f .PyCharm2018.3/system/tmp/docker-compose.override.8.yml run --rm --name skeleton_generator_643129755 python
Regenerate skeletons
```

or

```text
can't open file '/opt/.pycharm_helpers/pycharm/django_test_manage.py' + "No such file or directory"
```

Then you should clear all PyCharm helpers from your docker containers and images:

```bash
docker ps -a | grep -i pycharm | awk '{print $1}' | xargs docker rm
docker images | grep -i pycharm | awk '{print $3}' | xargs docker rmi
```