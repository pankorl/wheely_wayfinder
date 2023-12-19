class GPIO:
    BOARD = "BOARD"
    OUT = "OUT"
    HIGH = "HIGH"
    LOW = "LOW"

    @staticmethod
    def setmode(mode):
        print(f"Setting mode: {mode}")

    @staticmethod
    def setup(pin, mode):
        print(f"Setting up pin {pin} with mode {mode}")

    @staticmethod
    def output(pin, state):
        print(f"Setting pin {pin} to state {state}")

    @staticmethod
    def cleanup():
        print("Cleaning up GPIO pins")
