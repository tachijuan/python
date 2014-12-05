import time
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)


try:
  while True:
    tweet = raw_input()

    if 'ON' in tweet:
      print "LED Turned ON"
      GPIO.output(7,GPIO.HIGH)

    if 'OFF' in tweet:
      print "LED turned OFF"
      GPIO.output(7,GPIO.LOW)

    if 'GREEN' in tweet:
      print 'Green ON'
      GPIO.output(22,GPIO.HIGH)

    if 'GROFF' in tweet:
      print 'Green OFF'
      GPIO.output(22,GPIO.LOW)

    #time.sleep(10)

except KeyboardInterrupt:
  print "Exiting now!"
  GPIO.cleanup()


