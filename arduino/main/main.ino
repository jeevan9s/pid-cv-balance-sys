// main Arduino-side program

#include <Servo.h>
#include "config.h"

// init
Servo SERVO_X;
Servo SERVO_Y;

String inputString = ""; // buffer
bool stringComplete = false;

// smoothing params
float smoothedX = SERVO_X_NEUTRAL;
float smoothedY = SERVO_Y_NEUTRAL;
const float alpha = ALPHA;

void setup() {
    Serial.begin(BAUD_RATE);
    SERVO_X.attach(SERVO_X_PIN);
    SERVO_Y.attach(SERVO_Y_PIN);

    inputString.reserve(32);
    Serial.println("arduino-side ready.");
}

void loop() {
    readSerial();
    if (stringComplete) {
        handleServoCommand(inputString);
        inputString = "";
        stringComplete = false;
    }
}

// -------- HELPERS --------

// ----- READ SERIAL -----
void readSerial() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

// ----- ACTUATION -----
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