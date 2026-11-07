from machine import I2C

class QMI8658:
    def __init__(self, i2c, addr=0x6B):
        self.i2c = i2c
        self.addr = addr
        # Basic sensor activation
        self.i2c.writeto_mem(self.addr, 0x02, b'\x01') 

    def read_xyz(self):
        # Read 6 bytes of acceleration data
        data = self.i2c.readfrom_mem(self.addr, 0x03, 6)
        # Convert to signed 16-bit integers
        x = int.from_bytes(data[0:2], 'little', True)
        y = int.from_bytes(data[2:4], 'little', True)
        z = int.from_bytes(data[4:6], 'little', True)
        return (x, y, z)