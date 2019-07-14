#!/usr/bin/env python2.7  
# script by Alex Eames https://raspi.tv  
# https://raspi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3  
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  
  
# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.  
# Both ports are wired to connect to GND on button press.  
# So we'll be setting up falling edge detection for both  
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  

# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
  
# now we'll define two threaded callback functions  
# these will run in another thread when our events are detected  
def my_callback1(channel):  
    print("falling edge detected on 27")
  
def my_callback2(channel):  
    print("falling edge detected on 18") 

def my_callback3(channel):  
    print("falling edge detected on 17") 

def my_callback4(channel):  
    print("falling edge detected on 4") 

input("Press Enter when ready\n>")  
  
# when a falling edge is detected on port 17, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(27, GPIO.RISING, callback=my_callback1, bouncetime=10)  
GPIO.add_event_detect(18, GPIO.RISING, callback=my_callback2, bouncetime=10)  
GPIO.add_event_detect(17, GPIO.RISING, callback=my_callback3, bouncetime=10)  
GPIO.add_event_detect(4, GPIO.RISING, callback=my_callback4, bouncetime=10)  

# when a falling edge is detected on port 23, regardless of whatever   
# else is happening in the program, the function my_callback2 will be run  
# 'bouncetime=300' includes the bounce control written into interrupts2a.py  

while True:
    pass

# try:  
#     print("Waiting for rising edge on port 24")
#     GPIO.wait_for_edge(24, GPIO.RISING)  
#     print("Rising edge detected on port 24. Here endeth the third lesson.")
  