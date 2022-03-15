#!/usr/bin/python3
import serial
import time
    
def relayTrig(serial):
    time.sleep(2)
    serial.write(("1\n").encode())
    time.sleep(5)
    serial.write(("1\n").encode())
    
def main():
    ser = serial.Serial('/dev/ttyUSB0', 115200) # Serial initialization
    try:
        if ser.is_open == True:
            relayTrig(ser)
    finally:
        print("Done watering the plants")

#methods initialization
main()
