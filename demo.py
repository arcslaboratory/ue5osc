from time import sleep
import threading
from time import sleep
import ue5osc

osc_sender = ue5osc.OSCSender("127.0.0.1", 7447)

# start thread to allow the server to not run indefinitely
server_thread = threading.Thread(target=osc_sender.start_server)
server_thread.start()

for i in range(10):
    osc_sender.move_forward(98.0)
    sleep(0.1)

# Shut down the server and join the server thread
sleep(10)
osc_sender.server.shutdown()
server_thread.join()
print("Closed")
