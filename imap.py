import os, sys, imaplib, rfc822, re, StringIO
import RPi.GPIO as GPIO
import time

server  ='mail.orlandini.us'
username='juan@orlandini.us'
password='all4b0g'


GPIO.setmode(GPIO.BOARD)
GREEN_LED = 22
RED_LED = 7
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)



M = imaplib.IMAP4_SSL(server)
M.login(username, password)
M.select()

try:
  while 1:

    print "checking email"
    typ, data = M.search(None, '(UNSEEN SUBJECT "PIFI MESSAGE")')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        #print 'Message %s\n%s\n' % (num, data[0][1])

        redon = re.search(	"RED ON",
                  data[0][1],
                  re.MULTILINE|re.DOTALL )
        greenon = re.search(	"GREEN ON",
                  data[0][1],
                  re.MULTILINE|re.DOTALL )
        redoff = re.search(	"RED OFF",
                  data[0][1],
                  re.MULTILINE|re.DOTALL )
        greenoff = re.search(	"GREEN OFF",
                  data[0][1],
                  re.MULTILINE|re.DOTALL )
        if redon:
          GPIO.output(RED_LED, True)
          print "red on"
        if greenon:
          GPIO.output(GREEN_LED, True)
          print "green on"
        if redoff:
          GPIO.output(RED_LED, False)
          print "red off"
        if greenoff:
          GPIO.output(GREEN_LED, False)
          print "green off"
          

    time.sleep(120)
    M.noop()
except KeyboardInterrupt:
  GPIO.cleanup()
  pass


M.close()
M.logout()
