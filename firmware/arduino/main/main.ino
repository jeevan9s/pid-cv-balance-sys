#include <Servo.h>
#include "config.h"

// init
Servo SERVO_X;
Servo SERVO_Y;

String inputString = "";
bool stringComplete = false;

float smoothedX = SERVO_X_NEUTRAL;
float smoothedY = SERVO_Y_NEUTRAL;
const float alpha = ALPHA;

void setup() {
    Serial.begin(BAUD_RATE);
    SERVO_X.attach(SERVO_X_PIN);
    SERVO_Y.attach(SERVO_Y_PIN);

    inputString.reserve(32);
    Serial.println("arduino-side ready.");

    // initPlatform();
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

void smoothMove(Servo &servo, float startAngle, float endAngle, int durationMs) {
    const int steps = 10; 
    float stepDelay = float(durationMs) / steps;
    float stepSize = (endAngle - startAngle) / steps;

    for (int i = 0; i <= steps; i++) {
        servo.write(startAngle + stepSize * i);
        delay(stepDelay);
    }
}
void initPlatform() {

    smoothMove(SERVO_X, SERVO_X_NEUTRAL, SERVO_X_MIN, 300);
    smoothMove(SERVO_Y, SERVO_Y_NEUTRAL, SERVO_Y_MIN, 300);
    delay(300);

    smoothMove(SERVO_X, SERVO_X_MIN, SERVO_X_MAX, 300);
    delay(300);

    smoothMove(SERVO_Y, SERVO_Y_MIN, SERVO_Y_MAX, 300);
    delay(300);

    smoothMove(SERVO_X, SERVO_X_MAX, SERVO_X_MIN, 300);
    delay(300);

    smoothMove(SERVO_Y, SERVO_Y_MAX, SERVO_Y_NEUTRAL, 300);
    smoothMove(SERVO_X, SERVO_X_MIN, SERVO_X_NEUTRAL, 300);
}

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

    angleX = constrain(angleX, SERVO_X_MIN, SERVO_X_MAX);
    angleY = constrain(angleY, SERVO_Y_MIN, SERVO_Y_MAX);

    smoothedX = alpha * angleX + (1 - alpha) * smoothedX;
    smoothedY = alpha * angleY + (1 - alpha) * smoothedY;

    SERVO_X.write(int(smoothedX));
    SERVO_Y.write(int(smoothedY));
}
