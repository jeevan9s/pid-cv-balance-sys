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

        # ignore until PID is ready
        if pid_controller is None:
            return

        # apply dead zone
        x_input, y_input = x_norm, y_norm
        if abs(0.5 - x_norm) < DEAD_ZONE:
            x_input = 0.5
        if abs(0.5 - y_norm) < DEAD_ZONE:
            y_input = 0.5

        # compute PID corrections
        output_x, output_y = pid_controller._compute_2axis(x_input, y_input)

        # map to servo angles
        servo_x, servo_y = pid_controller.run(output_x, output_y)
        serial.send_angles(servo_x, servo_y)

        # periodic printout
        if t - last_print_time >= PRINT_INTERVAL:
            last_print_time = t
            print(f"[{t:.2f}] ball pos: ({gx},{gy}) | servo angles: X={servo_x}, Y={servo_y}")

    # create vision (ROI selection happens here)
    vision = Vision(callback=callback)

    # once ROI is selected, initialize PID with ROI size
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
