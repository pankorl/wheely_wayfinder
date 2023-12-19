# mock_RPi.py

import tkinter as tk

class GPIO:

    OUT = "OUT"
    HIGH = True
    LOW = False

    pins_state = {}

    root = tk.Tk()
    root.title("Robot Simulation")

    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    front_left_wheel = canvas.create_oval(50, 50, 150, 150, fill="gray")
    front_right_wheel = canvas.create_oval(250, 50, 350, 150, fill="gray")
    rear_left_wheel = canvas.create_oval(50, 250, 150, 350, fill="gray")
    rear_right_wheel = canvas.create_oval(250, 250, 350, 350, fill="gray")

    @classmethod
    def setup(cls, pin, mode):
        cls.pins_state[pin] = cls.LOW

    @classmethod
    def output(cls, pin, state):
        cls.pins_state[pin] = state
        cls.update_wheels()

    @classmethod
    def update_wheels(cls):
        if cls.pins_state.get(17, False) and not cls.pins_state.get(18, False):  # Forward for front_left
            cls.canvas.itemconfig(cls.front_left_wheel, fill="blue")
        elif not cls.pins_state.get(17, False) and cls.pins_state.get(18, False):  # Backward for front_left
            cls.canvas.itemconfig(cls.front_left_wheel, fill="red")
        else:
            cls.canvas.itemconfig(cls.front_left_wheel, fill="gray")

        if cls.pins_state.get(22, False) and not cls.pins_state.get(23, False):  # Forward for front_right
            cls.canvas.itemconfig(cls.front_right_wheel, fill="blue")
        elif not cls.pins_state.get(22, False) and cls.pins_state.get(23, False):  # Backward for front_right
            cls.canvas.itemconfig(cls.front_right_wheel, fill="red")
        else:
            cls.canvas.itemconfig(cls.front_right_wheel, fill="gray")

        if cls.pins_state.get(24, False) and not cls.pins_state.get(25, False):  # Forward for rear_left
            cls.canvas.itemconfig(cls.rear_left_wheel, fill="blue")
        elif not cls.pins_state.get(24, False) and cls.pins_state.get(25, False):  # Backward for rear_left
            cls.canvas.itemconfig(cls.rear_left_wheel, fill="red")
        else:
            cls.canvas.itemconfig(cls.rear_left_wheel, fill="gray")

        if cls.pins_state.get(26, False) and not cls.pins_state.get(27, False):  # Forward for rear_right
            cls.canvas.itemconfig(cls.rear_right_wheel, fill="blue")
        elif not cls.pins_state.get(26, False) and cls.pins_state.get(27, False):  # Backward for rear_right
            cls.canvas.itemconfig(cls.rear_right_wheel, fill="red")
        else:
            cls.canvas.itemconfig(cls.rear_right_wheel, fill="gray")

        cls.root.update()

    @classmethod
    def cleanup(cls):
        cls.root.destroy()

    @classmethod
    def run_simulation(cls, main_function):
        cls.root.after(1000, main_function)  # Start movements after 1 second
        cls.root.mainloop()