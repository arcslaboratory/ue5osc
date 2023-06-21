from pythonosc import udp_client


class OSCSender:
    def __init__(self, ip: str, port: int):
        self.client = udp_client.SimpleUDPClient(ip, port)

    def move_forward(self, amount: float):
        self.client.send_message("/move/forward", float(amount))


    def dummy(self):
        pass


    # Turn right
    # Turn left
    # Take screenshot
    # Reset to beginning
