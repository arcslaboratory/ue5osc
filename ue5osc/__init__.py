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

    #float parameters are optional for these two functions
    def take_screenshot(self, degree: float=0.0):
        self.client.send_message("/take/screenshot", float(degree))

    def reset_to_start(self, degree: float=0.):
        self.client.send_message("/return/start", float(degree))