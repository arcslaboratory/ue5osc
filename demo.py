from time import sleep
import threading
import ue5osc
import sys
from argparse import ArgumentParser


def main():
    # Argument Parser that verifies that the image path is getting passed in
    parser = ArgumentParser()
    parser.add_argument(
        "path", type=str, help="Path to folder in which to store images."
    )
    args = parser.parse_args()

    # Setting variables for consol and client"
    ip = "127.0.0.1"
    client_port = 7447
    server_port = 7001

    osc_sender = ue5osc.Communicator(ip, client_port, server_port, args.path)

    # start thread to allow the server to not run indefinitely
    server_thread = threading.Thread(target=osc_sender.start_server)
    print(f"Server is Listening to {ip}:7001 ...")
    server_thread.start()

    osc_sender.get_player_location()
    sleep(1)
    osc_sender.move_forward(90.0)
    sleep(1)
    osc_sender.set_player_location(34.0, 200.0, 4.0)
    sleep(1)
    osc_sender.set_player_yaw(30.0)
    sleep(1)
    osc_sender.get_player_location()
    sleep(1)
    osc_sender.get_player_rotation

    # Shut down the server and join the server thread
    sleep(13)
    print("Closing the server...")
    sleep(1)
    osc_sender.server.shutdown()
    server_thread.join()
    print("Server Closed")


# Calling main function
if __name__ == "__main__":
    main()
