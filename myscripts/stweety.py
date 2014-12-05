from twitter import *
import simplejson
import time
import RPi.GPIO as GPIO

turl = 'http://api.twitter.com/1.1/search/tweets.json?q='
CONSUMER_KEY = 'xxx'
CONSUMER_SECRET = 'xxx'
OAUTH_TOKEN = 'xxx'
OAUTH_SECRET = 'xxx'


t = TwitterStream( auth=OAuth(OAUTH_TOKEN,OAUTH_SECRET,CONSUMER_KEY,CONSUMER_SECRET) )
iterator = t.statuses.sample()

for tweet in iterator:
  print tweet


