---
title: "Potential Breaking Changes with Django 2.0"
alias: "potential-breaking-changes-with-django-20"
tags:
  - "Informatics"
  - "Linux"
  - "Python"
  - "django"
  - "python"
weight: 0
created_at: "2017-10-09T00:00:00Z"
updated_at: "2017-10-09T00:00:00Z"
---

### ForeignKeys need to have the on\_delete Attribute set (e.g., to models.CASCADE for a cascading delete)

This also affects existing migrations. If you have migrations that you created with Django 1.8, you will run into errors (as they do not have that attribute set in the migration).

Also see this Ticket: <https://code.djangoproject.com/ticket/28677>

### Apps should specify the "app\_name" attribute in their urls.py

If you don't do this, you might run into an error when you include that urls.py in another urls.py

Also see this Ticket: https://code.djangoproject.com/ticket/28691

### SessionAuthenticationMiddleware is no longer available

If you have SessionAuthenticationMiddleware MIDDLEWARE listed (you most likely do if you are upgrading from an older Django Version), you will have to remove it from your middleware list (or tuple).

### user.is\_authenticated() and user.is\_anonymous() are no longer available as functions

They are now properties and have to be called without the function parentheses!

[More Info](https://docs.djangoproject.com/en/dev/releases/1.10/#using-user-is-authenticated-and-user-is-anonymous-as-methods)