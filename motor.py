#!/usr/bin/python

from datetime import datetime
from datetime import timedelta
import subprocess
import RPi.GPIO as GPIO
import time

class MotorObject(object):
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)    
    
        self.enable_pin = 18
        self.coil_A_1_pin = 4
        self.coil_A_2_pin = 17
        self.coil_B_1_pin = 23
        self.coil_B_2_pin = 24
        
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)

        GPIO.output(self.enable_pin, 1)


    ## for the Stepper


    def forward(self, delay, steps):
        for i in range(0, steps):
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)

    def backwards(self, delay, steps):
        for i in range(0, steps):
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)
            
    def setStep(self, w1, w2, w3, w4):
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    ##**************
