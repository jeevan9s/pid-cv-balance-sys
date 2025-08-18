// main Arduino-side program

#include <Servo.h>
#include <config.h>

// init
Servo SERVO_X;
Servo SERVO_Y;

String inputString = ""; // buffer
bool stringComplete = false;

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

  
  SERVO_X.write(angleX);
  SERVO_Y.write(angleY);
}