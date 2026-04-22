---
title: "Use Python Faker to create users automatically"
alias: "use-python-faker-to-create-users-automatically"
tags:
  - "Uncategorized"
weight: 0
created_at: "2016-11-18T00:00:00Z"
updated_at: "2016-11-18T00:00:00Z"
---

```
from django.contrib.auth.models import User
from faker import Faker
fake = Faker()

for i in range(0,200):
    name = fake.name()
    first_name = name.split(' ')[0]
    last_name = ' '.join(name.split(' ')[-1:])
    username = first_name[0].lower() + last_name.lower().replace(' ', '')
    user = User.objects.create_user(username, password=username)
    user.first_name = first_name
    user.last_name = last_name
    user.is_superuser = False
    user.is_staff = False
    user.email = username + "@" + last_name.lower() + ".com"
    user.save()
```