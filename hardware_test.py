from gpiozero import Servo
from time import sleep

servo = Servo(17, initial_value=None)

try:
    servo.value = 0
    sleep(0.5)
    servo.value = None

    input("Press Enter to move slightly...")

    servo.value = 0.1
    sleep(0.4)
    servo.value = None

    print("Movement test complete")

finally:
    servo.close()