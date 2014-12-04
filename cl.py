#!/usr/bin/python
# a very simple ARGV example

import sys

if len(sys.argv) < 2:
  print " You need to enter more one or more files as the arguments to this script"
  exit(42)
else: 
  for myfile in sys.argv:
    print myfile

