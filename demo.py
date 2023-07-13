from argparse import ArgumentParser
from time import sleep

import ue5osc


def main():
    """Argument Parser that verifies that the image path is getting passed in and
    optional ability to set ip and ports."""
    parser = ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP Address")
    parser.add_argument("--ue_port", type=int, default=7447, help="UE server port.")
    parser.add_argument("--py_port", type=int, default=7001, help="Python server port.")

    args = parser.parse_args()

    with ue5osc.Communicator(
        args.ip,
        args.ue_port,
        args.py_port,
    ) as osc_communicator:
        print(osc_communicator.get_location())
        sleep(1)
        print(osc_communicator.get_rotation())
        sleep(1)
        print(osc_communicator.get_project_name())
        sleep(1)


# Calling main function
if __name__ == "__main__":
    main()
