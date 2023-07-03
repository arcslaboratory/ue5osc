from pathlib import Path
from time import sleep

from PIL import Image
from pythonosc import udp_client
from pythonosc.osc_server import BlockingOSCUDPServer
import threading

from ue5osc.osc_dispatcher import OSCMessageReceiver


class Communicator:
    """This handles interaction between the UE5 environment and the a program."""

    def __init__(self, ip: str, client_port: int, server_port: int, directory: str):
        """Initialize OSC client and server."""
        self.path = Path(directory)
        self.img_number = 0

        self.message_handler = OSCMessageReceiver()
        self.server = BlockingOSCUDPServer(
            (ip, server_port), self.message_handler.dispatcher
        )
        self.client = udp_client.SimpleUDPClient(ip, client_port)

        self.server_thread = threading.Thread(target=self.server.serve_forever)
        print(f"Server is Listening to {ip}:{server_port} ...")
        self.server_thread.start()

    def close_osc(self):
        """Closes the OSC server and joins the server."""
        print("Closing the server...")
        sleep(1)
        self.server.shutdown()
        self.server_thread.join()
        print("Server Closed")

    def send_and_wait(self, osc_address: str) -> object:
        """Sends command and waits for a return value before continuing."""
        dummy_data = 0.0
        self.client.send_message(osc_address, dummy_data)
        return self.message_handler.wait_for_response()

    def get_project_name(self) -> str:
        """Returns and optionally prints the name of the current connected project."""
        return self.send_and_wait("/get/project")

    def get_player_location(self, pawn: int = 0) -> list[float, float, float]:
        """Returns x, y, z location of the player in the Unreal Environment and optionally prints."""
        return self.send_and_wait("/get/location")

    def set_player_location(self, x: float, y: float, z: float, pawn: int = 0):
        """Sets X, Y, and Z values of an Unreal Camera."""
        self.client.send_message("/set/location", [x, y, z])

    def get_player_rotation(self, pawn: int = 0) -> list[float, float, float]:
        """Returns pitch, yaw, and roll and can optionally print."""
        return self.send_and_wait("/get/rotation")

    def set_player_yaw(self, yaw: float, pawn: int = 0):
        """Set the camera yaw in degrees."""
        # Pawn is a variable used to assign what player we will be controlling in the future
        ue_roll, ue_pitch, _ = self.get_player_rotation()
        self.client.send_message("/set/rotation", [ue_pitch, ue_roll, yaw])

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
        self.file_path = self.path / f"{self.img_number:06}"
        self.img_number += 1
        # Unreal Engine Needs a forward / to separate folder from the filenames
        self.client.send_message("/save/image", f"{self.path}/{self.img_number:06}")
        sleep(1.5)

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
        sleep(1)
