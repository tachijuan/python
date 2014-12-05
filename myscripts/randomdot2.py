from plotter import mybuffer
from random import randint
import time

if __name__ == "__main__":

  a = mybuffer()
  
  try:
    while 1:
      a.clearbuf()
      for r in range(100):
        a.setxy(randint(0,19),randint(0,11))
      time.sleep(5)
  except KeyboardInterrupt:
    print "exiting"
