# PID-OpenCV Ball Balancing Platform
> Control system leveraging PID & computer vision to balance a ball on a platform.

**WIP**: PID tuning is ongoing. Final results will be added soon.


<details>
<summary>Contents</summary>

- [Overview](#overview)
- [Architecture](#architecture)
  - [Firmware](#firmware)
  - [Hardware](#hardware)
- [Prerequisites / Installation](#prerequisites--installation)
- [Contact](#contact)

</details>

# Overview
<table width="100%" cellspacing="0" cellpadding="0">
  <tr>
    <td width="50%">
      <img src="/media/pid-cv-firmware-side.png" style="width:100%; height:auto;">
    </td>
    <td width="50%">
      <img src="/media/pid-cv-testing.gif" style="width:100%; height:auto;">
    </td>
  </tr>
</table>


I built this project to learn and apply control theory and system design (PID), and embedded image processing (openCV).

The system's main function is to balance a ball by using computer vision to extract its coordinates relative to a user-selected region of interest (ROI). These coordinates are then sent to a control module that computes the correctional Servo angles for both axes. The system's firmware was coded in a mix of Python and Arduino. 


## Built With
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
- ![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
- ![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)

# Architecture
## System
<div align="center">
      <img src="/media/pid-cv-workflow.png" width="50%" height="80%">
</div>



The system's design is _modular_, it conists of three sections:
<details>
  <summary><a href="/media/pid-cv-vision-workflow.png" target="_blank">Vision</a></summary>
  <p>
    This module processes the webcam stream, and detects, tracks, and returns the ball's positional coordinates.
  </p>

  <ul>
    <li>ROI Selection, HUD Creation</li>
    <li>Object Binarization, Gaussian Blur, Colour Masking, Contour Detection /li>
    <li>ROI-Relative Position Extraction (coords)</li>
  </ul>
</details>

<details>
  <summary><a href="/media/pid-cv-control-workflow.png" target="_blank">Control</a></summary>
  <p>
    The control module computes the motor correction angles with the ball's positional coordinates via the PID algorithm/equation.
  </p>

  <ul>
    <li>Compute correctional angles with PID on each axis (2 controllers)</li>
    <li>Convert to servo-writeable angles</li>
  </ul>
</details>

<details>
  <summary><a href="/media/pid-cv-actuation-workflow.png" target="_blank">Actuation</a></summary>
  <p>
    The actuation module receives the correction angles, applies smoothing, and writes to each axis motor.
  </p>

  <ul>
    <li>Read incoming serial data from Python-side (correction angles)</li>
    <li>Smooth and write angles to each motor (X and Y)</li>
  </ul>
</details>

## Firmware 
System was written in Python and Arduino, using _pyserial_ to connect  both sides. 

Code workflow consists of user selection of the ROI (region of interest), ball binarization, detection, and position extraction. Positions are then sent to the control script to calculate the correctional angles which are sent to the Arduino side via serial to be smoothed and applied to each motor. 

- The PID parameters along with any scaling/smoothing factors are tuned to optimized the system.

As seen in the <a href="/firmware/python/">Python</a> directory within <a href="/firmware/">Firmware</a>, there are code modules responsible for each step (vision, pid, serial, etc.). 

 **Here's an example of a vision module function:**

<details>
  <summary>binarize_ball()</summary>

```py
# this function is used to "binarize" the ball, converting the ball region into a clean binary mask by highlighting the ball based on its color (orange in my case).


def _binarize_ball(self, roi_bgr):
    # colour masking
    blurred = cv2.GaussianBlur(roi_bgr, (5,5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 120, 120])
    upper = np.array([25, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    # cleaning 
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel)

    return mask
```
</details>

**A snippet from the Arduino (actuation) module:**

<details>
<summary>handleServoCommand()</summary>

```cpp
// this functions takes the command (angles) sent by the Python side via serial, applies smoothing, and writes them to the motors. 

void handleServoCommand(String command) {
  int spaceIndex = command.indexOf(' ');
  if (spaceIndex == -1) return;  

  int angleX = command.substring(0, spaceIndex).toInt();
  int angleY = command.substring(spaceIndex + 1).toInt();

  smoothedX = alpha * angleX + (1 - alpha) * smoothedX;
  smoothedY = alpha * angleY + (1 - alpha) * smoothedY;

  
  SERVO_X.write(int(smoothedX));
  SERVO_Y.write(int(smoothedY));
}
```
</details>

## Hardware 
The system's hardware can be broken down into electrical and mechanical components. 
<br>
- The electric components feature an ELEGOO Uno R3 MCU for central control (serial, angle writing), and two 20kg DS3218 Servo motors; all powered by 6V 2A power from an AC Adapter.

- The mechanical components were mostly custom designed and 3D-Printed with Fusion360. These include a rising bracket/mount for the Servos, L-brackets to connect the Servo arms to the platform, and the system's central base. The acrylic platform was purchased seperately and drilled through for connection.

## Prerequisites / Installation

### Prerequisites

- Arduino IDE: with board support for your MCU
- Python environment
- pip for Python

### Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/jeevan9s/pid-cv-balance-sys.git
cd pid-cv-balance-sys
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Upload the Arduino sketch to your microcontroller using the Arduino IDE. Make sure the correct board and port are selected.

4. Run the main script:
```bash
python main.py
```
5. Select an ROI manually with your cursor and tune parameters in <a href="/firmware/python/config.py">config file</a> according to the observed behaviour.
<br>
thanks for reading!
<br>

## Contact 
[`email`](mailto:jeevansanchez42@gmail.com)&nbsp;&nbsp;&nbsp; [``LinkedIn``](https://linkedin.com/in/jeevansanchez)


