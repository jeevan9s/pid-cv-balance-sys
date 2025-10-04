# config file (serial, cam, pid config)

# SERIAL
# ----------------
SERIAL_PORT = 'COM4'
BAUD_RATE = 115200

# CAM
# ----------------
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
CAM_INDEX = 0 
# PID
# ----------------
PID_X = {"kp": 3.0, "ki": 0.02, "kd": 0.2}
PID_Y = {"kp": 3.0, "ki": 0.02, "kd": 0.2}

OUTPUT_SCALE_X = 30
OUTPUT_SCALE_Y = 30


# SERVOs
# ----------------
SERVO_X_NEUTRAL = 65
SERVO_Y_NEUTRAL = 100

SERVO_X_MIN = 20
SERVO_X_MAX = 250
SERVO_Y_MIN = 20
SERVO_Y_MAX = 250

