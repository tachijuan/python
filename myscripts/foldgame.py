#JOHN CONWAY'S GAME OF LIFE
import RPi.GPIO as GPIO
import time
import random
import serial
import string
from plotter import mybuffer

MAXGENERATIONS = 4000
DISPLAY = True
gamecount = 0
maxgenfold = ''

def toggledisplay(pin):
  global DISPLAY
  p.turnondisplay()
  p.loadcustomchars(fullblock=False)
  DISPLAY = not DISPLAY
  print "Gamecount is %i" % gamecount


def countSurrounding(universe, a, b):
    count = 0
    surrounding = ((a - 1, b - 1),
                   (a - 1, b    ),
                   (a - 1, b + 1),
                   (a    , b - 1),
                   (a    , b + 1),
                   (a + 1, b - 1),
                   (a + 1, b    ),
                   (a + 1, b + 1))
    for a, b in surrounding:
        if not(a < 0 or b < 0 or a >= len(universe) or b >= len(universe[a])) and universe[a][b]:
            count += 1
    return count



def printUniverse(universe):
  p.clearbuf()
  for a in range(0,len(universe)):
    for b in range(0,len(universe[a])):
      if universe[a][b]: p.setxy(b,a) 


def fold(arr):
  b = ''
  for a in arr:
    b=b+''.join(map(lambda x: ["0","1"][x],a))
  return b


def dumpmaxgen(pin):
  print "maxgen looks like:"
  for l in [ maxgenfold[i:i+20] for i in range(0, 240, 20) ]:
    print l.translate(string.maketrans("0"," "))

  
if __name__ == "__main__":
  p = mybuffer(fullblock=False)

  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(16, GPIO.IN)
  GPIO.setup(7, GPIO.IN)

  GPIO.add_event_detect(16, GPIO.FALLING, callback = toggledisplay)
  GPIO.add_event_detect(7, GPIO.FALLING, callback = dumpmaxgen)

  try:
    maxgen = 0
    while 1:

      hist=[]
      nextUniverse=[]
      gamecount += 1

      for i in range(0,12):
          nextUniverse.append([random.randint(0,1) for r in xrange(20)])

      hist.append(fold(nextUniverse))
      gen = 0
      
      while gen<MAXGENERATIONS :
          universe = [a[:] for a in nextUniverse]
          printUniverse(universe)
          gen += 1
          if DISPLAY or gen>=maxgen:
            p.write("\xCD%3i" % gen)
          time.sleep(.5)
          for a in range(0, len(universe)):
              for b in range(0, len(universe[a])):
                  if universe[a][b] == 0 and countSurrounding(universe, a, b) == 3:
                      nextUniverse[a][b] = 1
                  elif universe[a][b] == 1 and countSurrounding(universe, a, b) not in (2, 3):
                      nextUniverse[a][b] = 0

          curr = fold(nextUniverse)
          if curr in hist:
            p.write("\xCD%3i" % gen)
            time.sleep(1)
            break
          else:
            hist.append(curr)
            if len(hist)>6: hist = hist[1:6]

      if gen > maxgen: 
        maxgen = gen
        maxgenfold = curr
        print "New record! %i" % maxgen

  except KeyboardInterrupt:
    print "\nQuitting..."
    print "We played %i games" % gamecount
    print "Max gen was %i" % maxgen
    for l in [ maxgenfold[i:i+20] for i in range(0, 240, 20) ]:
      print l.translate(string.maketrans("0"," "))
