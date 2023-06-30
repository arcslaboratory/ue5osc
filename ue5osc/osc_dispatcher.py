from pythonosc.dispatcher import Dispatcher
from typing import List, Any
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from time import sleep


class OSCMessageReceiver:
    def __init__(self):
        self.values = None
        self.dispatcher = Dispatcher()

        # Map commands to the set_filter method
        self.dispatcher.map("/location", self.handle_location)
        self.dispatcher.map("/rotation", self.handle_rotation)
        self.dispatcher.map("/project", self.handle_project)
        self.dispatcher.set_default_handler(self.handle_invalid_command)

    def handle_location(self, address: str, *args: List[Any]):
        # Logic to handle location path
        # Split the string argument into three float values
        if address == "/location":
            values = args[0].split(",")
            x, y, z = map(float, values)
            if (
                not len(values) == 3
                or type(x) is not float
                or type(y) is not float
                or type(z) is not float
            ):
                return
            # Assigning location values to x, y, and z
            value1 = x
            value2 = y
            value3 = z
            print(f"Getting location values: x: {value1}, y: {value2}, z: {value3}")
            self.values = [value1, value2, value3]
            return self.values

    def handle_rotation(self, address: str, *args: List[Any]):
        if address == "/rotation":
            values = args[0].split(",")
            roll, pitch, yaw = list(map(float, values))
            if (
                not len(values) == 3
                or type(roll) is not float
                or type(pitch) is not float
                or type(yaw) is not float
            ):
                return
            # Assign rotation values
            value1 = roll
            value2 = pitch
            value3 = yaw
            print(
                f"Getting rotation values: pitch: {value1}, roll: {value2}, yaw: {value3}"
            )
            self.values = [value1, value2, value3]
            return self.values

    def handle_project(self, address: str, *args: List[Any]):
        if address == "/project":
            # Logic to handle project path
            if not len(args) == 1 or type(args[0]) is not str:
                return
            name = args[0]
            print(f"Scene name: {name}")
            self.values = name
            return self.values

    def handle_invalid_command(self, address, *args):
        # Logic to handle invalid commands
        print(f"Invalid command: {address}")
        return None

    def wait(self):
        # Delay between each value returned
        while not self.values:
            sleep(0.01)
