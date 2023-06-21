from pythonosc import udp_client


class OSCSender:
    def __init__(self, ip: str, port: int):
        self.client = udp_client.SimpleUDPClient(ip, port)

    def move_forward(self, amount: float):
        self.client.send_message("/move/forward", float(amount))

    def turn_left(self, degree: float):
        self.client.send_message("/turn/left", float(degree))

    def turn_right(self, degree: float):
        self.client.send_message("/turn/right", float(degree))

    def take_screenshot(self, filename: str):
        self.client.send_message("/screenshot", filename)

    def reset_to_start(self):
        self.client.send_message("/reset")
