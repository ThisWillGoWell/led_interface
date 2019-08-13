
def generate_callback(func, parameter):
    def callback():
        func(parameter)
    return callback




class MenuNode:
    def __init__(self, name, on_select=None, return_node=True):
        self.children = []
        if return_node:
            self.children.append(ReturnNode())
            
        self.name = name 
        self.current_index = 0
        self.parent = None 
        self.on_select = on_select

    """
    Attach a child node to it sub menu 
    """
    def attach_child(self, child):
        child.parent = self
        self.children.append(child)

    """
    triggerd when the menu is selected, if the function has a callback defiend, 
    call it and pass the paramter 
    """
    def selected(self):
        if self.on_select != None:
            self.on_select()

class NumSelectorNode:
    """
    Setting mode
    """
    def __init__(self, name, min_value, max_value, delta, on_update=None):
        self.name = name 
        self.min_value = min_value
        self.max_value = max_value
        self.value = (min_value + max_value) / (2 + delta - delta)
        self.on_update = on_update
        self.delta = delta
        self.parent = None 

    """
    when the up arrow is hit, what should happen
    trigger callback(self.value)
    """
    def on_up(self):
        if self.value != self.max_value:
            self.value = max(self.max_value, self.value + self.delta )
            if self.on_update is not None:
                self.on_update(self.value)

    """
    when the down arrow is hit, what should happen
    """
    def on_down(self):
        if self.value != self.min_value:
            self.value = max(self.min_value, self.value - self.delta )
            if self.on_update is not None:
                self.on_update(self.value)


class ReturnNode:
        name = "          return"
        def __init__(self):
            self.parent=None
            pass

class Menu: 
    def __init__(self, on_message_update=None, on_mode_update=None):
        self.nodes = self.build_modes(on_mode_update)

        self.current_node = None 
        self.top_level = self.nodes
        self.current_index = 0

        self.on_message_update = on_message_update
        self.update_message()

    

    

    def build_modes(self, on_mode_update):
        
        off_mode_num = 0
        rainbow_mode_num = 1
        sparkle_mode_num = 2
        theater_mode_num = 3
        aux_mode_num = 4
        mic_mode_num = 5
        test_brightness_mode_num = 6
        test_color_mode_num = 7
        test_write_speed = 8


        off_mode = MenuNode("off", on_select=generate_callback(on_mode_update, off_mode_num))
        color_modes = MenuNode("patterns")

        rainbow_node = MenuNode("rainbow", on_select=generate_callback(on_mode_update, rainbow_mode_num))
        rainbow_node.attach_child(NumSelectorNode("speed",1, 10, 1))
        rainbow_node.attach_child(NumSelectorNode("width", 0, 1000,5, on_interact))
        color_modes.attach_child(rainbow_node)

        music_node = MenuNode("sparkle", on_select=generate_callback(on_mode_update, sparkle_mode_num))
        music_node.attach_child(NumSelectorNode("speed",1, 10, 10, on_interact))
        music_node.attach_child(NumSelectorNode("width", 0, 1000,5, on_interact))
        color_modes.attach_child(music_node)
        
        theather_chase_node = MenuNode("theater chase", on_select=generate_callback(on_mode_update, theater_mode_num))
        theather_chase_node.attach_child(NumSelectorNode("speed",1, 10, 10, on_interact))
        theather_chase_node.attach_child(NumSelectorNode("width", 0,1000, 5, on_interact))
        color_modes.attach_child(theather_chase_node)

        reactive_nodes = MenuNode("Reactive")
        
        aux_node = MenuNode("aux",on_select=generate_callback(on_mode_update, aux_mode_num))
        reactive_nodes.attach_child(aux_node)
        
        mic_node = MenuNode("mic", on_select=generate_callback(on_mode_update, mic_mode_num))
        reactive_nodes.attach_child(mic_node)

        test_nodes = MenuNode("test")
        
        brightness_node = MenuNode("brightness", on_select=generate_callback(on_mode_update, test_brightness_mode_num))
        brightness_node.attach_child(NumSelectorNode("level", 0, 254, 1, on_interact))
        test_nodes.attach_child(brightness_node)

        color_node = MenuNode("color", on_select=generate_callback(on_mode_update, test_color_mode_num))
        color_node.attach_child(NumSelectorNode("level", 0, 254, 1, on_interact))
        test_nodes.attach_child(color_node)

        write_speed_node = MenuNode("write speed", on_select=generate_callback(on_mode_update, test_write_speed))
        write_speed_node.attach_child(NumSelectorNode("level", 0, 254, 1, on_interact))
        test_nodes.attach_child(write_speed_node)

        return [color_modes, reactive_nodes, test_nodes, off_mode] 
    
    def update_message(self):
        if self.current_node is None:
            self.current_message = self.top_level[self.current_index].name
        
        elif isinstance(self.current_node, MenuNode):
            self.current_message = "%s\n%s" % (
                self.current_node.name,
                self.current_node.children[self.current_index].name
            )
        
        elif isinstance(self.current_node, NumSelectorNode):
            self.current_message = "%s\n%s  %d" % (
                self.current_node.parent.name, 
                self.current_node.name,
                self.current_node.value
            )
        
        if self.on_message_update != None:
            print("update")
            self.on_message_update(self.current_message)
        
        
        print("update message:\t%s" %( self.current_message))

    def on_ok(self):
        if self.current_node is None:
            self.current_node = self.top_level[self.current_index]
   
        elif isinstance(self.current_node, MenuNode):
            
            if isinstance(self.current_node.children[self.current_index], ReturnNode): #return up 
                self.current_node = self.current_node.parent
            else:
                self.current_node = self.current_node.children[self.current_index]

            if isinstance(self.current_node, MenuNode):
                self.current_node.selected()
            

        elif isinstance(self.current_node, NumSelectorNode):
            self.current_node = self.current_node.parent 
        self.current_index = 0
        self.update_message()
            
        

    #note these are swapped so they feel better
    def on_up(self):
        if self.current_node is None: # root of the menu) 
            self.current_index = max(0, self.current_index - 1)

        elif isinstance(self.current_node, MenuNode):
            self.current_index = max(0, self.current_index -1)
        
        elif isinstance(self.current_node, NumSelectorNode):
            self.current_node.on_down()
        
        self.update_message()
        
        

    def on_down(self):
        if self.current_node is None: # root of the menu 
            self.current_index = min(len(self.top_level)-1, self.current_index + 1)
        
        if isinstance(self.current_node, MenuNode):
            self.current_index = min(len(self.current_node.children) - 1, self.current_index + 1)

        if isinstance(self.current_node, NumSelectorNode):
            self.current_node.on_up()

        self.update_message()

def on_interact(value):
    print("interact_value: ", value)

def on_select():
    print("selected")

if __name__ == "__main__":
    m = Menu()
    m.on_up()
    m.on_ok()
    m.on_ok()
    m.on_down()