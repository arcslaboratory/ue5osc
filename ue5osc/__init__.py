from pythonosc import udp_client
from time import sleep
from ue5osc.osc_dispatcher import OSCMessageReceiver
from pythonosc.osc_server import BlockingOSCUDPServer
from PIL import Image
import threading

import matplotlib.pyplot as plt


class Communicator:
    """Handles interaction between the UE5 environment and the a program."""

    def __init__(self, ip: str, client_port: int, server_port: int, directory: str):
        "Initialize OSC server"
        self.path = directory
        self.imgnumber = 0
        self.file_path = self.path + "/Image_" + str(self.imgnumber)

        self.location_handler = OSCMessageReceiver()
        self.client = udp_client.SimpleUDPClient(ip, client_port)
        self.server = BlockingOSCUDPServer(
            (ip, server_port), self.location_handler.dispatcher
        )

    def start_server(self):
        self.server.serve_forever()

    def get_project_name(self):
        """Returns the name of the current connected project."""
        self.client.send_message("/get/project", 0.0)
        self.location_handler.wait()
        name = self.location_handler.values
        self.location_handler.values = None
        return name

    def get_player_location(self, pawn: int = 0) -> list[float, float, float]:
        """Returns x, y, z location of the player in the Unreal Environment."""
        self.client.send_message("/get/location", 0.0)
        self.location_handler.wait()
        x, y, z = self.location_handler.values
        self.location_handler.values = None
        return float(x), float(y), float(z)

    def set_player_location(self, x: float, y: float, z: float, pawn: int = 0):
        """Sets X, Y, and Z values of an Unreal Camera."""
        self.client.send_message("/set/location", [x, y, z])

    def get_player_rotation(self, pawn: int = 0) -> list[float, float, float]:
        """Returns pitch, yaw, and roll."""
        self.client.send_message("/get/rotation", 0.0)
        self.location_handler.wait()
        roll, pitch, yaw = self.location_handler.values
        self.location_handler.values = None
        return float(roll), float(pitch), float(yaw)

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
        """Move Robot forwards."""
        self.client.send_message("/move/forward", float(amount))

    def turn_left(self, degree: float):
        """turn Robot left."""
        self.client.send_message("/turn/left", float(degree))

    def turn_right(self, degree: float):
        """turn Robot right."""
        self.client.send_message("/turn/right", float(degree))

    def move_backward(self, amount: float):
        """move Robot backwards."""
        self.client.send_message("/move/forward", float(-amount))

    def save_image(self, pawn: int = 0) -> None:
        """Screenshot with default name"""
        self.imgnumber += 1
        self.client.send_message("/save/image", self.file_path)
        sleep(1)

    def request_image(self, pawn: int = 0) -> bytes:
        """request image we saved"""
        image = Image.open(self.file_path)
        return image

    def show(self):
        """If matplotlib is being used, show the image taken to the plot"""
        plt.imshow(self.request_image())

    def take_screenshot(self, filename: str):
        """Save a screenshot with a unique name"""
        self.client.send_message("/screenshot", filename)

    def reset_to_start(self):
        """Reset agent to start location using a UE Blueprint command."""
        self.client.send_message("/reset", 0.0)
