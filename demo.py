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

    # Setting variables for server and client"
    ip = "127.0.0.1"
    client_port = 7447
    server_port = 7001

    osc_communicator = ue5osc.Communicator(ip, client_port, server_port, args.path)

    print(osc_communicator.get_player_location()[0])
    sleep(1)
    print(osc_communicator.get_player_rotation())
    sleep(1)
    print(osc_communicator.get_project_name())
    sleep(1)

    sleep(4)
    osc_communicator.close_osc()


# Calling main function
if __name__ == "__main__":
    main()
