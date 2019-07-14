from subprocess import Popen, PIPE
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

class Display:
    def __init__(self, lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7 ):
        lcd_rs = digitalio.DigitalInOut(lcd_rs)
        lcd_en = digitalio.DigitalInOut(lcd_en)
        lcd_d4 = digitalio.DigitalInOut(lcd_d4)
        lcd_d5 = digitalio.DigitalInOut(lcd_d5)
        lcd_d6 = digitalio.DigitalInOut(lcd_d6)
        lcd_d7 = digitalio.DigitalInOut(lcd_d7)
 
        self.lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
        self.lcd.clear()

    def update(self, message):
        self.lcd.clear()
        self.lcd.message = message 
    
if __name__ == "__main__":
    import time 
    d = Display(board.D12, board.D13, board.D25, board.D22, board.D23, board.D24)   
    while True:
        d.update("hello")
        time.sleep(3)
        d.update("\nworld")
    
