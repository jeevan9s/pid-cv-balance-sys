// general testing program
#include <Servo.h>

Servo SERVO_X;
Servo SERVO_Y;

void setup() {
  Serial.begin(112500);
  SERVO_X.attach(4);
  SERVO_Y.attach(2);
}

void loop() {
  // SERVO_X.write(65);
  // delay(2000);
  SERVO_Y.write(100);
}
