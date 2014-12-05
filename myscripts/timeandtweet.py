from twitter import *
import simplejson
import serial
import datetime
import time
import threading


QUIT = 0
prevtweet = ""

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
  rangthebell = 0

  while QUIT == 0:
#    dates = centerstring(datetime.datetime.now().strftime("%B %d, %Y"),20)
#    times = centerstring(datetime.datetime.now().strftime("%I:%M:%S %p"),20)
#
#    p.write("\x80")
#    p.write("%s\r%s" % (dates,times))
    dates = datetime.datetime.now().isoformat(' ')[0:19]
    p.write("\x80")  # move to 0,0 on the display
    p.write(padstring(dates,20)) # make sure to have a nice clean line by filling it all out
    

    if datetime.datetime.now().strftime("%M")[-1:] == "5":
      if rangthebell == 0:
        p.write("\xD2\xE1\xD1\xE4\xD2\xE1") # do an anoying beep at the minute mark
        rangthebell = 1
    else:
      rangthebell = 0

    time.sleep(1)
  


def checktweet():

  turl = 'http://api.twitter.com/1.1/search/tweets.json?q='
  CONSUMER_KEY = 'xxx'
  CONSUMER_SECRET = 'xxx'
  OAUTH_TOKEN = 'XXX'
  OAUTH_SECRET = 'XXX'


  t = Twitter( auth=OAuth(OAUTH_TOKEN,OAUTH_SECRET,CONSUMER_KEY,CONSUMER_SECRET) )
  prevtweet = ""

  while QUIT == 0:
    twitter_results = t.statuses.home_timeline()
    tweet = twitter_results[0]['text'].encode('ascii','ignore')  # convert to ascii and ignore unicode conv. errors

    if prevtweet != tweet:
#      p.write("\xA8")  # second line 0 position (line 3 on the display)
      p.write("\x94")  # first line 0 position (line 2 on the display)
      p.write(padstring(tweet,60))
      p.write("\xD2\xE7\xD1\xE1\xD2\xE5")
      print "-"*150
      print "From: %s" % twitter_results[0]['user']['screen_name']
      print tweet
      print "-"*150
      prevtweet = tweet


    seconds = 0
    while seconds < 180:
      time.sleep (1)
      seconds += 1
      p.write("\xCD")
      p.write("%03d" % (180-seconds))
      if QUIT:
        break
    p.write("\xD0\xE7\xE2\xE2")
    #time.sleep(60)



if __name__ == "__main__":

  # open up the serial port
  p = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=2)
  p.write("starting the clock!")

  # clear the screen and get ready to display with backlight on
  p.write("\x16") # turns it on with no cursor blink
  p.write("\x11") # turn on the back light
  p.write("\x0C") # clear the screen. Must wait 5ms before we move on

  t1 = threading.Thread(target = runtime, args=())
  t2 = threading.Thread(target = checktweet, args=())

  t1.start()
  t2.start()

  try:
    while 1:
      time.sleep(.1)
  except KeyboardInterrupt:
    print "Quiting"
    QUIT = 1
    print "Exiting clock"
    t1.join()
    print "Exiting tweet"
    t2.join()
    print "Exits complete"
    p.write("\x15")    # turns display off, but not backlight
    p.write("\x12")    # turns backlight off
    p.close()
    QUIT = 1
    pass

  print 'exiting'

