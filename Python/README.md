Install Python on RHEL Software Collection List(SCL)

1. Installation

'''
$ su -
# yum install rh-python36
'''

2. Run Python in interactive mode using scl enable

'''
$ scl enable rh-python36 bash
$ python3
Python 3.6.3 (default, Oct  5 2017, 20:27:50)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print("Hello, Red Hat Developer Program World")
Hello, Red Hat Developer Program World
>>> quit()
$
'''
3. Python program can be run from the command line.

'''
$vi hello.py

#!/usr/bin/scl enable rh-python36 -- python3


import sys

version = "Python %d.%d" % (sys.version_info.major, sys.version_info.minor)
print("Hello, Red Hat Developer Program World from",version)

$ chmod +x hello.py
$ ./hello.py
Hello, Red Hat Developer Program World from Python 3.6
'''
