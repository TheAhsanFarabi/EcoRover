#include <Servo.h>

// Pin Definitions (L298N Driver + Servos)
const int ENA = 5; const int IN1 = 6; const int IN2 = 7; // Left Motor
const int ENB = 10; const int IN3 = 8; const int IN4 = 9; // Right Motor
const int ARM_PIN = 11;
const int CLAW_PIN = 12;

Servo armServo;
Servo clawServo;

void setup() {
  Serial.begin(9600); // UART Baud Rate
  
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  
  armServo.attach(ARM_PIN);
  clawServo.attach(CLAW_PIN);
  
  // Initial State: Stop & Open Claw
  stopMotors();
  armServo.write(0);  // Retracted
  clawServo.write(90); // Open
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    
    switch(cmd) {
      case 'F': moveForward(); break;
      case 'L': turnLeft(); break;
      case 'R': turnRight(); break;
      case 'S': stopMotors(); break;
      case 'G': grabSequence(); break;
    }
  }
}

void moveForward() {
  analogWrite(ENA, 150); digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  analogWrite(ENB, 150); digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void turnLeft() {
  analogWrite(ENA, 120); digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  analogWrite(ENB, 120); digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void turnRight() {
  analogWrite(ENA, 120); digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  analogWrite(ENB, 120); digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
}

void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}

void grabSequence() {
  stopMotors();
  delay(500);
  armServo.write(100); // Lower arm
  delay(1000);
  clawServo.write(10); // Close claw
  delay(1000);
  armServo.write(0);   // Raise arm
  delay(1000);
  clawServo.write(90); // Drop in bin
  delay(500);
}