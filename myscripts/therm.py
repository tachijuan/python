import RPi.GPIO as GPIO, time, os

DEBUG = 1
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.output(7,GPIO.LOW)
GPIO.setup(22,GPIO.OUT)
GPIO.output(22,GPIO.LOW)

Blink = True

def RCtime(RCpin):
  reading = 0
  GPIO.setup(RCpin, GPIO.OUT)
  GPIO.output(RCpin, GPIO.LOW)
  time.sleep(0.1)

  GPIO.setup(RCpin, GPIO.IN)

  while (GPIO.input(RCpin) == GPIO.LOW):
    reading += 1

  return reading


try:
  while True:
    light =  RCtime(12)
    leng = light / 500
    print "="*leng
    if (Blink):
      GPIO.output(7,GPIO.HIGH)
    else: 
      GPIO.output(7,GPIO.LOW)
    Blink = not(Blink)

    if (light > 40000):
      GPIO.output(22,GPIO.HIGH)
    else:
      GPIO.output(22,GPIO.LOW)

except KeyboardInterrupt:
  print "\n Leaving now\n"
  GPIO.cleanup()


