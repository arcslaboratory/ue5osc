import threading

from pythonosc import udp_client
from pythonosc.osc_server import BlockingOSCUDPServer

from ue5osc.osc_dispatcher import OSCMessageReceiver


class Communicator:
    """This handles interaction between the UE5 environment and a Python script."""

    def __init__(self, ip: str, ue_port: int, py_port: int):
        """Initialize OSC client and server."""
        self.ip = ip
        self.ue_port = ue_port
        self.py_port = py_port

        self.message_handler = OSCMessageReceiver()
        self.server = BlockingOSCUDPServer(
            (self.ip, self.py_port), self.message_handler.dispatcher
        )
        self.client = udp_client.SimpleUDPClient(self.ip, self.ue_port)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close_osc()

    def close_osc(self) -> None:
        """Closes the OSC server and joins the server."""
        self.server.shutdown()
        self.server_thread.join()

    def send_and_await(self, osc_address: str):
        """Sends command and waits for a return value before continuing."""
        dummy_data = 0.0
        self.client.send_message(osc_address, dummy_data)
        return self.message_handler.wait_for_response()

    def get_project_name(self) -> str:
        """Returns and optionally prints the name of the current connected project."""
        return self.send_and_await("/get/project")

    def get_location(self) -> tuple[float, float, float]:
        """Returns x, y, z location of the player in the Unreal Environment."""
        return self.send_and_await("/get/location")

    def set_location(self, x: float, y: float, z: float) -> None:
        """Sets X, Y, and Z values of an Unreal Camera."""
        self.client.send_message("/set/location", [x, y, z])

    def get_rotation(self) -> tuple[float, float, float]:
        """Returns pitch, yaw, and roll."""
        return self.send_and_await("/get/rotation")

    def set_yaw(self, yaw: float) -> None:
        """Set the camera yaw in degrees."""
        ue_roll, ue_pitch, _ = self.get_rotation()
        self.client.send_message("/set/rotation", [ue_pitch, ue_roll, yaw])

    def move_forward(self, amount: float) -> None:
        """Move robot forward."""
        self.client.send_message("/move/forward", float(amount))

    def move_backward(self, amount: float) -> None:
        """Move robot backwards."""
        self.client.send_message("/move/forward", float(-amount))

    def rotate_left(self, degree: float) -> None:
        """Rotate robot left."""
        self.client.send_message("/rotate/left", float(degree))

    def rotate_right(self, degree: float) -> None:
        """Rotate robot right."""
        self.client.send_message("/rotate/right", float(degree))

    def set_resolution(self, resolution: str) -> None:
        """Allows you to set resolution of images in the form of ResXxResY."""
        self.client.send_message("/set/resolution", resolution)

    def save_image(self, filename: str) -> None:
        """Takes screenshot with the default name."""
        # Unreal Engine Needs a forward / to separate folder from the filenames
        filename = "/".join(filename.rsplit("\\", 1))
        self.client.send_message("/save/image", str(filename))

    def console(self, message: str) -> None:
        """Sends Unreal Engine console commands (only works in development mode)."""
        self.client.send_message("/console", message)

    def toggle_camera_view(self) -> None:
        """Toggles the camera between 1st and 3rd person views."""
        dummy = 0.0
        self.client.send_message("/toggle/view", dummy)

    def set_quality(self, graphics_level: int) -> None:
        """Set the graphics quality level from 0 (low) to 4 (high)."""
        self.client.send_message("/set/quality", graphics_level)

    def reset(self) -> None:
        """Reset agent to the start location using a UE Blueprint command."""
        # The python OSC library send_message method always requires a value
        self.client.send_message("/reset", 0.0)
