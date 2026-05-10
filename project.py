import json
import sys
import requests

import database
import api
import search

from rich.panel import Panel
from rich.table import Table
from console import console
from constants import ERROR_MESSAGES


def main():
    connection = database.create_connection()
    database.create_tables(connection)
    database.seed_birds(connection)
    all_bird_names = database.get_bird_names(connection)

    while True:
        try:
            bird_name = search.find_bird(all_bird_names)
            bird = database.find_bird_by_name(connection, bird_name)

            if not database.find_recordings_by_bird_id(connection, bird["id"]):
                api_records = api.fetch_bird_recordings(bird["id"])
                database.insert_recordings(connection, api_records)

            best_recording = database.find_best_recording(connection, bird["id"])
            display_bird(bird, best_recording)

            if not search.confirm_search_again():
                break
        except requests.ConnectionError as err:
            sys.exit(f"{ERROR_MESSAGES["connection_error"]}: {err}")
        except requests.exceptions.RequestException as err:
            sys.exit(f"{ERROR_MESSAGES["http_error"]}: {err}")
        except json.JSONDecodeError:
            sys.exit(ERROR_MESSAGES["json_error"])


def display_bird(bird, best_recording):
    table = Table(show_lines=True, expand=True, show_header=False)

    table.add_column(justify="left", style="cyan")
    table.add_column(justify="left", style="green")

    table.add_row("[bold] About[/bold]", "")
    table.add_row("🦜 Bird name:", f"{bird["name"]}")
    table.add_row("🔍 Scientific name:", f"{bird["sci_name"]}")
    table.add_row("🌍 Region:", f"{", ".join(json.loads(bird["region"]))}")
    table.add_row("📏 Bird size:", f"{bird["length_min"]} - {bird["length_max"]} cm")
    table.add_row("📗 Protection status:", f"{bird["status"]}")

    if best_recording:
        table = add_recording_rows(table, best_recording)

    console.print(Panel(table, title="🕊️ Bird Card"))


def add_recording_rows(table, best_recording):
    table.add_row("[bold] Best Recording[/bold]", "")
    table.add_row("🎵 Audio:", f"{best_recording["file_url"]}")
    table.add_row("🎙 Recorded by:", f"{best_recording["recorder"]}")
    table.add_row("📍 Location:", f"{best_recording["location"]} - {best_recording["country"]}")
    table.add_row("📅 Date:", f"{best_recording["date"]}")
    table.add_row("⌛ Duration:", f"{best_recording["record_length"]}")
    table.add_row("🎶 Voice type:", f"{best_recording["type"].title()}")
    return table


if __name__ == "__main__":
    main()
