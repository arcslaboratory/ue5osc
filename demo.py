import threading
from argparse import ArgumentParser
from time import sleep

import ue5osc


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

    osc_communicator = ue5osc.Communicator(ip, client_port, server_port, args.path)

    # Start thread to allow the server to not run indefinitely
    server_thread = threading.Thread(target=osc_communicator.start_server)
    print(f"Server is Listening to {ip}:{server_port} ...")
    server_thread.start()

    # TODO: We print the rotation values
    osc_communicator.get_player_location(True)
    sleep(1)
    osc_communicator.get_player_rotation(True)
    sleep(1)
    osc_communicator.get_project_name(True)
    sleep(1)

    # Shut down the server and join the server thread
    sleep(3)
    print("Closing the server...")
    sleep(1)
    osc_communicator.server.shutdown()
    server_thread.join()
    print("Server Closed")


# Calling main function
if __name__ == "__main__":
    main()
