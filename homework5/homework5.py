import time
import board
import adafruit_dht
import sys, requests, smbus
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
sys.modules['smbus'] = smbus

TARGET_URL = 'localhost' 

# Initial the dht device, with data pin connected to GPIO4:
dhtDevice = adafruit_dht.DHT22(board.D4)

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True) 
lcd.clear()

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = round(temperature_c * (9 / 5) + 32, 2)
        humidity = dhtDevice.humidity
        #print("Input the simulation data\n")
        #temperature_c,humidity = eval(input("Please input the simulated temperature and humidity: \n temperature, humidity :  "))
        #temperature_f = temperature_c * (9 / 5) + 32
        print(
            "Temp: {:.2f} F / {:.2f} C    Humidity: {:.2f}% \n".format(
                temperature_f, temperature_c, humidity
            )
        )
        r = requests.get('http://{0}/LogRecord_GET.php?TEMPC={1}&TEMPF={2}&HUMD={3}'.format(TARGET_URL,temperature_c,temperature_f,humidity))
        print("Server Return Code :", r.status_code)
        print(r.text)
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Temp: {0:.2f}*C".format(temperature_c)) 
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Humidity: {0:.2f}%".format(humidity))
        time.sleep(2.0)
        
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        continue
    except:
        dhtDevice.exit()
        GPIO.cleanup()
        lcd.clear()
        break
