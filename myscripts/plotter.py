import serial
import time
import datetime

class mybuffer:
  def __init__(self,fullblock=True):
    self.buf = [[0 for y in range(20)] for x in range(4)]
    self.p = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout = 2)
    self.p.write("clear this string")
    self.p.write("\x16\x11\x0C")
    time.sleep(0.05)
    self.loadcustomchars(fullblock)


  def loadcustomchars(self,fullblock=True):
    '''define custom characters
     the lcd allows you to define chars 0-7 with custom bits.
     each char is made up of 5x8 bit matrices. We emit F8+char and then the 8 bytes that represent
     custom char.

     first I make an array that has tuples of the char and the bit mask
     this is an attempt to make my LCD "graphical" by using these characters to divide each
     cell into a 1x3 block. We have to permute all the possible "on" states for these cells
     as an option the constructor can be called so that the last character is made up of full bits
     this makes it look better for some of my apps that only use that character'''

    m=[('\xF8',[ 0, 0, 0, 0, 0, 0, 0, 0]),
       ('\xF9',[31,31, 0, 0, 0, 0, 0, 0]),
       ('\xFA',[ 0, 0, 0,31,31, 0, 0, 0]),
       ('\xFB',[31,31, 0,31,31, 0, 0, 0]),
       ('\xFC',[ 0, 0, 0, 0, 0, 0,31,31]),
       ('\xFD',[31,31, 0, 0, 0, 0,31,31]),
       ('\xFE',[ 0, 0, 0,31,31, 0,31,31])]
    if fullblock:
      m.append(('\xFF',[31,31,31,31,31,31,31,31]))
    else:
      m.append(('\xFF',[31,31, 0,31,31, 0,31,31]))

    # then I iterrate through the array tuples
    for mychar,mybits in m:
      self.p.write(mychar)         # emit the char
      for i in mybits:
        self.p.write(chr(i))       # emit the bits

  def clearbuf(self):
    self.buf = [[0 for y in range(20)] for x in range(4)]
    self.p.write("\x0C")
    time.sleep(0.05)

  def turnondisplay(self):
    self.p.write("\x16\x11")

  def printxy(self,x,y):
    self.p.write(chr(0x80+(y/3)*20+x))
    self.p.write(chr(self.buf[y/3][x]))

  def setxy(self,x,y):
    self.buf[y/3][x] = self.buf[y/3][x] | ( 1 << y%3 )
    self.printxy(x,y)

  def unsetxy(self,x,y):
    self.buf[y/3][x] = self.buf[y/3][x] & ~ ( 1 << y%3 )
    self.printxy(x,y)

  def printbuf(self):
    self.p.write("\x80")
    for x in self.buf:
      for y in x:
        self.p.write(chr(y))
  
  def printxystr(self,x,y,mess):
    self.p.write(chr(0x80+y*20+x))             # go the right spot on the screen
    self.p.write(mess)

  def write(self, mess):
    self.p.write(mess)

  def __del__(self):
    self.p.write("\x15\x12")
    self.p.close()




if __name__ == "__main__":
  a = mybuffer()
  b = mybuffer()
  b.setxy(19,2)
  b.setxy(7,5)
  b.printxystr(2,3,datetime.datetime.now().strftime("%H:%M"))
  time.sleep(2)

  a.setxy(19,3)
  a.printxystr(2,1,"above!")
  time.sleep(2)

  b.printxystr(2,1,"bitch!")
  time.sleep(10)

