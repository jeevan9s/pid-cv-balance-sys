# config file (serial, cam, pid config)

# SERIAL
# ----------------
SERIAL_PORT = 'COM3'
BAUD_RATE = 115200

# CAM
# ----------------
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
CAM_INDEX = 0 
# PID
# ----------------
PID_X = {"kp": 2.0, "ki": 0.0, "kd": 1.0}
PID_Y = {"kp": 2.0, "ki": 0.0, "kd": 1.0}

OUTPUT_SCALE_X = 30
OUTPUT_SCALE_Y = 30


# SERVOs
# ----------------
SERVO_X_NEUTRAL = 65
SERVO_Y_NEUTRAL = 120

SERVO_X_MIN = 20
SERVO_X_MAX = 250
SERVO_Y_MIN = 20
SERVO_Y_MAX = 250

