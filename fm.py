#!/usr/bin/env python
import getopt,sys

def exttorealsize(number):
  deciIndex = ' KMGTPEZY'
  binIndex = ' kmgtpezy'
  base = 1024
  if (number[-1] in deciIndex+binIndex):
    index = binIndex.find(number[-1].lower())
    if (number[-1] in deciIndex):
      base = 1000
    retnum = int(number[:-1])*base**index
  else:
    retnum = int(number)
  return retnum
    

def usage():
  print """
  The usage for this command is:

  Don't do something stupid

  do it well
  """

def main():
    size = plug = 0
    flag = False
    try:
      opts, args = getopt.getopt(sys.argv[1:], "s:p:f")
    except getopt.GetoptError as err:
      # print help information and exit:
      print str(err) # will print something like "option -a not recognized"
      usage()
      sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
      if o == "-s":
        size = exttorealsize(a)
      elif o == "-p":
        plug = exttorealsize(a)
      elif o == "-f":
        flag = True;
      else:
        assert False, "unhandled option"

    print "size: %d, plug: %d, flag = %s" % (size,plug,flag)
    

if __name__ == "__main__":
    main()
