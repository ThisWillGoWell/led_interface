from drivers.knob import Knob
from drivers.lcd import Display
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


class MenuNode:
    def __init__(self, name, on_select=None):
        self.children = []
        self.name = name 
        self.current_index = 0
        self.parent = None 
        self.on_select = on_select

    def attach_child(self, child):
        self.children.append(child)

    def selected(self):
        if self.on_select != None:
            self.on_select()

class NumSelectorNode:
    def __init__(self, name, min_value, max_value, delta, on_update):
        self.name = name 
        self.min_value = min_value
        self.max_value = max_value
        self.value = (min_value + max_value) / (2 + delta - delta)
        self.on_update = on_update
        self.delta = delta
        self.parent = None 

    def on_up(self):
        if self.value != self.max_value:
            self.value = max(self.max_value, self.value + self.delta )
            self.on_update(self.value)

    def on_down(self):
        if self.value != self.min_value:
            self.value = max(self.min_value, self.value - self.delta )
            self.on_update(self.value)

class Menu: 
    def __init__(self):
        self.nodes = self.build_modes()

        self.current_node = None 
        self.top_level = self.nodes
        self.current_index = 0
        
        self.current_message = "loading.."
        self.on_message_update = None 

    @staticmethod
    def build_modes():
        modes = []
        rainbow_node = MenuNode("rainbow", on_select)
        rainbow_node.attach_child(NumSelectorNode("speed",1, 10, 1, on_interact))
        rainbow_node.attach_child(NumSelectorNode("width", 0, 1000,5, on_interact))
        modes = modes.append(rainbow_node)

        music_node = MenuNode("music", on_select)
        music_node.attach_child(NumSelectorNode("speed",1, 10, 10, on_interact))
        music_node.attach_child(NumSelectorNode("width", 0, 1000,5, on_interact))
        modes = modes.append(music_node)
        
        theather_chase_node = MenuNode("theater chase", on_select)
        theather_chase_node.attach_child(NumSelectorNode("speed",1, 10, 10, on_interact))
        theather_chase_node.attach_child(NumSelectorNode("width", 0,1000, 5, on_interact))
        modes = modes.append(theather_chase_node)

        brightness_node = MenuNode("brightness", on_select)
        brightness_node.attach_child(NumSelectorNode("level", 0, 254, 1, on_interact))
        modes = modes.append(brightness_node)

        return modes 
    
    def update_message(self):
        if self.current_node is None :
            self.current_message = self.top_level[self.current_index].name
        
        if self.current_node is MenuNode:
            self.current_message = self.current_node.name 
        
        if self.current_node is NumSelectorNode:
            self.current_message = self.current_node.name + " " + str(self.current_node.value)
        
        if self.on_message_update != None:
            self.on_message_update(self.current_message)
        
        print("update message:\t%s", self.current_message)

    def on_ok(self):
        if self.current_node is None: 
            self.current_node = self.top_level[self.current_index]
   
        if self.current_node is MenuNode:
            if self.current_index == len(self.current_node.children): #return up 
                self.current_node = self.current_node.parent
            else:
                self.current_node = self.current_node.children[self.current_index]

        if self.current_node is NumSelectorNode:
            self.current_node = self.current_node.parent 
        
        self.update_message()
        


    def on_down(self):
        if self.current_node is None: # root of the menu 
            self.current_index = max(0, self.current_index - 1)

        if self.current_node is MenuNode:
            self.current_index = max(0, self.current_index -1)
        
        if self.current_node is NumSelectorNode:
            self.current_node.on_down()
        
        self.update_message()
        
        

    def on_up(self):
        if self.current_node is None: # root of the menu 
            self.current_index = min(len(self.top_level), self.current_index + 1)
        
        if self.current_node is MenuNode:
            self.current_index = min(len(self.current_node.children), self.current_index + 1)

        if self.current_node is NumSelectorNode:
            self.current_node.on_up()



def on_interact(value):
    print("interact_value: ", value)

def on_select():
    print("selected")
        

class Controller:
    def __init__(self):
        self.menu = Menu()    
        self.knob = Knob(   
            pin_knob_encoder_a, 
            pin_knob_encoder_b, 
            pin_knob_encoder_button,
            self.menu.on_up, 
            self.menu.on_down, 
            self.menu.on_ok
        )
        self.display = Display(
            pin_lcd_lcd_rs, 
            pin_lcd_lcd_en, 
            pin_lcd_lcd_d4, 
            pin_lcd_lcd_d5, 
            pin_lcd_lcd_d6, 
            pin_lcd_lcd_d7
        ) 

        self.menu.on_message_update = self.display.update



if __name__ == "__main__":
    c = Controller()

    

