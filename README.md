# OpenCV-PID Ball Balancing System
<p align="left">
  <img src="assets/white.jpg" width="500" />
</p>

## Table of contents
* [description](#description)
* [hardware](#hardware)
* [software](#software)

## DESCRIPTION
- project with the scope of learning more about control theory and system design (PID), and embedded image processing (openCV).
- system prevents a ball from falling off a platform by controlling the position of the platform on two axes to keep the ball centered.
  
- a webcam tracks the ball’s position, feeding x/y coordinates into two PID controllers that compute corrective tilt angles, which are sent to an Arduino program to drive the motors.

system's design is _modular_, there are 3 main modules.

1. VISION: processes the webcam stream, and detects, tracks, and sends the position of the ball to the Control module. also creates a HUD. (python)
<p align="left">
  <img src="assets/white.jpg" width="250" />
</p>

2. CONTROL: computes the motor correction angles with the ball's positional coordinates via the PID algorithm/equation. (python)
 <p align="left">
  <img src="assets/white.jpg" width="250" />
</p>

3. ACTUATION: receives the correction angles, applies smoothing, and writes to each axis motor. (Arduino)
 <p align="left">
  <img src="assets/white.jpg" width="250" />
</p>


<br>
