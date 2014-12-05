import RPi.GPIO as GPIO     # mess with the pins
import time                 # you know - the time pauses and stuff
import serial               # to talk to the LCD 
import string               # forking strings
from random import randint


# define the screen buffer (4,20) char matrix
buf = [[0 for y in range(20)] for x in range(4)]


def clearbuf():
  global buf
  buf = [[0 for y in range(20)] for x in range(4)]

def printbuf():
  p.write('\x80')
  for x in buf:
    for y in x:
      p.write(chr(y))

def setxy(x,y):
  global buf
  buf[y/3][x] = buf[y/3][x] | (1 << y%3)   # turn on the bit in the buffer
  p.write(chr(0x80+(y/3)*20+x))            # go to the right spot on the screen
  p.write(chr(buf[y/3][x]))                # display the new block of bits

def unsetxy(x,y):
  global buf
  buf[y/3][x] = buf[y/3][x] & ~(1 << y%3)   # turn off the bit in the buffer
  p.write(chr(0x80+(y/3)*20+x))             # go the right spot on the screen
  p.write(chr(buf[y/3][x]))                 # display the new block of bits

if __name__ == "__main__":

  p = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=2)
  p.write("Starting the thing")

  # clear the display
  p.write("\x16") # turns it on with no cursor blink
  p.write("\x11") # turn on the back light
  p.write("\x0C") # clear the screen. Must wait 5ms before we move on
  time.sleep(0.05) # sleep baby

  #define custom characters
  # the lcd allows you to define chars 0-7 with custom bits.
  # each char is made up of 5x8 bit matrices. We emit F8+char and then the 8 bytes that represent
  # custom char.

  # first I make an array that has tuples of the char and the bit mask
  # this is an attempt to make my LCD "graphical" by using these characters to divide each
  # cell into a 1x3 block. We have to permute all the possible "on" states for these cells

  m=[('\xF8',[ 0, 0, 0, 0, 0, 0, 0, 0]),
     ('\xF9',[31,31,31, 0, 0, 0, 0, 0]),
     ('\xFA',[ 0, 0, 0,31,31,31, 0, 0]),
     ('\xFB',[31,31,31,31,31,31, 0, 0]),
     ('\xFC',[ 0, 0, 0, 0, 0, 0,31,31]),
     ('\xFD',[31,31,31, 0, 0, 0,31,31]),
     ('\xFE',[ 0, 0, 0,31,31,31,31,31]),
     ('\xFF',[31,31,31,31,31,31,31,31])]


  # then I iterrate through the array tuples
  for mychar,mybits in m:
    p.write(mychar)         # emit the char
    for i in mybits:
      p.write(chr(i))       # emit the bits

  try:
    while 1:
      clearbuf()
      printbuf()
      for r in range(100):
        setxy(randint(0,19),randint(0,11))
#        printbuf()
      time.sleep(10)


  except KeyboardInterrupt:
    p.write("\x15")    # turns display off, but not backlight
    p.write("\x12")    # turns backlight off
    p.close()

