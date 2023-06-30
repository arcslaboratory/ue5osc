from time import sleep
import threading
import ue5osc
import sys
from argparse import ArgumentParser


def main():
    # Argument Parser that verifies that the image path is getting passed in
    parser = ArgumentParser()
    parser.add_argument("path", type=str, help="Path to dataset.")
    args = parser.parse_args()

    if args.path:
        print("File path:", args.path)
    else:
        print("No")

    # Setting variables for consol and client"
    ip = "127.0.0.1"
    port = 7447
    osc_sender = ue5osc.OSCSender(ip, port, args.path)

    # start thread to allow the server to not run indefinitely
    server_thread = threading.Thread(target=osc_sender.start_server)
    print(f"Server is Listening to {ip}:7001 ...")
    server_thread.start()

    osc_sender.save_image()
    sleep(2)
    osc_sender.show()

    # Shut down the server and join the server thread
    sleep(4)
    print("Closing the server...")
    sleep(1)
    osc_sender.server.shutdown()
    server_thread.join()
    print("Server Closed")


# Calling main function
if __name__ == "__main__":
    main()
