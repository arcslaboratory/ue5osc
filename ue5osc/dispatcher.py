from pythonosc.dispatcher import Dispatcher
from typing import List, Any
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient


class DispatchHandler:
    def __init__(self):
        # Initialize attributes
        self.location_values = None
        self.rotation_values = None
        self.project_name = None
        self.dispatcher = Dispatcher()

        # Define valid commands
        self.commands = ["/location", "/rotation", "/project"]

        # Map commands to the set_filter method
        self.dispatcher.map("/location*", self.set_filter)
        self.dispatcher.map("/rotation*", self.set_filter)
        self.dispatcher.map("/project*", self.set_filter)

    def set_filter(self, address: str, *args: List[Any]) -> None:
        # We expect three float arguments
        if address not in self.commands:
            return

        if address == "/location":
            # Check if the argument is a string
            if type(args[0]) is not str:
                return
            else:
                try:
                    # Split the string argument into three float values
                    location_values = args[0].split(",")
                    x, y, z = map(float, location_values)
                except ValueError:
                    return
            if (
                not len(location_values) == 3
                or type(x) is not float
                or type(y) is not float
                or type(z) is not float
            ):
                return
            value1 = x
            value2 = y
            value3 = z
            print(f"Setting location values: x: {value1}, y: {value2}, z: {value3}")
            self.location_values = [value1, value2, value3]
        elif address == "/rotation":
            # Check if the argument is a string
            if type(args[0]) is not str:
                return
            else:
                try:
                    # Split the string argument into three float values
                    rotation_values = args[0].split(",")
                    pitch, roll, yaw = map(float, rotation_values)
                except ValueError:
                    return
            if (
                not len(rotation_values) == 3
                or type(pitch) is not float
                or type(roll) is not float
                or type(yaw) is not float
            ):
                return
            value1 = pitch
            value2 = roll
            value3 = yaw
            print(
                f"Setting rotation values: pitch: {value1}, roll: {value2}, yaw: {value3}"
            )
            self.rotation_values = [value1, value2, value3]
        elif address == "/project":
            # Check if there is a single string argument
            if not len(args) == 1 or type(args[0]) is not str:
                return
            name = args[0]
            print(f"Scene name: {name}")
            self.project_name = name
