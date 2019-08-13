from smbus2 import SMBusWrapper

class Mcu:
    address = 0x20
    mode_address = 0x01    
    current_power_address = 0x02

    base_power_per_led = 1 
    def __init__(self):
        self.bus = SMBusWrapper(1)
    
    def set_mode(self, mode_number):
        print("set mode: ", mode_number)
        with self.bus as b:
            b.write_byte_data(self.address, self.mode_address, mode_number)
    
    def read_current_power(self):
        count = 0
        with self.bus as b:
            l = b.read_i2c_block_data(self.address, self.current_power_address, 4)
            count = l[3] * 16777216 + l[2] * 65536 + l[1] * 256 + l[0]
            print(l)
            print(count)
        return count 

if __name__ == "__main__":
    m = Mcu()
    import time
    while True:
        print( (m.read_current_power() * 0.045359477 + 500)/1000.0)
        time.sleep(1)