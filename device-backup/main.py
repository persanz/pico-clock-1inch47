import machine
import time
import gc
from lcd import LCD_1inch47

def main():
    # Force garbage collections
    gc.collect()
    
    # Allow time for power-up initialization
    time.sleep(1) 
    
    # 1. Initialize Display only
    lcd = LCD_1inch47()
    backlight = machine.Pin(21, machine.Pin.OUT)
    backlight.value(1) # Ensure screen is lit
    
    # Simple splash screens
    lcd.fill(0x0800)
    lcd.text("HELLO POTATO FRITO", 10, 10, 0x07E0)
    lcd.show()

    # 2. Draw static UI
    #lcd.fill(0x0000) # Black
    #lcd.text("SYSTEM ONLINE", 20, 50, 0xFFFF)
    #lcd.text("NO IMU DETECTED", 20, 80, 0xF800) # Red warning
    #lcd.show()
    
    #print("Dashboard running without sensors.")

    # 3. Main loop
    try:
        while True:
            # Add screen-only updates here
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped.")
        lcd.fill(0x0000)
        lcd.show()

if __name__ == '__main__':
    main()