import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  
import time 
class Knob:
    def __init__(self, encoder_pin_b, encoder_pin_a, switch_pin, on_turn_func, on_click_func):
        self.encoder_pin_a = encoder_pin_a
        self.encoder_pin_b = encoder_pin_b
        self.on_turn_func = on_turn_func
        self.on_click_func = on_click_func
        GPIO.setup(encoder_pin_b, GPIO.IN)  
        GPIO.setup(encoder_pin_a, GPIO.IN)  
        GPIO.setup(switch_pin, GPIO.IN)  

        self.fall_time = 0

        self.bounced = False 
        self.first_channel = -1

        self.debouncer = {}

        self.debouncer[encoder_pin_a] = {}
        self.debouncer[encoder_pin_a]['fall_time'] = 0
        self.debouncer[encoder_pin_a]['bounced'] = True
        
        self.debouncer[encoder_pin_b] = {}
        self.debouncer[encoder_pin_b]['fall_time'] = 0
        self.debouncer[encoder_pin_b]['bounced'] = True


        
        GPIO.add_event_detect(encoder_pin_b, GPIO.BOTH, callback=self.on_turn_event )  
        GPIO.add_event_detect(encoder_pin_a, GPIO.BOTH, callback=self.on_turn_event)  

        GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=self.on_click_event, bouncetime=500)  
        

    def on_turn_event(self, channel):
        t = time.time_ns()        
        if GPIO.input(channel): #rising edge
            if t - self.debouncer[channel]['fall_time'] > 1000000: # 1ms since last fall:
                self.debouncer[channel]['bounced'] =  True 
                if self.first_channel != -1 and self.first_channel != channel:
                    self.first_channel = -1
                    self.on_turn_func(channel == self.encoder_pin_a)


                
        else:
            if not self.debouncer[channel]['bounced'] and t - self.debouncer[channel]['fall_time'] > 1000000000: # 1 second since went down and not debounced, reset
                self.debouncer[channel]['bounced'] = True 
            
            if self.debouncer[channel]['bounced']: # are we ready to look at a down
                self.debouncer[channel]['fall_time'] = t
                self.debouncer[channel]['bounced'] = False

                if self.first_channel == -1:
                    self.first_channel = channel
               
    
    def on_click_event(self, value):
        self.on_click_func()
    
if __name__ == "__main__":
    def on_click():
        print("click")
    
    def on_turn(direction):
        print("\t\tturn: ", direction)
    
    Knob(18, 17, 4, on_turn, on_click)

    while True:
        pass