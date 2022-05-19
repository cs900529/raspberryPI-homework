# Import required Python libraries
import time
import sys
import smbus
import spidev
import os

tmpData = 0
joystick = [0, 0, 0]

# open(bus, device) : open(X,Y) will open /dev/spidev-X.Y
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 976000

# Read SPI data from MCP3008, Channel must be an integer 0-7
def ReadChannel(ch):
    if ((ch > 7) or (ch < 0)):
       return -1
    adc = spi.xfer2([1,(8+ch)<<4,0])
    data = ((adc[1]&3)<<8) + adc[2]
    return data

# Define sensor channels
light_ch = 0
swt_channel = 1
vrx_channel = 2
vry_channel = 3

# LCD setup
sys.modules['smbus'] = smbus
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

# LCD show data
def showLCD(data, joyList):
    global tmpData
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    x = tmpData - data
    JOY = ""
    xy = ""

    if(x > 10):
        lcd.write_string("Darker:" + str(data))
    elif(x < -10):
        lcd.write_string("Lighter:" + str(data))
    else:
        lcd.write_string("Light:" + str(data))
        
    tmpData = data

    lcd.cursor_pos = (1, 0)
    if(joyList[0] > 1000):
        JOY = JOY + "RIGHT"
        xy = "1"
    elif(joyList[0] < 10):
        JOY = JOY + "LEFT"
        xy = "-1"
    else:
        xy = "0"
        
    if(joyList[1] > 1000):
        JOY = JOY + "DOWN"
        xy += ",-1"
    elif(joyList[1] < 10):
        JOY = JOY + "UP"
        xy += ",1"
    else:
        xy += ",0"

    if(xy == "0,0"):
        JOY = "MIDDLE"

    '''if(joyList[2] < 2):
        JOY = JOY + "PRESSED"'''
        
    lcd.write_string(JOY + "(" + xy + ")")
    
try:
    while True:
        # Read the light sensor data
        light_data = 1024 - ReadChannel(light_ch)

        # Read the joystick position data
        joystick[0] = ReadChannel(vrx_channel)
        joystick[1] = ReadChannel(vry_channel)

        # Read switch state
        joystick[2] = ReadChannel(swt_channel)

        # Print out results
        showLCD(light_data, joystick)

        # Delay seconds
        time.sleep(1)
except:
    pass
finally:
    # Reset GPIO settings
    lcd.clear()
