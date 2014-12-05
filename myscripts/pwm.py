import threading
import time
import RPi.GPIO as GPIO

RED = 7
BLUE = 22
QUIT = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)

b = GPIO.PWM(BLUE, 50)  # channel=12 frequency=50Hz
b.start(0)

r = GPIO.PWM(BLUE, 50)  # channel=12 frequency=50Hz
r.start(0)


def cycle_red():
  print "in red"
  while QUIT == 0:
      print "loop start"
      for dc in range(0, 101, 5):
          r.ChangeDutyCycle(dc)
          time.sleep(0.1)
      for dc in range(100, -1, -5):
          r.ChangeDutyCycle(dc)
          time.sleep(0.1)

def cycle_blue():
  while QUIT == 0:
      for dc in range(0, 101, 5):
          b.ChangeDutyCycle(dc)
          time.sleep(0.1)
      for dc in range(100, -1, -5):
          b.ChangeDutyCycle(dc)
          time.sleep(0.1)

  

if __name__ == "__main__":

  t1 = threading.Thread(target = cycle_red, args= ())
  t2 = threading.Thread(target = cycle_blue, args= ())

  t1.start()
  t2.start()


  try:
    while 1:
      time.sleep(.1)
  except KeyboardInterrupt:
    QUIT = 1
    pass

  print 'exiting'
  GPIO.cleanup()
