# serial communication 
from config import *
import serial, time

class SerialComm:
    def __init__(self):
        self.ser = None
        self.connect()
    
    def connect(self):
    
        try:
            self.ser = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE)
            time.sleep(2)
            print("serial communication established")
        except Exception as e:
            print(f"serial communication failed to establish: {e} ")
            self.ser = None
    
    def is_connected(self):
        return self.ser is not None and self.ser.is_open
    
    def send_message(self, message):
        if self.ser is None:
            print("serial communication unavailable")
            return False
        
        try:
            if not message.endswith('\n'):
                message += '\n'
            self.ser.write(message.encode(encoding='ascii'))
            return True
        except Exception as e:
            print(f"failed to send message: {e}")
            return False
    
    def send_angles(self, angle_x, angle_y):
        
        if self.ser is None:
            print("serial communication unavailable")
            return False
        
        try:
            message = f"{angle_x} {angle_y}"
            
            if not message.endswith('\n'):
                message += '\n'
            self.ser.write(message.encode(encoding='ascii'))
            return True
        except Exception as e:
            print(f"failed to send message: {e}")
            return False
    
    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("serial communication closed")
            

        


