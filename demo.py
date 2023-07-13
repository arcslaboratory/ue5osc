from argparse import ArgumentParser
from time import sleep

import ue5osc


def main():
    """Argument Parser that verifies that the image path is getting passed in and
    optional ability to set ip and ports."""
    parser = ArgumentParser()
    parser.add_argument("path", type=str, help="Path to folder to store images.")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP Address")
    parser.add_argument("--client_port", type=int, default=7447, help="Client Port")
    parser.add_argument("--server_port", type=int, default=7001, help="Server Port")
    parser.add_argument("--resolution", type=list, help="Set resolution of images.")
    args = parser.parse_args()

    with ue5osc.Communicator(
        args.ip, args.client_port, args.server_port, args.path
    ) as osc_communicator:
        print(osc_communicator.get_location()[0])
        sleep(1)
        print(osc_communicator.get_rotation())
        sleep(1)
        print(osc_communicator.get_project_name())
        sleep(1)


# Calling main function
if __name__ == "__main__":
    main()
