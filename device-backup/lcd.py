from machine import Pin, SPI
import framebuf
import time

class LCD_1inch47(framebuf.FrameBuffer):
    
    def __init__(self):
        self.width = 172
        self.height = 320
        self.spi = SPI(0, baudrate=40000000, sck=Pin(18), mosi=Pin(19))
        self.dc = Pin(16, Pin.OUT)
        self.cs = Pin(17, Pin.OUT)
        self.rst = Pin(20, Pin.OUT)
        self.bl = Pin(21, Pin.OUT)
        self.bl.value(1) # Backlight On
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
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

    def init_display(self):
        self.rst.value(1); time.sleep(0.1); self.rst.value(0); time.sleep(0.1); self.rst.value(1); time.sleep(0.1)
        self.write_cmd(0x11); time.sleep(0.12)
        self.write_cmd(0x36); self.write_data(0x00)
        self.write_cmd(0x3A); self.write_data(0x05)
        self.write_cmd(0x21); self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A); self.write_data(0x00); self.write_data(34); self.write_data(0x00); self.write_data(172 + 34 - 1)
        self.write_cmd(0x2B); self.write_data(0x00); self.write_data(0x00); self.write_data(0x01); self.write_data(0x3F)
        self.write_cmd(0x2C); self.dc.value(1); self.cs.value(0); self.spi.write(self.buffer); self.cs.value(1)