// general testing program
#include "config.h"
#include <Servo.h>

Servo SERVO_X;
Servo SERVO_Y;

void setup() {
  Serial.begin(BAUD_RATE);
  SERVO_X.attach(SERVO_X_PIN);
  SERVO_Y.attach(SERVO_Y_PIN);
}

void loop() {
  SERVO_X.write(SERVO_X_NEUTRAL);
}
