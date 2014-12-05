import serial
import datetime
import time


def centerstring(string,width):
  """ Pad a string to a specific width """
  return " "*((width-len(string))/2)+string

# open up the serial port
p = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=2)
p.write("starting the clock!")

# clear the screen and get ready to display with backlight on
p.write("\x16") # turns it on with no cursor blink
p.write("\x11") # turn on the back light
p.write("\x0C") # clear the screen. Must wait 5ms before we move on

#p.write("\xFA") # start define of char 2
#p.write("\x3F\x1F\x0F\x07\x03\x07\x0F\x1F") # Define the bitmap

time.sleep(.05)
p.write("starting")


try:
  while 1:
    dates = centerstring(datetime.datetime.now().strftime("%B %d, %Y"),20)
    times = centerstring(datetime.datetime.now().strftime("%I:%M:%S %p"),20)

    p.write("\x80")
    p.write("%s\r%s" % (dates,times))
#    if datetime.datetime.now().strftime("%M") in ["00","15","30","45"]:
#      p.write("\xD2\xE1\xD1\xE4\xD2\xE1") # do an anoying beep at the minute mark
    #p.write("\r\x02")
    time.sleep(1)
except KeyboardInterrupt:
  p.write("\x15")    # turns display off, but not backlight
  p.write("\x12")    # turns backlight off
  p.close()
  pass

