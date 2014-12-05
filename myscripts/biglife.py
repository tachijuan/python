#JOHN CONWAY'S GAME OF LIFE
import time
import random
import serial
from plotter import mybuffer

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
    p.write("\x80")
    for a in universe:
        for b in a:
          p.setxy(b,a)


p = mybuffer()

try:
  while 1:

    nextUniverse=[]
    for i in range(0,12):
        nextUniverse.append([random.randint(0,1) for r in xrange(20)])

    for gen in range(0, 30):
        universe = [a[:] for a in nextUniverse]
        printUniverse(universe)
        p.write("\xCD%3i" % gen)
        time.sleep(.5)
        for a in range(0, len(universe)):
            for b in range(0, len(universe[a])):
                if universe[a][b] == 0 and countSurrounding(universe, a, b) == 3:
                    nextUniverse[a][b] = 1
                elif universe[a][b] == 1 and countSurrounding(universe, a, b) not in (2, 3):
                    nextUniverse[a][b] = 0
except KeyboardInterrupt:
  p.write("\x15")    # turns display off, but not backlight
  p.write("\x12")    # turns backlight off
  p.close()
  
