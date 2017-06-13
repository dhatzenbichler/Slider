#!/usr/bin/python

from datetime import datetime
from datetime import timedelta
import subprocess
import RPi.GPIO as GPIO
import time

from wrappers import GPhoto
from wrappers import Identify
from wrappers import NetworkInfo


from ui import TimelapseUi
from motor import MotorObject


def main():
    
    print "Timelapse"
    camera = GPhoto(subprocess)
    
    idy = Identify(subprocess)
    netinfo = NetworkInfo(subprocess)
    ui = TimelapseUi()
    motor = MotorObject()
    motor.backwards(0.005,50)
    
    shot = 0
    

    network_status = netinfo.network_status()
    ui.main(motor, network_status)
    print "Test vor capture"
    
    try:
        
##        last_started = datetime.now()
##        print "Shot: %d Shutter: %s ISO: %d" % (shot)
##        ui.backlight_on()
##        print "Jetyt set shutter speed"
##        camera.set_shutter_speed(secs=config[0])
##        print "Jetyt nach set shutter speed"
##        print config[1]
##        camera.set_iso(iso=str(config[1]))
##        print "Jetyt nach set iso"
        
        if ui.getBkt() == True:
            camera.set_bracketing()
            print "nach Set Bracketing"
            
        ui.backlight_off()
            
            
        while True:
            try:
                if ui.getBkt() == True:
                    camera.capture_image_and_download(shot)
                    shot = shot + 1
                    camera.capture_image_and_download(shot)
                    shot = shot + 1
                    camera.capture_image_and_download(shot)

                else:
                    camera.capture_image_and_download(shot)
                
                time.sleep(intervall)
                
                motor.forward(5/1000,ui.getSteps())
                
                time.sleep(ui.getSteps()/33) # Zeit die der Motor yum fahren braucht
                
            except Exception, e:
                print "Error on capture." + str(e)
                print "Retrying..."
                # Occasionally, capture can fail but retries will be successful.
                continue
            shot = shot + 1
    except Exception,e:
        ui.show_error(str(e))


if __name__ == "__main__":
    main()