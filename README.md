PyJi
=====

PyJi is a lightweight tool (written in Python) that allows the user to invoke 
Atlassian JIRA REST APIs via the command line. In effect it's a wrapper of the [JIRA/Python library](https://pypi.python.org/pypi/jira) 

You can create comments and make transitions and many more. These are called "Actions". 
Each Action can take it's own set of parameters, PyJi can be directed as to what the user is trying to do and will execute the corresponding action
(actions will be added by myself or any contributors). It was written as a means to integrate Jenkins CI with JIRA which after July 10th 2015 stopped supporting SOAP APIs. The Jenkins plugin I was
using at the time was broken so I had to improvise :-)

PyJi has built in logging, command line option parsing, externalized configuration and can run in both Windows and Linux.

Installation
========

First you will need to install the [JIRA/Python library](https://pypi.python.org/pypi/jira) 

Download and install using `pip install jira` or `easy_install jira`

Then install PyJi by checking out a fresh copy from the [PyJi Repo](https://github.com/idimitrakopoulos/PyJi)

(ensure the user you are using has appropriate permissions)

Add a comment

```
> ./pyji.py -U https://jira.atlassian.net -u johndoe -p passwordHere -a comment -k "JRA-1" -c "hello world!"
```

Make a transition

```
> ./pyji.py -U https://jira.atlassian.net -u johndoe -p passwordHere -a transition -k "JRA-1" -s "Reopen"
```

Get Help for any action!
(simply specify which action and use -h)

```
> ./pyji.py -a comment -h
```

Contributing to PyJi
=====================

PyJi welcomes all forms of contributions!

If you want to create an action that doesnt exist please 

Please report any security issues you discover to idimitrakopoulos@gmail.com.

License
========

MIT License 
