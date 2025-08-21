# main script 
from config import *
from serial_comm import SerialComm
from vision import Vision
from pid import PID
import time 

PRINT_INTERVAL = 0.1

def main():
    # init
    serial = SerialComm()
    pid_controller = None # init after ROI selection
    last_print_time = 0 
    
    def callback(gx, gy, x_norm, y_norm, t):
        nonlocal pid_controller, last_print_time
        if pid_controller is None:
            pid_controller = PID(vision.roi[2], vision.roi[3])
            
        output_x, output_y = pid_controller._compute_2axis(gx, gy)
        servo_x, servo_y = pid_controller.run(output_x, output_y)
        serial.send_angles(servo_x, servo_y)
        
        if t - last_print_time >= PRINT_INTERVAL:
            last_print_time = t
            print(f"[{t:.2f}] ball pos: ({gx},{gy}) | servo angles: X={servo_x}, Y={servo_y}")
    
    vision = Vision(callback=callback)
    
    try:
        vision.run()
    except KeyboardInterrupt:
        print("interrupted")
    finally:
        serial.disconnect()
        print("exiting")
    
    
    
if __name__ == "__main__":
    main()
    
    
