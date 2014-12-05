import threading
import time
import os

song = "Blank"
e = threading.Event()

def padstring(string,width):
  """pad a string to a maximum length"""
  if len(string) > width:
    result = string[0:width]
  else:
    result = string + " "*(width-len(string))

  return result

def songgenerator():
  """ simulate a function that gets current song being played
      intended to be run as a separate thread """

  global song
  songlist = ['One one one one one one one one one:',
              'Two two two two two two two two two:',
              'Three three three three three three:']
  iter = 0;
  while not e.isSet():
    song = songlist[iter]
    iter += 1
    iter %= 3
    for i in range(1,100):
      time.sleep(.1)
      if e.isSet():
        break

def printsong():
  global song

  currsong = song
  i = 0
  while not e.isSet():
#    print "[2J[H",
#    os.system("clear")
    if currsong != song:
      currsong = song
      i = 0

    print "\x1B[2J\x1B[H:"+"-"*20+":"  # Go to upper left and print top ruler
    print ":\x1B[31m"+padstring(song[i:i+20],20)+"\x1b[0m:"   # print left and right bars with scrolling red
    print ":"+"-"*20+":"               # bottom bar
    if i == 0:                         # pause for a little longer at the start of a song
      time.sleep(.8)

    if (i <=len(song)):
      i += 1
    else:
      i = 0
    time.sleep(.2)

if __name__ == "__main__":
  e.clear()

  s = threading.Thread(target = songgenerator, args=())
  s.start()
  p = threading.Thread(target = printsong, args=())
  p.start()

  print "\x1B[?25l"   # hide cursor

  try:
    while True:
      time.sleep(.1)
  except KeyboardInterrupt:
    print "Quitting"
    e.set()

  print "\x1B[?25h"   # hide cursor
  print "Done main thread"

