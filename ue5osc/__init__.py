from pythonosc import udp_client

# import matplotlib.pyplot as plt
from dispatcher import DispatchHandler
from pythonosc.osc_server import BlockingOSCUDPServer


class OSCSender:
    """Handles interaction between the UE5 environment and the a program."""

    def __init__(self, ip: str, port: int):
        self.location_handler = DispatchHandler()
        self.client = udp_client.SimpleUDPClient(ip, port)
        self.server = BlockingOSCUDPServer(
            (ip, port + 1), self.location_handler.dispatcher
        )

    def start_server(self):
        self.server.serve_forever()

    def get_project_name(self):
        """Returns the name of the current connected project."""
        self.client.send_message("/get/project", 0.0)
        name = self.location_handler.project_name
        return name

    def get_camera_location(self, pawn: int = 0) -> tuple[float, float, float]:
        """Returns x, y, z location of a camera in the Unreal Environment."""
        self.client.send_message("/get/location", 0.0)
        location = self.location_handler.location_values
        x, y, z = location
        return float(x), float(y), float(z)

    def set_camera_location(self, x: float, y: float, z: float, pawn: int = 0):
        """Sets X, Y, and Z values of an Unreal Camera."""
        self.client.send_message("/set/location", "{x}, {y}, {z}")

    def get_camera_rotation(self, pawn: int = 0) -> tuple[float, float, float]:
        """Returns pitch, yaw, and roll."""
        self.client.send_message("/get/rotation", 0.0)
        rotation = self.location_handler.rotation_values
        pitch, yaw, roll = rotation
        return float(pitch), float(roll), float(yaw)

    def set_camera_yaw(self, yaw: float, pawn: int = 0):
        """Set the camera yaw in degrees."""
        ue_pitch, ue_roll, _ = self.get_camera_rotation()
        self.client.send_message("/set/rotation", "{ue_pitch}, {ue_roll}, {yaw}")

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

    # TODO: Find a way to request and save images
    # def save_image(self, pawn: int = 0) -> None:
    #     self.client.send_message("/save/image", 0)
    #     sleep(1)

    # def request_image(self, pawn: int = 0) -> bytes:

    # def show(self):
    #     """If matplotlib is being used, show the image taken to the plot"""
    #     plt.imshow(self.request_image())

    def take_screenshot(self, filename: str):
        self.client.send_message("/screenshot", filename)

    def reset_to_start(self):
        """Reset agent to start location using a UE Blueprint command."""
        self.client.send_message("/reset", 0.0)
