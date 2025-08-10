# file: client_module.py

import requests
import json


def run_client():
    print("Dice roller client (connects to server)")

    server_url = input("Enter server URL (e.g. https://localhost:5000/roll): ").strip()
    if not server_url.endswith("/roll"):
        server_url = server_url.rstrip("/") + "/roll"

    while True:
        player = input("Player name (or 'exit'): ").strip()
        if player.lower() == "exit":
            break

        try:
            num_dice = int(input("Number of dice: "))
            num_sides = int(input("Sides per dice: "))
        except ValueError:
            print("Invalid input, try again.")
            continue

        payload = {
            "player": player,
            "num_dice": num_dice,
            "num_sides": num_sides,
        }

        try:
            resp = requests.post(server_url, json=payload,
                                 verify=False)  # verify=False for self-signed certs; remove in prod
            resp.raise_for_status()
            data = resp.json()
            print("Roll result:", data["result"])
            print("Signature:", data["signature"])
            print(f"Timestamp: {data['timestamp']}")
        except Exception as e:
            print("Error contacting server:", e)
