import serial
import time

class RobotController:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2) # Wait for Arduino to reset
        except:
            print(f"Warning: Could not connect to {port}. Running in simulation mode.")
            self.ser = None

    def send_command(self, command):
        """Sends a command string to Arduino (e.g., 'F' for forward, 'G' for grab)"""
        if self.ser:
            self.ser.write(command.encode('utf-8'))
            print(f"Sent: {command}")
        else:
            print(f"[SIM] Sent: {command}")

    def stop(self):
        self.send_command('S')

    def move_forward(self):
        self.send_command('F')

    def turn_left(self):
        self.send_command('L')

    def turn_right(self):
        self.send_command('R')

    def grab_object(self):
        self.send_command('G')