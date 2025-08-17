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
PID_X = {"kp":1.0, "ki":0.0, "kd": 0.0}
PID_Y = {"kp":1.0, "ki":0.0, "kd": 0.0}

"""
default 
PID_X = {"kp":1.0, "ki":0.0, "kd": 0.0}
PID_Y = {"kp":1.0, "ki":0.0, "kd": 0.0}
"""

# SERVO
# ----------------
SERVO_X_NEUTRAL = 85
SERVO_Y_NEUTRAL = 135

SERVO_X_MAX = 160
SERVO_X_MIN = 100
SERVO_Y_MAX = 160
SERVO_Y_MIN = 100