import RPi.GPIO as GPIO     # mess with the pins
import time                 # you know - the time pauses and stuff
import serial               # to talk to the LCD 
import datetime             # to get the curren time
import string               # forking strings
from mpd import MPDClient   # pip install python-mpd2
import threading            # to run parallel threads

DISPLAY = False
QUIT = threading.Event()   # event to signal all threads to quit
SONGLIST = []              # array used to keep track of the tracks that have been played.
TRACKWIDTH = 12             # width of the track "window"

def displaysong():
  """ Displays the current song or an alternating pattern if the Display button/variable is not set """
  global DISPLAY
  global mpdclient        # not sure if you need this
  global SONGLIST

  currsong = mpdclient.currentsong().get('title',' ')     # defaults to blank in case we can't get the MPD song
  currname = mpdclient.currentsong().get('name', ' ')
  SONGLIST.append(currsong)
  prevsong = currsong
  offset = 0
  noffset = 0
  flip = False
  line1 = " *"*(TRACKWIDTH/2)
  line2 = "* "*(TRACKWIDTH/2)
  line1 = line1.translate(string.maketrans("*","\x07"))
  line2 = line2.translate(string.maketrans("*","\x07"))

  while not QUIT.isSet():                                 # until thread termination is called
    currsong = mpdclient.currentsong().get('title',currsong)
    currname = mpdclient.currentsong().get('name', currname)

    if prevsong != currsong:                              # check for song switch
      SONGLIST.append(currsong)
      prevsong = currsong
      offset = 0
      noffset = 0

    if DISPLAY:                                           # display song or pattern
      l1 = currsong[0+offset:TRACKWIDTH+offset].ljust(TRACKWIDTH," ")       # rotate through the title string
      l2 = currsong[TRACKWIDTH+offset:TRACKWIDTH*2+offset].ljust(TRACKWIDTH," ")
      l3 = currsong[TRACKWIDTH*2+offset:TRACKWIDTH*3+offset].ljust(TRACKWIDTH," ")
      l0 = currname[0+noffset:11+noffset].ljust(11, " ")
    else:                                                 # pattern
      if flip:
        flip = not flip
        l1 = line1   # lazy way to enter the block chars
        l2 = line2
        l3 = line1
        l0 = "654321".ljust(11," ")
      else:
        flip = not flip
        l1 = line2
        l2 = line1
        l3 = line2
        l0 = "654321".ljust(11," ")
      offset = 0
      noffset = 0

    p.write("\x80"+l0)
    p.write("\x9C{0}\xB0{1}\xC4{2}".format(l1,l2,l3))   # display the lines

    if offset == 0:                                     # pause a little longer at the start of a song
      time.sleep(.8)

    offset = (offset + 1) % len(currsong)
    noffset = (noffset + 1) % len(currname)

    if DISPLAY:
      time.sleep(.4)
    else:
      time.sleep(.2)



def toggledisplay(pin):                                 # called when the toggledisplay button is pressed
  global DISPLAY
  DISPLAY = not DISPLAY
  p.write("\x16\x11")                                   # turn on the display and backlight in case it got botched
  if DISPLAY:
    print "playing"
    mpdclient.play()
  else:
    print "stopping"
    mpdclient.stop()


def playnext(pin):                                  # called when the playnext button is pressed
  if DISPLAY:
    print "playing next"
    mpdclient.next()
    print mpdclient.currentsong().get('name',' ')
    time.sleep(.4)    # just to make sure we have a bit of time to catch up
    mpdclient.play()

def displaybinary(num):
  """ takes a numeral and converts it to a "binary string"
      the 0's are converted to -
      the 1's are converted to \x07 which we define as a full block"""
  return "{0:06b}".format(num).translate(string.maketrans("01","-\x07"))

def printbintime(time):
  """ Print the time in the upper right in human and then in the lower left in binary+human+hex """
  p.write("\x8C"+time)
  h,m,s = map(int,time.split(":"))   # split the time into int values for h, m, s
  p.write('\x94{0}{1:02X}'.format(displaybinary(h),h))
  p.write('\xA8{0}{1:02X}'.format(displaybinary(m),m))
  p.write('\xBC{0}{1:02X}'.format(displaybinary(s),s))

  return time

if __name__ == "__main__":
  mpdclient = MPDClient()
  mpdclient.connect("localhost",6600)

  if DISPLAY:
    mpdclient.play()

  p = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=2)
  p.write("Starting the thing")

  # clear the display
  p.write("\x16") # turns it on with no cursor blink
  p.write("\x11") # turn on the back light
  p.write("\x0C") # clear the screen. Must wait 5ms before we move on
  time.sleep(0.05) # sleep baby
  p.write("\x80654321")

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

  # threading stuff
  QUIT.clear()
  t1 = threading.Thread(target = displaysong, args=())
  t1.start()


  # show the time until a break happens. I should run this on a separate thread. TODO

  try:
    while 1:
      times = datetime.datetime.now().strftime("%H:%M:%S")
      printbintime(times)
      p.write("\xCD")
      time.sleep(1)
      

  except KeyboardInterrupt:
    QUIT.set()          # signal all my threads to quit
    t1.join()           # wait for the display code to quit

    p.write("\x15")    # turns display off, but not backlight
    p.write("\x12")    # turns backlight off
    p.close()
    mpdclient.stop()
    mpdclient.close()
    
    print "We played:"
    for i in SONGLIST:
      print i

  

