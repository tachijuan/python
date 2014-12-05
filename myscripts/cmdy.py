import RPi.GPIO as GPIO
import time
import cmd

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

GPIO.output(7,GPIO.LOW)
GPIO.output(22,GPIO.LOW)


def RCtime(RCpin):
  reading = 0
  GPIO.setup(RCpin, GPIO.OUT)
  GPIO.output(RCpin, GPIO.LOW)
  time.sleep(0.1)

  GPIO.setup(RCpin, GPIO.IN)

  while (GPIO.input(RCpin) == GPIO.LOW):
    reading += 1

  return reading


def FlashPin(pin, count, delay):
  for i in range(0,count):
    GPIO.output(pin,True)
    time.sleep(delay)
    GPIO.output(pin,False)
    time.sleep(delay)


class LedBlinky(cmd.Cmd):

  COMMANDS = [ 'on', 'off']
  prompt = 'Master? : '

  def do_prompt(self,newprompt):
    """change the prompt"""
    self.prompt=newprompt

  def do_light(self,count):
    """Get the light measurement <count> number of times. Default is 1 time"""
    if (count == ''):
      count="1"
    for i in range(0,int(count)):
      light=RCtime(12)
      print "*"*(light/4000)+": %d" % light

  def do_green(self,command):
    """ Turn the Green LED ON or OFF"""
    if "on" in command:
      print 'Green ON'
      GPIO.output(22,GPIO.HIGH)
    elif "off" in command:
      print 'Green OFF'
      GPIO.output(22,GPIO.LOW)
    elif "flash" in command:
      print 'Flashing green'
      FlashPin(pin=22,count=5,delay=0.1)
    else:
      print "ERROR! MF!"


  def do_red(self,command):
    """ Turn the Red LED ON or OFF"""
    if "on" in command:
      print 'Red ON'
      GPIO.output(7,GPIO.HIGH)
    elif "off" in command:
      print 'Red OFF'
      GPIO.output(7,GPIO.LOW)
    elif "flash" in command:
      print 'Flashing green'
      FlashPin(pin=7,count=5,delay=0.1)
    else:
      print "ERROR! MF!"

  def complete_green(self, text, line, begidx, endidx):
    if not text:
      completions = self.COMMANDS[:]
    else:
      completions = [ f
                      for f in self.COMMANDS
                      if f.startswith(text)
                      ]
    return completions

  def complete_red(self, text, line, begidx, endidx):
    if not text:
      completions = self.COMMANDS[:]
    else:
      completions = [ f
                      for f in self.COMMANDS
                      if f.startswith(text)
                      ]
    return completions

  def emptyline(self):
    print "Empty line!"
    print "repeating: "+cmd.Cmd.lastcmd
    return cmd.Cmd.emptyline(self)

  def do_EOF(self, line):
    GPIO.cleanup()
    return True;

  def postloop(self):
    print

  def cmdloop(self):
    try:
      cmd.Cmd.cmdloop(self)
    except KeyboardInterrupt as e:
      print "Interrupt!"
      self.cmdloop()

if __name__ == '__main__':
  LedBlinky().cmdloop()

print "Exiting"
GPIO.cleanup()
