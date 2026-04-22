---
title: "Django (REST) Filter Inconsistency with BooleanFilter / NullBooleanField"
alias: "django-rest-filter-inconsistency-with-booleanfilter-nullbooleanfield"
tags:
  - "Django"
  - "Informatics"
  - "Python"
weight: 0
created_at: "2017-11-29T00:00:00Z"
updated_at: "2017-11-29T00:00:00Z"
---

Django has an interesting default behaviour for NullBooleanFields, which are used by django\_filters BooleanFilter. While the String 'True' evaluates to Python Boolean True, and the String 'False' evaluates to Python Boolean False, this is not happening for the lowercase variants 'true' and 'false'. This is kind of annoying when you are using DJango Rest Filters, where you would have a REST API call like this (e.g., when calling from JavaScript):

GET /tasks/?show\_only\_my\_tasks=true

This does not work as expected, as "show\_only\_my\_tasks=true" evaluates to "None".

The correct usage according to Djangos NullBooleanField would have been this:

GET /tasks/?show\_only\_my\_tasks=True

To overcome this issue, you can use the following code snippet:

```
class BetterBooleanSelect(NullBooleanSelect):
    """
    Djangos NullBooleanSelect does not evaluate 'true' to True, and not 'false' to False
    This overwritten NullBooleanSelect allows that
    See https://code.djangoproject.com/ticket/22406#comment:3
    """
    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        return {
            '2': True,
            True: True,
            'true': True,  # added, as NullBooleanSelect does not do that
            'True': True,
            '3': False,
            'false': False,  # added, as NullBooleanSelect does not do that
            'False': False,
            False: False,
        }.get(value)

class BetterBooleanField(forms.NullBooleanField):
    """
    Better Boolean Field that also evalutes 'false' to False and 'true' to True
    """
    widget = BetterBooleanSelect

    def clean(self, value):
        return super(BetterBooleanField, self).clean(value)

class BetterBooleanFilter(django_filters.BooleanFilter):
    """
    This boolean filter allows evaluating 'true' and 'false'
    """
    field_class = BetterBooleanField
```

In your REST Filter you then only need to write this:

```
class TaskFilter(BaseFilter):
    """ Filter for Tasks """
    class Meta:
        model = Task

    show_only_my_tasks = BetterBooleanFilter()
```