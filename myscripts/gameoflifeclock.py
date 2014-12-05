#JOHN CONWAY'S GAME OF LIFE
import RPi.GPIO as GPIO
import time
import random
import serial
import datetime

DISPLAY = True

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
    if DISPLAY: p.write("\x80") 
    for a in universe:
        b = ''.join(map(lambda x: [" ","*"][x], a))   # magic to convert 1 to * and 0 to space and then to a single string
        p.write(b)
    times = datetime.datetime.now().strftime("%H:%M")
    if DISPLAY: p.write("\x8F"+times) 


def toggledisplay(channel):
  global DISPLAY
  DISPLAY = not DISPLAY

if __name__ == "__main__":
  p = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=2)
  p.write("Starting the thing")

  # clear the display
  p.write("\x16") # turns it on with no cursor blink
  p.write("\x11") # turn on the back light
  p.write("\x0C") # clear the screen. Must wait 5ms before we move on
  time.sleep(0.05) # sleep baby

  # setup a pin to toggle the time and life count
  GPIO.setmode(GPIO.BOARD)
  INPUT = 16
  GPIO.setup(INPUT, GPIO.IN)

  GPIO.add_event_detect(INPUT, GPIO.FALLING, callback = toggledisplay)

  # play the game until we break with a control c
  try:
    while 1:

      nextUniverse=[]         # clear out the universe
      for i in range(0,4):    # generate a new universe seed
          nextUniverse.append([random.randint(0,1) for r in xrange(20)])

      for gen in range(0, 30):  # run the universe for 30 generations
          universe = [a[:] for a in nextUniverse]
          printUniverse(universe)
          if DISPLAY: p.write("\xCD%3i" % gen)    # displays the generation on the bottom right of the LCD
          time.sleep(.3)
          for a in range(0, len(universe)):   # generate the next iteration
              for b in range(0, len(universe[a])):
                  if universe[a][b] == 0 and countSurrounding(universe, a, b) == 3:
                      nextUniverse[a][b] = 1
                  elif universe[a][b] == 1 and countSurrounding(universe, a, b) not in (2, 3):
                      nextUniverse[a][b] = 0
  except KeyboardInterrupt:
    p.write("\x15")    # turns display off, but not backlight
    p.write("\x12")    # turns backlight off
    p.close()
  
