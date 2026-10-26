
import os
from time import sleep

SIMULATION = os.getenv("SIMULATION", "true").lower() == "true"

class ServoController:
    def __init__(self):
        self.state = "unknown"
        self.servo = None

        if not SIMULATION:
            from gpiozero import Servo
            self.servo = Servo(17, initial_value=None)

    def move(self, position):
        if position not in ("locked", "unlocked"):
            raise ValueError("Invalid position")

        if self.servo:
            angle = 0.2 if position == "locked" else -0.2
            self.servo.value = angle
            sleep(0.5)
            self.servo.value = None
        else:
            print(f"[SIMULATION] Moving to {position}")

        self.state = position
        return self.state
