---
title: "Why using Virtual Environments in Python is great"
alias: "why-using-virtual-environments-in-python-is-great"
tags:
  - "Informatics"
  - "Science"
  - "python"
  - "virtual environment"
weight: 0
created_at: "2017-09-17T00:00:00Z"
updated_at: "2017-09-17T00:00:00Z"
---

Remember those days when you just did something like

```
pip install numpy
pip install matplotlib
```

and wrote python code in some file called **calculate\_and\_plot.py** and your (data science) project just got some nice plots?

This was probably before you ever heard about Python **virtual environments**. And even if you did hear about it, you probably said to yourself: Why would I add another layer of complexity? I don't need that for now, It's just a little project.

> "I can handle my python libraries just fine without introducing more complexity!"

Well, let me tell you this: You are both right and wrong. If your goal is just doing a little project that you will use once and then forget about it, then you really don't need a virtual environment. However, this does not mean that you shouldn't use it! You will end up having to re-visit your code at some point in time, and then you are going to ask yourself the following two questions:

* What was this library called I used to do XYZ? (you probably wrote that down in a README anyway, right?
* What version of said library did I use? Was it 3.1? 5.7? 1.0? 0.9rc1? Oh my god there are so many different versions!?!

Both questions are only symptoms from a problem with how Python libraries are usually managed. Most operating systems (Windows as well as Linux) will install your Python libraries (such as numpy, matplotlib, Django, ...) into your OS Python lib-packages directory (that's also why you are usually required to do this with Admin rights or sudo).

> "But virtual environments are so complex, and I really need to finish this project on time, so ..."

Let me give you a quick introduction and you will see that they are not complex at all. Also, about the time component: Not using a virtual environment could be one of these things that you might regret later (e.g., when you give your Python code to a colleague).

## What are Python Virtual Environments?

Actually, the name is kind of misleading. "Virtual" usually implies that there is some kind of virtualization going on. This is not the case. It's really just a set of symbolic links (e.g., for the python binary) and directories that contain your python libraries.

What it really does is modifying your local environment variables and it tells the shell where to find the python interpreter and python libraries.

## How do I create a Python Virtual Environment?

IMHO the best and simplest way to create and manage your Virtual Environments, or "venvs" is to do it in your local project folder. Assuming you have the following project:

* research\_paper\_876/
  + statistics.py
  + data/
    - run1.csv
    - run2.csv
    - run3.csv
  + plots/
    - run1.png
    - run2.png
    - run3.png

Then you would create your virtual environment within the folder **research\_paper\_876** like this:

```
cd research_paper_876
virtualenv -p python3 venv
```

This will create a folder called **venv** in your **research\_paper\_876** directory. Note: If you are using git, svn or any other versioning system, I recommend adding an exception for the venv directory. DO NOT ADD THE VENV DIRECTORY TO YOUR VERSIONING CONTROL SYSTEM!

Your directory structure will now look like this:

research\_paper\_876/

* statistics.py
* data/
  + run1.csv
  + run2.csv
  + run3.csv
* plots/
  + run1.png
  + run2.png
  + run3.png
* **venv/**
  + bin/
    - python (symbolic link to your python installation)
    - pip (symbolic link to pip)
    - ...
  + include/
  + lib/
    - python3.\*/
      * site-packages/
        + ...
      * ...

Okay, next step: Activate your venv!

This is done with the following shell command:

```
source venv/bin/activate
```

Often you will find that your shell shows you that you have activated a virtual environment by adding a prefix, e.g.:

```
ckreuzberger@localhost:~/research_paper_876$ source venv/bin/activate
(venv)ckreuzberger@localhost:~/research_paper_876$
```

Now that you have activated your venv, you can install the desired libraries (e.g., numpy and matplotlib).

```
pip install numpy matplotlib
```

This will install these libraries and all required dependencies into your venv/lib/python3.\*/site-packages/ folder.

If you now run your python code (e.g., **python statistics.py**) within your venv, only the libraries installed in your venv will be used.

Two more things you need to know:

First: Create a file called requirements.txt in your projects main directory by using the following command:

```
pip freeze > requirements.txt
```

This will fill your requirements.txt with a set of libraries and versions. When I wrote this tutorial it looked like this:

```
numpy==1.13.1
matplotlib==2.0.2
```

Second: If you finished working with your project, you should deactivate your venv by running the following command:

```
deactivate
```

## How to re-create the same environment later

If you give your project to a colleague, or publish it on github, etc..., you would supply your code and the requirements.txt file. Your colleague can then create the exact same python virtual environment by executing the following commands:

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

This is something you could (and should) write into a README file, so you and potentially others don't forget about it later.

## Where can I read more about this?

I recommend reading the official docs on python.org about virtual environments: <https://docs.python.org/3/tutorial/venv.html>