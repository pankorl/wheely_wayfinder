import tkinter as tk
import time
import threading

# Mock GPIO settings from RPi.py (you can replace this with actual RPi GPIO if needed)
class GPIO:
    BOARD = "BOARD"
    OUT = "OUT"
    HIGH = "HIGH"
    LOW = "LOW"
    pins = {}

    @staticmethod
    def setmode(mode):
        pass

    @staticmethod
    def setup(pin, mode):
        GPIO.pins[pin] = GPIO.LOW

    @staticmethod
    def output(pin, state):
        GPIO.pins[pin] = state
        update_wheels()

    @staticmethod
    def cleanup():
        pass

def update_wheels():
    for motor, pins in motor_pins.items():
        if GPIO.pins.get(pins[0]) == GPIO.HIGH:
            wheel_widgets[motor].config(bg="green")
        else:
            wheel_widgets[motor].config(bg="red")

root = tk.Tk()
root.title("Wheel Movement Visualizer")

# Create canvases for wheels
wheel_widgets = {
    "front_left": tk.Canvas(root, bg="red", height=100, width=100),
    "front_right": tk.Canvas(root, bg="red", height=100, width=100),
    "rear_left": tk.Canvas(root, bg="red", height=100, width=100),
    "rear_right": tk.Canvas(root, bg="red", height=100, width=100)
}

wheel_widgets["front_left"].grid(row=0, column=0)
wheel_widgets["rear_left"].grid(row=1, column=0)
wheel_widgets["front_right"].grid(row=0, column=1)
wheel_widgets["rear_right"].grid(row=1, column=1)

# Your movement logic
motor_pins = {
    "front_left": [17, 18],
    "front_right": [22, 23],
    "rear_left": [24, 25],
    "rear_right": [26, 27]
}

for pins in motor_pins.values():
    GPIO.setup(pins[0], GPIO.OUT)
    GPIO.setup(pins[1], GPIO.OUT)

def drive_forward(duration):
    for pins in motor_pins.values():
        GPIO.output(pins[0], GPIO.HIGH)
        GPIO.output(pins[1], GPIO.LOW)
    time.sleep(duration)
    stop()

def rotate(duration):
    GPIO.output(motor_pins["front_left"][1], GPIO.HIGH)
    GPIO.output(motor_pins["rear_left"][1], GPIO.HIGH)
    GPIO.output(motor_pins["front_right"][0], GPIO.HIGH)
    GPIO.output(motor_pins["rear_right"][0], GPIO.HIGH)
    time.sleep(duration)
    stop()

def stop():
    for pins in motor_pins.values():
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.LOW)

def execute_robot_movements():
    time.sleep(1)
    drive_forward(2)
    rotate(1)
    GPIO.cleanup()

# Use threading to run your robot's movements while keeping the GUI responsive
threading.Thread(target=execute_robot_movements).start()

root.mainloop()
