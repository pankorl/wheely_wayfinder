# robot_movement.py

import RPi.GPIO as GPIO
# from mock_RPi import GPIO

import time
import threading

# Initialize GPIO mode
# GPIO.setmode(GPIO.BCM)

# Set up motor pins
motor_pins = {
    "front_left": [17, 18],
    "front_right": [22, 23],
    "rear_left": [24, 25],
    "rear_right": [26, 27]
}

# Configure GPIO pins
def setup_pins():
    for pins in motor_pins.values():
        GPIO.setup(pins[0], GPIO.OUT)
        GPIO.setup(pins[1], GPIO.OUT)

# Drive forward function
def drive_forward(duration):
    for pins in motor_pins.values():
        GPIO.output(pins[0], GPIO.HIGH)  # Forward pins to HIGH
        GPIO.output(pins[1], GPIO.LOW)   # Backward pins to LOW
    time.sleep(duration)
    stop()

# Rotate function
def rotate(duration):
    # Front left and rear left motors move backward
    GPIO.output(motor_pins["front_left"][1], GPIO.HIGH)
    GPIO.output(motor_pins["rear_left"][1], GPIO.HIGH)

    # Front right and rear right motors move forward
    GPIO.output(motor_pins["front_right"][0], GPIO.HIGH)
    GPIO.output(motor_pins["rear_right"][0], GPIO.HIGH)
    
    time.sleep(duration)
    stop()

# Stop function
def stop():
    for pins in motor_pins.values():
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.LOW)

# Cleanup function (if needed)
def cleanup():
    GPIO.cleanup()


def execute_robot_movements():
    setup_pins()
    time.sleep(2)
    drive_forward(2)
    rotate(1)
    time.sleep(2)
    GPIO.cleanup()

# GPIO.run_simulation(execute_robot_movements)
