from pypresence import Presence
import requests, time, config

client_id = 882335355733422200
RPC = Presence(client_id)
try:
    RPC.connect()
    print("SUCCESS: RPC Connected")
except Exception as e:
    print("ERROR: Could not connect to discord. Please Try Again Later")


while True:
    response = requests.get(f"https://lichess.org/api/user/{config.lichess_username}")
    try:
        stat = response.json()
    except:
        pass

    if str(response) == "<Response [200]>":
        if stat["online"]:
            if 'playing' in stat:
                RPC.update(
                    details="Playing a match",
                    large_image="icon",
                    large_text=config.lichess_username,
                    small_image="play",
                    small_text="Playing",
                    buttons =
                    [
                        {
                            "label": "Playing on Lichess.org",
                            "url": stat['playing']
                        }
                    ]
                )
            else:
                RPC.update(
                details="Idle on Lichess.org",
                large_image="icon",
                large_text=config.lichess_username,
                small_image="online",
                small_text="Idling",
                buttons = [
                    {
                        "label": "Challenge to a game",
                        "url": f"https://lichess.org/?user={config.lichess_username}#friend"
                    }
                ]
            )
        if not stat["online"]:
            RPC.update(
                details="Offline on Lichess.org",
                large_image="icon",
                buttons = [
                    {
                        "label": "Lichess.org Profile",
                        "url": f"https://lichess.org/@/{config.lichess_username}"
                    }
                ]
            )

    time.sleep(3)