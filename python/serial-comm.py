# serial communication 
from config import *
import serial, time

ser = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE)
time.sleep(2)

print("sending msg")
ser.write(b'hello there\n')

