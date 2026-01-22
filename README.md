# EcoRover: Autonomous Edge AI Waste Collection Robot
**EcoRover** is an autonomous mobile robot designed to detect, track, and collect recyclable waste in real-time. It leverages **Edge AI** for low-latency vision processing and a microcontroller for precise actuation.

This project demonstrates the deployment of **Quantized Deep Learning models (TinyML)** on resource-constrained edge devices to solve real-world environmental challenges.



---

## 🚀 Key Features

* **Edge AI Vision:** Runs a custom-trained **YOLOv11n** model optimized via **TFLite quantization** on a Raspberry Pi 5, achieving real-time inference (~20-30 FPS).
* **Sensor Fusion:** Combines visual data with ultrasonic distance sensors for robust obstacle avoidance and path planning.
* **Dual-Controller Architecture:**
    * **Brain (RPi 5):** Handles heavy computation, object detection, and decision logic.
    * **Body (Arduino):** Handles PWM motor control, inverse kinematics for the robotic arm, and sensor readings.
* **Adaptive Communication:** Utilizes a custom **UART (Serial)** protocol for low-latency command transmission between the Pi and Arduino.
* **Automated Retrieval:** Features a 2-DOF robotic arm with a custom "Grab-and-Bin" sequence triggered autonomously upon object locking.

---

## 🛠️ Hardware Stack

| Component | Specification | Role |
| :--- | :--- | :--- |
| **SBC** | Raspberry Pi 5 (8GB) | Main compute unit, Vision processing |
| **Microcontroller** | Arduino Uno R3 | Motor & Servo controller |
| **Camera** | Pi Camera Module 3 / USB Webcam | Visual input for YOLO model |
| **Actuators** | 4x DC Motors + 2x MG996R Servos | Movement & Robotic Arm |
| **Driver** | L298N Motor Driver | Power distribution to motors |
| **Power** | 3S LiPo Battery (11.1V) | System power supply |

---