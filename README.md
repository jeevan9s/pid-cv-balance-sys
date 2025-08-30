# OpenCV-PID Ball Balancing System
<p align="left">
  <img src="assets/white.jpg" width="500" />
</p>

## Table of contents
* [description](#description)
* [hardware](#hardware)
* [software](#software)

## DESCRIPTION
- project with the scope of learning and applying control theory and system design (PID), and embedded image processing (openCV).
- system prevents a ball from falling off a platform by controlling the position of the platform on two axes to keep the ball centered.
  
- a webcam tracks the ball’s position, feeding x/y coordinates into two PID controllers that compute corrective tilt angles, which are sent to an Arduino program to drive the motors.
<p align="left">
  <img src="assets/white.jpg" width="350" />
</p>

System's design is _modular_, there are 3 main modules.

1. [**VISION**](assets/pid-cv-vision-workflowdrawio.drawio.png) processes the webcam stream, and detects, tracks, and returns the ball's positional coordinates. (python)
<p align="left">
  <img src="assets/white.jpg" width="250" />
</p>

2. [**CONTROL**](assets/pid-cv-control-workflow.drawio.png) computes the motor correction angles with the ball's positional coordinates via the PID algorithm/equation. (python)
 <p align="left">
  <img src="assets/white.jpg" width="250" />
</p>

3. [**ACTUATION**](assets/2pid-cv-actuation-workflow.drawio.png) receives the correction angles, applies smoothing, and writes to each axis motor. (Arduino)
 <p align="left">
  <img src="assets/white.jpg" width="250" />
</p>

## HARDWARE 
_Mechanical/structural components were assembled with hand & power tools for wood or designed in CAD software (Fusion360) and 3D-printed._
- MCU: ELEGOO UNO R3
- motors: DS3218MG
- USB camera: 640x480
- power source: 6V 2A AC Adapter


## SOFTWARE
Python and Arduino were used to program the system. 
- serial communication script was used to implement correction angle sending from control side to actuation side. (python -> serial -> arduino)
  
- languages: Python, Arduino
- Libraries: openCV, time, Servo
- design: Fusion360, KiCad
  <br>


<p align="center">
  <img src="assets/white.jpg" width="500" />
</p>
