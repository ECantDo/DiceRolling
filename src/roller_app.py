# file: roller_app.py
import threading

import script_updater, server_module, DiceRollerUI
import argparse
import queue

import os
import sys

from ServerLogGUI import ServerLogGUI


def run_server():
    # Server
    log_q = queue.Queue()
    gui = ServerLogGUI(log_q)

    server_thread = threading.Thread(target=server_module.run_server, args=(log_q,), daemon=True)
    server_thread.start()

    gui.gui_main()
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


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource located alongside the executable/script.

    Works both in dev (script) and after packaging as an EXE.

    :param relative_path: relative path to resource from the EXE/script folder
    :return: absolute path to resource
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    script_updater.run_update_checker()

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
