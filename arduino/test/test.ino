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
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');  

    int spaceIndex = msg.indexOf(' ');
    if (spaceIndex > 0) {
      int angle_x = msg.substring(0, spaceIndex).toInt();
      int angle_y = msg.substring(spaceIndex + 1).toInt();

      angle_x = constrain(angle_x, SERVO_X_MIN, SERVO_X_MAX);
      angle_y = constrain(angle_y, SERVO_Y_MIN, SERVO_Y_MAX);

      SERVO_X.write(angle_x);
      SERVO_Y.write(angle_y);

      Serial.print("x=");
      Serial.print(angle_x);
      Serial.print(" y=");
      Serial.println(angle_y);
    }
  }
}
