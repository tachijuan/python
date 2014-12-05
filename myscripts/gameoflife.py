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
  p.clearbuf()
  for a in range(0,len(universe)):
    for b in range(0,len(universe[a])):
      if universe[a][b]: p.setxy(b,a) 



if __name__ == "__main__":
  p = mybuffer(fullblock=False)

  try:
    maxgen = 0
    while 1:

      nextUniverse=[]
      universe=[]
      universe2=[]

      for i in range(0,12):
          nextUniverse.append([random.randint(0,1) for r in xrange(20)])
          universe.append([random.randint(0,1) for r in xrange(20)])
          universe2.append([random.randint(0,1) for r in xrange(20)])

      gen = 0
      
      while gen<999 :
          universe2 = [a[:] for a in universe]
          universe = [a[:] for a in nextUniverse]
          printUniverse(universe)
          gen += 1
          p.write("\xCD%3i" % gen)
          time.sleep(.5)
          for a in range(0, len(universe)):
              for b in range(0, len(universe[a])):
                  if universe[a][b] == 0 and countSurrounding(universe, a, b) == 3:
                      nextUniverse[a][b] = 1
                  elif universe[a][b] == 1 and countSurrounding(universe, a, b) not in (2, 3):
                      nextUniverse[a][b] = 0
          same = True
          for a in range(0,len(nextUniverse)):
            for b in range(0,len(nextUniverse[a])):
              if (nextUniverse[a][b] != universe2[a][b]):
                same = False
                break
          if same:
            break

      if gen > maxgen: maxgen = gen

  except KeyboardInterrupt:
    print "\nQuitting..."
    print "Max gen was %i" % maxgen
