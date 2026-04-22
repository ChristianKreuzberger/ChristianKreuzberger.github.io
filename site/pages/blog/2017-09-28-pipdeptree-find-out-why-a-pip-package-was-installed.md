---
title: "pipdeptree – find out why a pip package was installed"
alias: "pipdeptree-find-out-why-a-pip-package-was-installed"
tags:
  - "Informatics"
  - "Linux"
  - "Python"
weight: 0
created_at: "2017-09-28T00:00:00Z"
updated_at: "2017-09-28T00:00:00Z"
---

Ever wondered why a certain python package was installed?

E.g., when you are installing `WeasyPrint` you will find that it installs a lot of other libraries, such as `cffi`, `cariocffi` and `html5lib`. With `pipdeptree` you can visualize this 🙂

`pip install pipdeptree`

`pipdeptree`

```
WeasyPrint==0.40
  - cairocffi [required: >=0.5, installed: 0.8.0]
    - cffi [required: >=1.1.0, installed: 1.11.0]
      - pycparser [required: Any, installed: 2.18]
  - CairoSVG [required: >=1.0.20, installed: 2.0.3]
    - cairocffi [required: Any, installed: 0.8.0]
      - cffi [required: >=1.1.0, installed: 1.11.0]
        - pycparser [required: Any, installed: 2.18]
    - cssselect [required: Any, installed: 1.0.1]
    - lxml [required: Any, installed: 3.8.0]
    - pillow [required: Any, installed: 4.2.1]
      - olefile [required: Any, installed: 0.44]
    - tinycss [required: Any, installed: 0.4]
  - cffi [required: >=0.6, installed: 1.11.0]
    - pycparser [required: Any, installed: 2.18]
  - cssselect2 [required: >=0.1, installed: 0.2.0]
    - tinycss2 [required: Any, installed: 0.6.0]
      - webencodings [required: >=0.4, installed: 0.5.1]
  - html5lib [required: >=0.999999999, installed: 0.999999999]
    - setuptools [required: >=18.5, installed: 36.5.0]
    - six [required: Any, installed: 1.11.0]
    - webencodings [required: Any, installed: 0.5.1]
  - Pyphen [required: >=0.8, installed: 0.9.4]
  - tinycss2 [required: >=0.5, installed: 0.6.0]
    - webencodings [required: >=0.4, installed: 0.5.1]
```