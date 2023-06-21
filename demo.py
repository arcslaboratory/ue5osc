from time import sleep

import ue5osc

osc_sender = ue5osc.OSCSender("127.0.0.1", 7447)

for i in range(10):
    osc_sender.move_forward(98.0)
    sleep(0.1)

    