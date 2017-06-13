from time import sleep
try:
  from Adafruit_I2C import Adafruit_I2C
  from Adafruit_MCP230xx import Adafruit_MCP230XX
  from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
except ImportError:
  # This is just to allow the UI to be tested on Linux
  class Adafruit_CharLCDPlate(object):
    def __init__(self, busnum):
        pass

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class FakeCharLCDPlate(object):

    RED = "red"
    UP = "q"
    DOWN = "a"
    SELECT = "s"

    def __init__(self):
        self._getch = _GetchUnix()
        pass

    def clear(self):
        print "--LCD Cleared--"

    def message(self, msg):
        print msg

    def backlight(self, bl):
        print "Backlight %s" % str(bl)

    def fakeonly_getch(self):
        self._ch = self._getch()

    def buttonPressed(self, button):
        return self._ch == button



class TimelapseUi(object):

    def __init__(self):
        self._lcd = Adafruit_CharLCDPlate(busnum = 1)
        #self._lcd = FakeCharLCDPlate()
        self.intervall = 10
        self.bkt = False
        self.steps = 50
        self._lcd.backlight(self._lcd.ON)

    def update(self, text):
        self._lcd.clear()
        self._lcd.message(text)
        print(text)

    def getIntervall():
        return self.intervall
    
    def getBkt():
        return self.bkt
    
    def getSteps():
        return self.steps


    def show_config(self, configs, current):
        config = configs[current]
        self.update("Timelapse\nT: %s ISO: %d" % (config[0], config[1]))

    def show_status(self, shot, configs, current):
        config = configs[current]
        self.update("Shot %d\nT: %s ISO: %d" % (shot, config[0], config[1]))

    def show_error(self, text):
        self.update(text[0:16] + "\n" + text[16:])
        while not self._lcd.buttonPressed(self._lcd.SELECT):
            self.backlight_on()
            sleep(1)
            self.backlight_off()
            sleep(1)
        self.backlight_off()

    def backlight_on(self):
        self._lcd.backlight(self._lcd.ON)

    def backlight_off(self):
        self._lcd.backlight(self._lcd.OFF)
        

    def getMenu(self, current):
            
        if current == 0:
            self.update("BKT: " + str(self.bkt))
        elif current == 1:
            self.update("Start")
        elif current == 2:
            self.update("Intervall: " +str(self.intervall))
        elif current == 3:
            self.update("Steps: " +str(self.steps))
        elif current == 4:
            self.update("Drive Mode")
        else:
            self.update("End of Menu")

    def main(self, motor, network_status):
        self.backlight_on()
        self.update(network_status)
        current = 0
        while not self._lcd.buttonPressed(self._lcd.SELECT):
            pass

        ready = False
        while not ready:
            self.getMenu(current)
            
            while True:
                if (type(self._lcd) == type(FakeCharLCDPlate())):
                    self._lcd.fakeonly_getch()

                if self._lcd.buttonPressed(self._lcd.UP):
                    current -= 1
                    if current < 0:
                        current = 0
                    print current
                    break
                if self._lcd.buttonPressed(self._lcd.DOWN):
                    current += 1
                    print current
                    break
                if self._lcd.buttonPressed(self._lcd.LEFT):
                    if current == 0:
                        bkt = not bkt
                        
                    if current == 2:
                        self.intervall = self.intervall - 5
                        if self.intervall <= 0:
                            self.intervall = 5
                            
                    if current == 3:
                        self.steps = self.steps + 10
                        if self.steps <= 0:
                            self.steps = 5
                            
                    if current == 4:
                        motor.backwards(0.005,10)
                            
                    break
                
                if self._lcd.buttonPressed(self._lcd.RIGHT):
                    if current == 0:
                        self.bkt = not self.bkt
                    if current == 2:
                        self.intervall = self.intervall + 5
                    if current == 3:
                        self.steps = self.steps + 10
                    if current == 4:
                        motor.forward(0.005,10)
                        
                    break
                
                if self._lcd.buttonPressed(self._lcd.SELECT):
                    ready = True
                    
        return bkt, intervall



    

