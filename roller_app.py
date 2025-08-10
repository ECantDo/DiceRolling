# file: roller_app.py
import threading

import DiceRollerUI
import client_module
import dice_logic
import argparse

import server_module

VERSION = "1.0.0"


def run_server():
    # Server
    server_module.run_server()
    pass


def run_client():
    # Client
    print("Starting GUI...")
    DiceRollerUI.start_gui()
    print("Closed GUI")
    # gui_thread = threading.Thread(target=DiceRollerUI.start_gui, daemon=True)
    # gui_thread.start()

    # client_module.run_client()
    pass


if __name__ == "__main__":
    print("Starting program...")
    arg_choice = ["server", "client"]

    parser = argparse.ArgumentParser(description="Dice Roller App")
    parser.add_argument("--mode", choices=arg_choice, required=False, help="Run as server or client")

    args = parser.parse_args()

    if args.mode == arg_choice[0]:
        run_server()
    elif args.mode == arg_choice[1]:
        run_client()
    else:
        run_client()
