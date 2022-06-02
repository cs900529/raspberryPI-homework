from time import sleep
import sys, requests, smbus
import mfrc522 as MFRC522
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import signal
sys.modules['smbus'] = smbus

TARGET_URL = 'localhost'

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True) 
lcd.clear()

MIFAREReader = MFRC522.MFRC522()

try:
    while True:
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print ("Card detected")
        
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            uid_decimal = uid[3]*256*256*256+uid[2]*256*256+uid[1]*256+uid[0]
            print(uid_decimal)

            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)


             # check OK?
            if status == MIFAREReader.MI_OK:
                rdData = MIFAREReader.MFRC522_Read(8)
                s = "".join([chr(c) for c in rdData])
                print(s)
            
                r = requests.get('http://{0}/RFID/LogRecord_GET.php?CONTENT={1}&UID={2}'.format(TARGET_URL,s,uid_decimal))
                print("Server Return Code :", r.status_code)
                print(r.text)

                lcd.clear()
                lcd.cursor_pos = (0, 0)
                lcd.write_string("UID:" + "{}".format(uid_decimal))
                lcd.cursor_pos = (1, 0)
                lcd.write_string(s)
                
                MIFAREReader.MFRC522_StopCrypto1()
                sleep(1)
            else:
                print ("Authentication error")
                sleep(1)
            
except:
    lcd.clear()
    GPIO.cleanup()
    MIFAREReader.MFRC522_StopCrypto1()
    
