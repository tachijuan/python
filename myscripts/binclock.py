import RPi.GPIO as GPIO
import time
import random
import serial
import datetime
import os
import string

DISPLAY = False

def toggledisplay(pin):
  global DISPLAY
  DISPLAY = not DISPLAY
  if DISPLAY:
    print "playing"
    os.system("mpc play")
  else:
    print "stopping"
    os.system("mpc stop")


def playnext(pin):
  if DISPLAY:
    print "playing next"
    os.system("mpc next")

def displaybinary(num):
  """ takes a numeral and converts it to a "binary string"
      the 0's are converted to -
      the 1's are converted to \x07 which we define as a full block"""
  return "{0:08b}".format(num).translate(string.maketrans("01","-\x07"))

def printbintime(time):
  p.write("\x8C"+times)
  h,m,s = map(int,time.split(":"))   # split the time into int values for h, m, s
  # this is very un-pythony (apparently)
  # I'm doing a ton of stuff here. First I position the text to the beginning of the correct line
  # Then we use the fancy join/map/lambda/list/format thing to take a string, convert it to binary string representation
  # make that into a list, use the list elements to index a two element list to convert the 0 and 1s to "-"s and blocks
  # with the custom character 0x07. Then we append the hour in decimal and in zero padded hex. 
  # --- the line below is the code I was talking about above
  # p.write('\x94'+''.join(map(lambda x: ["-","\x07"][int(x)],list("{0:08b}".format(int(h)))))+" "+h+" {0:02X}".format(int(h)))
  # ---
  # ok replaced that with a more pythony use of the translate method of the string package. Keeping the old one above for lambda reference
  #p.write('\x94'+"{0:08b} ".format(int(h)).translate(string.maketrans("01","-\x07"))+h+" {0:02X}".format(int(h)))

  # did some benchmark testing to see which of those is better and the string approach is about 5x times faster than the map thing:
  #[juan:~]$ python -m timeit -s "import string" '"{0:08b}".format(int("123")).translate(string.maketrans("01","-\x07"))'
  #100000 loops, best of 3: 2.21 usec per loop
  #[juan:~]$ python -m timeit "''.join(map(lambda x: ['-','\x07'][int(x)],list('{0:08b}'.format(int('123')))))"
  #100000 loops, best of 3: 10.9 usec per loop
  # one final thing - did some testing and the convesion to int from string was taking just as long as the string conversion, so
  # this was rewritten to split the time into ints for a single hit on the conversion
  p.write('\x94{0}{1:02}{2:02X}'.format(displaybinary(h),h,h))
  p.write('\xA8{0}{1:02}{2:02X}'.format(displaybinary(m),m,m))
  p.write('\xBC{0}{1:02}{2:02X}'.format(displaybinary(s),s,s))

  return time

if __name__ == "__main__":
  os.system("mpc play")
  p = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=2)
  p.write("Starting the thing")

  # clear the display
  p.write("\x16") # turns it on with no cursor blink
  p.write("\x11") # turn on the back light
  p.write("\x0C") # clear the screen. Must wait 5ms before we move on
  time.sleep(0.05) # sleep baby
  p.write("\x8087654321")

  # setup the two pins for the buttons. Button 16 is stop/play, button 7 is next song
  GPIO.setmode(GPIO.BOARD)
  TOGGLEPLAY = 16
  GPIO.setup(TOGGLEPLAY, GPIO.IN)
  NEXT = 7
  GPIO.setup(NEXT, GPIO.IN)

  GPIO.add_event_detect(TOGGLEPLAY, GPIO.FALLING, callback = toggledisplay)
  GPIO.add_event_detect(NEXT, GPIO.FALLING, callback = playnext)

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


  # play the game until we break with a control c
  ball = 0
  try:
    while 1:
      times = datetime.datetime.now().strftime("%H:%M:%S")
      printbintime(times)
      p.write("\xCD")
      if DISPLAY:
        p.write(chr(ball)) 
        ball = (ball + 1) % 8
      else:
        p.write(" ")
      time.sleep(1)
      

  except KeyboardInterrupt:
    p.write("\x15")    # turns display off, but not backlight
    p.write("\x12")    # turns backlight off
    p.close()
    os.system("mpc stop")
  

