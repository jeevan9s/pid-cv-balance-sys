# main script 
from serial_comm import SerialComm
from config import *

def main():
    comm = SerialComm()

    if not comm.is_connected():
        return

    comm.send_angles(SERVO_X_NEUTRAL, SERVO_X_NEUTRAL)

    comm.disconnect()

if __name__ == "__main__":
    main()