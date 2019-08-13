import RPi.GPIO as GPIO

class Buttons:
    def __init__(self,up_pin_num, on_up, 
                down_pin_num, on_down, 
                sel_pin_num, on_sel):

        self.on_down = on_down
        self.on_up = on_up
        self.on_sel = on_sel

        self.up_pin_num = up_pin_num
        self.sel_pin_num = sel_pin_num
        self.down_pin_num = down_pin_num

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(up_pin_num, GPIO.IN) 
        GPIO.setup(down_pin_num, GPIO.IN)
        GPIO.setup(sel_pin_num, GPIO.IN)

        GPIO.add_event_detect(up_pin_num, GPIO.RISING, callback=self.on_up_function,)
        GPIO.add_event_detect(down_pin_num, GPIO.RISING, callback=self.on_down_function)
        GPIO.add_event_detect(sel_pin_num, GPIO.RISING, callback=self.on_sel_function)

    def on_up_function(self, chan):
        
        debounce = 0
        for _ in range(10):
            if GPIO.input(self.up_pin_num):
                debounce += 1

        if debounce == 10:
            up()
            self.on_up()

    def on_down_function(self, chan):

        debounce = 0
        for _ in range(10):
            if GPIO.input(self.down_pin_num):
                debounce += 1

        if debounce == 10:
            self.on_down()
            down()

    
    def on_sel_function(self, chan):
        debounce = 0
        for _ in range(10):
            if GPIO.input(self.sel_pin_num):
                debounce += 1

        if debounce == 10:
            sel()
            self.on_sel()

counter = 0

def down():
    global counter
    counter -= 1
    print("counter: " + str(counter))
def up():
    global counter
    counter += 1
    print("counter: " + str(counter))
def sel():
    print("sel")


if __name__ == "__main__":



    b =  Buttons(18, up, 4, down, 17, sel)
    while True:
        pass