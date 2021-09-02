import sys
import threading
import requests
import config
from pypresence import Presence

client_id = 882335355733422200
RPC = Presence(client_id)


def connect():
    try:
        RPC.connect()
        print("SUCCESS: RPC Connected")
    except Exception as _:
        print("ERROR: Could not connect to discord. Please Try Again Later")
        sys.exit(1)


def update_presence():
    while True:
        response = requests.get(f"https://lichess.org/api/user/{config.lichess_username}")
        try:
            stat = response.json()
        except ValueError:
            continue

        presence = {
            "large_image": "icon",
            "large_text": config.lichess_username
        }

        if response.status_code == 200:
            if stat["online"]:
                if 'playing' in stat:
                    presence["details"] = "Playing a match"
                    presence["small_image"] = "play"
                    presence["small_text"] = "Playing"
                    presence["buttons"] = [
                        {
                            "label": "Playing on Lichess.org",
                            "url": stat['playing']
                        }
                    ]
                else:
                    presence["details"] = "Idle on Lichess.org"
                    presence["small_image"] = "online"
                    presence["small_text"] = "Idling"
                    presence["buttons"] = [
                        {
                            "label": "Challenge to a game",
                            "url": f"https://lichess.org/?user={config.lichess_username}#friend"
                        }
                    ]
            else:
                presence["details"] = "Offline on Lichess.org"
                presence["buttons"] = [
                    {
                        "label": "Lichess.org Profile",
                        "url": f"https://lichess.org/@/{config.lichess_username}"
                    }
                ]

            RPC.update(**presence)


if __name__ == '__main__':
    connect()
    threading.Timer(5.0, update_presence).start()
