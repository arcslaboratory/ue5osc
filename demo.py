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
    parser.add_argument("--resolution", type=str, default="1280x720", help="Resolution")
    parser.add_argument("--save_image", type=str,  help="Image path")

    args = parser.parse_args()

    with ue5osc.Communicator(
        args.ip,
        args.ue_port,
        args.py_port,
    ) as osc_communicator:
        for i in range(36):
            osc_communicator.set_yaw(i + 1.0)
            sleep(0.1)

        if args.save_image:
            osc_communicator.set_resolution(args.resolution)
            sleep(1)
            osc_communicator.save_image(args.save_image)

    print("Done!")


# Calling main function
if __name__ == "__main__":
    main()
