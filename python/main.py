from config import *
from serial_comm import SerialComm
from vision import Vision
from pid import PID
import time 

PRINT_INTERVAL = 0.1
DEAD_ZONE = 0.01  # 1% tolerance around center

def main():
    # init serial
    serial = SerialComm()
    last_print_time = 0
    serial.send_angles(SERVO_X_NEUTRAL, SERVO_Y_NEUTRAL)

    pid_controller = None  # will init after ROI is known

    def callback(gx, gy, x_norm, y_norm, t):
        nonlocal last_print_time, pid_controller

        if pid_controller is None:
            return

        # get ROI origin + size
        rx, ry, rw, rh = vision.roi  

        # convert to ROI-relative pixels
        rel_x = gx - rx  
        rel_y = gy - ry  

        # apply dead zone (in pixels now)
        dead_zone_px_x = DEAD_ZONE * rw
        dead_zone_px_y = DEAD_ZONE * rh

        if abs((rw / 2) - rel_x) < dead_zone_px_x:
            rel_x = rw / 2
        if abs((rh / 2) - rel_y) < dead_zone_px_y:
            rel_y = rh / 2


        output_x, output_y = pid_controller._compute_2axis(rel_x, rel_y)
        servo_x, servo_y = pid_controller.run(output_x, output_y)
        serial.send_angles(servo_x, servo_y)


        if t - last_print_time >= PRINT_INTERVAL:
            last_print_time = t
            print(f"[{t:.2f}] ball pos(px): ({gx},{gy}) | servo: X={servo_x}, Y={servo_y}")

    
    vision = Vision(callback=callback)

    
    _, _, rw, rh = vision.roi
    pid_controller = PID(
        rw, rh,
        pid_x=PID_X,
        pid_y=PID_Y,
        scale_x=30,
        scale_y=30
    )

    try:
        vision.run()
    except KeyboardInterrupt:
        print("interrupted")
    finally:
        serial.disconnect()
        print("exiting")

if __name__ == "__main__":
    main()
