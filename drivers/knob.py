import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  
from time import sleep

counter = 0

class Knob:
    def __init__(self, encoder_pin_b, encoder_pin_a, switch_pin, on_up_func, on_down_func, on_click_func):
        self.encoder_pin_a = encoder_pin_a
        self.encoder_pin_b = encoder_pin_b
        self.on_up_func = on_up_func
        self.on_down_func = on_down_func
        self.on_click_func = on_click_func

        GPIO.setup(encoder_pin_b, GPIO.IN)  
        GPIO.setup(encoder_pin_a, GPIO.IN)  
        GPIO.setup(switch_pin, GPIO.IN)  

        GPIO.add_event_detect(encoder_pin_a, GPIO.RISING, callback=self.rotation_decode, bouncetime=2)  
        GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=self.on_click_event, bouncetime=400)  
        


    def rotation_decode(self, channel):
        '''
        This function decodes the direction of a rotary encoder and in- or
        decrements a counter.

        The code works from the "early detection" principle that when turning the
        encoder clockwise, the A-switch gets activated before the B-switch.
        When the encoder is rotated anti-clockwise, the B-switch gets activated
        before the A-switch. The timing is depending on the mechanical design of
        the switch, and the rotational speed of the knob.

        This function gets activated when the A-switch goes high. The code then
        looks at the level of the B-switch. If the B switch is (still) low, then
        the direction must be clockwise. If the B input is (still) high, the
        direction must be anti-clockwise.

        All other conditions (both high, both low or A=0 and B=1) are filtered out.

        To complete the click-cycle, after the direction has been determined, the
        code waits for the full cycle (from indent to indent) to finish.

        '''

        global counter 

        sleep(0.002) # extra 2 mSec de-bounce time

        # read both of the switches
        Switch_A = GPIO.input(self.encoder_pin_a)
        Switch_B = GPIO.input(self.encoder_pin_b)

        if (Switch_A == 1) and (Switch_B == 0) : # A then B ->
           
            # at this point, B may still need to go high, wait for it
            while Switch_B == 0:
                Switch_B = GPIO.input(self.encoder_pin_b)
            # now wait for B to drop to end the click cycle
            while Switch_B == 1:
                Switch_B = GPIO.input(self.encoder_pin_b)
            print("up -> ", counter)
            counter += 1
            self.on_up_func()
            return

        elif (Switch_A == 1) and (Switch_B == 1): # B then A <-
            # A is already high, wait for A to drop to end the click cycle
            while Switch_A == 1:
                Switch_A = GPIO.input(self.encoder_pin_a)
            print("down <- ", counter)
            counter -= 1
            self.on_down_func()
            return

        else: # discard all other combinations
            return
                
    
    def on_click_event(self, channel):
        self.on_click_func()
        
if __name__ == "__main__":
    def on_click():
        print("click")
    
    def on_turn():
        print("\t\tturn: ")
    
    Knob(18, 17, 4, on_turn, on_turn, on_click)

    while True:
        pass