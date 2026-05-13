import sqlite3
import tempfile
from typing import Optional

import requests
from playsound3 import playsound

from console import console


def play_birdsong(recording: Optional[sqlite3.Row]) -> None:
    if not recording:
        return

    response = requests.get(recording["file_url"])
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
        fp.write(response.content)
        fp.seek(0)
        fp.close()
        bird_song = playsound(fp.name, block=False)

        if bird_song.is_alive():
            console.print("🎶 [purple]Now playing bird song... 🐦")
