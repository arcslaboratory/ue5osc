from pathlib import Path
from time import sleep

from PIL import Image
from pythonosc import udp_client
from pythonosc.osc_server import BlockingOSCUDPServer

from ue5osc.osc_dispatcher import OSCMessageReceiver


class Communicator:
    """This handles interaction between the UE5 environment and the a program."""

    def __init__(self, ip: str, client_port: int, server_port: int, directory: str):
        """Initialize OSC client and server."""
        self.path = Path(directory)
        self.img_number = 0

        self.message_handler = OSCMessageReceiver()
        self.client = udp_client.SimpleUDPClient(ip, client_port)
        self.server = BlockingOSCUDPServer(
            (ip, server_port), self.message_handler.dispatcher
        )

    def start_server(self):
        self.server.serve_forever()

    def send_and_wait(self, osc_address: str) -> object:
        """Sends command and waits for a return value before continuing."""
        dummy_data = 0.0
        self.client.send_message(osc_address, dummy_data)
        return self.message_handler.wait_for_response()

    def get_project_name(self, print_val: bool = False):
        """Returns and optionally prints the name of the current connected project."""
        values = self.send_and_wait("/get/project")
        if print_val:
            self.print_values("project", values)
        return values

    def get_player_location(self, print_val: bool = False) -> list[float, float, float]:
        """Returns x, y, z location of the player in the Unreal Environment and optionally prints."""
        values = self.send_and_wait("/get/location")
        if print_val:
            self.print_values("location", values)
        return values

    def set_player_location(self, x: float, y: float, z: float):
        """Sets X, Y, and Z values of an Unreal Camera."""
        self.client.send_message("/set/location", [x, y, z])

    def get_player_rotation(self, print_val: bool = False) -> list[float, float, float]:
        """Returns pitch, yaw, and roll and can optionally print."""
        values = self.send_and_wait("/get/rotation")
        if print_val:
            self.print_values("rotation", values)
        return values

    def set_player_yaw(self, yaw: float, pawn: int = 0):
        """Set the camera yaw in degrees."""
        ue_roll, ue_pitch, _ = self.get_player_rotation()
        self.client.send_message("/set/rotation", [ue_pitch, ue_roll, yaw])

    def __rotate(self, rotation: float, pawn: int = 0):
        """Rotate player a number of degrees."""
        ue_roll, ue_pitch, ue_yaw = self.get_player_rotation()
        yaw = float(ue_yaw) + rotation
        self.client.send_message("/turn/left", yaw)

    def move_forward(self, amount: float):
        """Move robot forward."""
        self.client.send_message("/move/forward", float(amount))

    def turn_left(self, degree: float):
        """Turn robot left."""
        self.client.send_message("/turn/left", float(degree))

    def turn_right(self, degree: float):
        """Turn robot right."""
        self.client.send_message("/turn/right", float(degree))

    def move_backward(self, amount: float):
        """Moverobot backwards."""
        self.client.send_message("/move/forward", float(-amount))

    def save_image(self) -> None:
        """Takes screenshot with the default name"""
        file_path = self.path / f"{self.img_number:06}"
        self.img_number += 1
        self.client.send_message("/save/image", file_path)
        sleep(1)

    def request_image(self) -> bytes:
        """Requests the image we saved."""
        image = Image.open(self.file_path)
        return image

    def show(self):
        """If matplotlib is being used, show the image taken to the plot"""
        import matplotlib.pyplot as plt

        plt.imshow(self.request_image())

    def take_screenshot(self, filename: str):
        """Save a screenshot with a unique name"""
        self.client.send_message("/screenshot", filename)

    def reset_to_start(self):
        """Reset agent to the start location using a UE Blueprint command."""
        self.client.send_message("/reset", 0.0)

    def print_values(self, address: str, values: tuple):
        """Helper Function that allows optional printing of return values."""
        if address == "location":
            print(
                f"Getting location values: x: {values[0]}, y: {values[1]}, z: {values[2]}"
            )
        elif address == "rotation":
            print(
                f"Getting rotation values: roll: {values[0]}, pitch: {values[1]}, yaw: {values[2]}"
            )
        else:
            print(f"Getting project name: {values}")
