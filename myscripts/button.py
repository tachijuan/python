""" Play with the serial LCD, and buttons
Also demos simple threading

TODO: Convert my cheap exit code into a proper thread exit code. 

"""


import RPi.GPIO as GPIO
import time
import serial
import datetime
import threading
from random import randint

#Glabals
command = {7:"Up",16:"Down"}
display = "Up"
QUIT = threading.Event()
#QUIT = 0

def centerstring(string,width):
  """ Pad a string to a specific width """
  return " "*((width-len(string))/2)+string

def padstring(string,width):
  """pad a string to a maximum length"""
  if len(string) > width:
    result = string[0:width]
  else:
    result = string + " "*(width-len(string))

  return result


def runtime():
  global display
  rangthebell = 0

  while not QUIT.isSet():
#    dates = centerstring(datetime.datetime.now().strftime("%B %d, %Y"),20)
#    times = centerstring(datetime.datetime.now().strftime("%I:%M:%S %p"),20)
#
#    p.write("\x80")
#    p.write("%s\r%s" % (dates,times))
    if display=="Up":
      dates = datetime.datetime.now().isoformat(' ')[0:19]
      p.write("\x11")
    else:
      dates = datetime.datetime.now().strftime('%B %Y %I:%m%p')
      p.write("\x12")
    p.write("\x80")  # move to 0,0 on the display
    p.write(padstring(dates,20)) # make sure to have a nice clean line by filling it all out


    if datetime.datetime.now().strftime("%M")[-1:] in ("5","0"):
      if rangthebell == 0:
        p.write("\xD2\xE1\xD1\xE4\xD2\xE1") # do an anoying beep at the minute mark
        rangthebell = 1
    else:
      rangthebell = 0

    time.sleep(.5)


def inputpressed(channel):
  global display 
  print "bang %s" % command[channel]
  display=command[channel]
  p.write("\x94") # second line
  p.write(padstring(centerstring(command[channel],20),20))

def timechanger():
  """ This is just for testing purposes. Not used right now """
  global display
  while not QUIT.isSet():
    print "changing time"
    if display=="Up":
      display="Down"
    else:
      display="Up"
    time.sleep(randint(3,7))


if __name__ == "__main__":

  p = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=2)
  p.write("Starting the thing!")    # clears out the buffers on the display

  # clear the display
  p.write("\x16") # turns it on with no cursor blink
  p.write("\x11") # turn on the back light
  p.write("\x0C") # clear the screen. Must wait 5ms before we move on

  time.sleep(0.05) # sleep baby
  t1 = threading.Thread(target = runtime, args=())
  t1.start()
#  t2 = threading.Thread(target = timechanger, args=())
#  t2.start()

  GPIO.setmode(GPIO.BOARD)

  INPUT1 = 7   # this is up
  INPUT2 = 16  # this is down
  GPIO.setup(INPUT1, GPIO.IN)
  GPIO.setup(INPUT2, GPIO.IN)

  # setup the callbacks for the buttons
  GPIO.add_event_detect(INPUT1, GPIO.FALLING, callback = inputpressed)
  GPIO.add_event_detect(INPUT2, GPIO.FALLING, callback = inputpressed)

  # clear the QUIT event 
  QUIT.clear()

  try: 
    while True:
      time.sleep(0.1)
  except KeyboardInterrupt:
    print "Quitting"
    QUIT.set()
    t1.join()
    p.write("\x15")  # display off
    p.write("\x12")  # backlight off

  print "done"
