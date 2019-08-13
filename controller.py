from drivers.buttons import Buttons
from drivers.lcd import Display
from drivers.mcu import Mcu
from menu import Menu
import board

pin_button_up = 18
pin_button_down = 4
pin_button_select = 17

# uses circuirt python bindings
pin_lcd_lcd_rs = board.D12
pin_lcd_lcd_en = board.D13
pin_lcd_lcd_d4 = board.D25
pin_lcd_lcd_d5 = board.D22
pin_lcd_lcd_d6 = board.D23
pin_lcd_lcd_d7 = board.D24

class Controller:
    def __init__(self):
        
        self.mcu = Mcu()

        self.display = Display(
            pin_lcd_lcd_rs, 
            pin_lcd_lcd_en, 
            pin_lcd_lcd_d4, 
            pin_lcd_lcd_d5, 
            pin_lcd_lcd_d6, 
            pin_lcd_lcd_d7
        ) 

        self.menu = Menu(on_message_update=self.display.update, on_mode_update=self.mcu.set_mode)    
        self.menu.update_message()

        self.buttons = Buttons(   
            pin_button_up, 
            self.menu.on_up, 
            pin_button_down, 
            self.menu.on_down, 
            pin_button_select,
            self.menu.on_ok
        )


if __name__ == "__main__":
    c = Controller()
    while True:
        pass

