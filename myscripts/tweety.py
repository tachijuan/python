from twitter import *
import simplejson
import time
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)


turl = 'http://api.twitter.com/1.1/search/tweets.json?q='
CONSUMER_KEY = 'XXX'
CONSUMER_SECRET = 'XXX'
OAUTH_TOKEN = 'XXX'
OAUTH_SECRET = 'XXX'


t = Twitter( auth=OAuth(OAUTH_TOKEN,OAUTH_SECRET,CONSUMER_KEY,CONSUMER_SECRET) )

try:
  while True:
    twitter_results = t.statuses.home_timeline()
    tweet = twitter_results[0]['text']

    if 'ON' in tweet:
      print "LED Turned ON"
      GPIO.output(7,GPIO.HIGH)

    if "OFF" in tweet:
      print "LED turned OFF"
      GPIO.output(7,GPIO.LOW)

    time.sleep(10)

except KeyboardInterrupt:
  print "Exiting now!"
  GPIO.cleanup()


