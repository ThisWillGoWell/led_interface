from drivers.knob import Knob
from drivers.lcd import Display
from menu import Menu
import board

pin_knob_encoder_a = 18
pin_knob_encoder_b = 17
pin_knob_encoder_button = 4

# uses circuirt python bindings
pin_lcd_lcd_rs = board.D12
pin_lcd_lcd_en = board.D13
pin_lcd_lcd_d4 = board.D25
pin_lcd_lcd_d5 = board.D22
pin_lcd_lcd_d6 = board.D23
pin_lcd_lcd_d7 = board.D24

pin_lcd_lcd_rs, 
pin_lcd_lcd_en, 
pin_lcd_lcd_d4, 
pin_lcd_lcd_d5, 
pin_lcd_lcd_d6, 
pin_lcd_lcd_d7, 


class Controller:
    def __init__(self):
    
        self.display = Display(
            pin_lcd_lcd_rs, 
            pin_lcd_lcd_en, 
            pin_lcd_lcd_d4, 
            pin_lcd_lcd_d5, 
            pin_lcd_lcd_d6, 
            pin_lcd_lcd_d7
        ) 

        self.menu = Menu(self.display.update)    
        self.menu.update_message()

        self.knob = Knob(   
            pin_knob_encoder_a, 
            pin_knob_encoder_b, 
            pin_knob_encoder_button,
            self.menu.on_up, 
            self.menu.on_down, 
            self.menu.on_ok
        )


if __name__ == "__main__":
    c = Controller()
    while True:
        pass

