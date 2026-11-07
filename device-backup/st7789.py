import time
from machine import Pin, SPI
import framebuf

class ST7789(framebuf.FrameBuffer):
    def __init__(self, spi, width, height, dc, rst, cs, bl):
        self.spi = spi
        self.width = width
        self.height = height
        self.dc = dc
        self.rst = rst
        self.cs = cs
        self.bl = bl
        
        self.buffer = bytearray(self.width * self.height * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        
        # Initialize pins
        self.dc.init(Pin.OUT, value=0)
        self.rst.init(Pin.OUT, value=1)
        self.cs.init(Pin.OUT, value=1)
        self.bl.init(Pin.OUT, value=1)
        
        self.reset()
        self.init_display()

    def write_cmd(self, cmd):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def write_data(self, data):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(bytearray([data]))
        self.cs.value(1)

    def reset(self):
        self.rst.value(1)
        time.sleep_ms(50)
        self.rst.value(0)
        time.sleep_ms(50)
        self.rst.value(1)
        time.sleep_ms(50)

    def init_display(self):
        self.write_cmd(0x11) # Sleep out
        time.sleep_ms(120)
        
        self.write_cmd(0x36) # Memory Data Access Control (Rotation)
        self.write_data(0x00) # Standard Portrait layout
        
        self.write_cmd(0x3A) # Interface Pixel Format
        self.write_data(0x05) # 16-bit color (RGB565)
        
        self.write_cmd(0x21) # Display Inversion On (Waveshare displays usually require this)
        
        self.write_cmd(0x29) # Display On

    def show(self):
        # Apply 172x320 physical centering offsets (X offset 34, Y offset 0)
        self.write_cmd(0x2A) # Column Address Set
        self.write_data(0x00)
        self.write_data(34)
        self.write_data(0x00)
        self.write_data(34 + self.width - 1)
        
        self.write_cmd(0x2B) # Row Address Set
        self.write_data(0x00)
        self.write_data(0)
        self.write_data(0x01)
        self.write_data(self.height - 1)
        
        self.write_cmd(0x2C) # Write to RAM
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(self.buffer)
        self.cs.value(1)