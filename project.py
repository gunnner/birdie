import json
import sys

import requests

import api
import bird_card
import bird_song
import database
import photos
import search
from constants import ERROR_MESSAGES


def main():
    connection = setup_db()
    all_bird_names = fetch_bird_names(connection)

    while True:
        try:
            bird = load_bird(connection, all_bird_names)
            best_recording = load_best_recording(connection, bird)
            display_bird(bird, best_recording)

            if not search.confirm_search_again():
                break
        except requests.ConnectionError as err:
            sys.exit(f"{ERROR_MESSAGES["connection_error"]}: {err}")
        except requests.exceptions.RequestException as err:
            sys.exit(f"{ERROR_MESSAGES["http_error"]}: {err}")
        except json.JSONDecodeError:
            sys.exit(ERROR_MESSAGES["json_error"])


def setup_db():
    connection = database.create_connection()
    database.create_tables(connection)
    database.seed_birds(connection)
    return connection


def fetch_bird_names(connection):
    return database.get_bird_names(connection)


def load_bird(connection, all_bird_names):
    bird_name = search.find_bird(all_bird_names)
    return database.find_bird_by_name(connection, bird_name)


def load_best_recording(connection, bird):
    if not database.find_recordings_by_bird_id(connection, bird["id"]):
        api_records = api.fetch_bird_recordings(bird["id"])
        database.insert_recordings(connection, api_records)

    return database.find_best_recording(connection, bird["id"])


def display_bird(bird, best_recording):
    bird_song.play_birdsong(best_recording)
    photos.display_photos(bird)
    bird_card.display_bird_card(bird, best_recording)


if __name__ == "__main__":
    main()
