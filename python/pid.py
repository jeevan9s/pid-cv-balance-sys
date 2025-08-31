# pid control module
import config as cfg
import time
 
"""
error is defined as the displacement of the ball (cx, cy) from the platform's center (setpoint) (ROI_w/2, ROI_h/2)

the PID controller for each axis takes the error as input, and outputs a correction angle for each axis (controlled via arduino-side actuation)
"""

class PID:
    def __init__(self, w:int, h:int, pid_x=cfg.PID_X, pid_y=cfg.PID_Y, scale_x=cfg.OUTPUT_SCALE_X, scale_y=cfg.OUTPUT_SCALE_Y):
        self.setpoint_x = w // 2
        self.setpoint_y = h // 2
        
        self.scale_x = scale_x
        self.scale_y = scale_y
        
        self.kp_x, self.ki_x, self.kd_x = pid_x["kp"], pid_x["ki"], pid_x["kd"]
        self.kp_y, self.ki_y, self.kd_y = pid_y["kp"], pid_y["ki"], pid_y["kd"]
        print(f"x_controller coefficients: {pid_x['kp'], pid_x['ki'], pid_x['kd']}")
        print(f"y_controller coefficients: {pid_y['kp'], pid_y['ki'], pid_y['kd']}")
        
        # integral, derivative term states
        self.prev_error_x, self.prev_error_y, self.integral_x, self.integral_y = 0, 0, 0, 0
        self.prev_time = time.time()
    
    def _compute(self, error:float, prev_error:float, integral: float, kp:float, ki:float, kd:float, dt:float):
        # mono-axis computation 
        integral += error*dt
        integral = max(min(integral, 1.0), -1.0)

        
        if dt > 0:
            derivative = (error - prev_error) / dt
        else: 
            derivative = 0
        
        output = (kp * error) + (ki * integral) + (kd * derivative)
        return output, integral
    
    def _compute_2axis(self, cx: int, cy:int):
        curr_time = time.time()
        dt = curr_time - self.prev_time
        self.prev_time = curr_time
        
        err_x = 0.5 - cx
        err_y = 0.5 - cy
        
        output_x, self.integral_x = self._compute(err_x, self.prev_error_x, self.integral_x, self.kp_x, self.ki_x, self.kd_x, dt)
        self.prev_error_x = err_x
        
        output_y, self.integral_y = self._compute(err_y, self.prev_error_y, self.integral_y, self.kp_y, self.ki_y, self.kd_y, dt)
        self.prev_error_y = err_y
        
        return output_x, output_y
    
    def _convert_to_servo(self, output:float, neutral:int, min_angle:int, max_angle:int):
        # map and clamp PID output to servo angle 
        
        angle = neutral + output # map
        angle = max(min_angle, min(max_angle, angle)) # clamp
        return int(angle)
    
    def run(self, output_x:float, output_y:float):
        servo_x = self._convert_to_servo(
            output_x * self.scale_x,
            cfg.SERVO_X_NEUTRAL,
            cfg.SERVO_X_MIN,
            cfg.SERVO_X_MAX
        )

        servo_y = self._convert_to_servo(
            output_y * self.scale_y,
            cfg.SERVO_Y_NEUTRAL,
            cfg.SERVO_Y_MIN,
            cfg.SERVO_Y_MAX
    )
        
        return servo_x, servo_y
        
        
        
        
             
        
    

        
        
        
        


