import json
import sqlite3
from typing import Optional

from rich.panel import Panel
from rich.table import Table

from console import console


def display_bird_card(bird: sqlite3.Row, best_recording: Optional[sqlite3.Row]) -> None:
    bird_dict = dict(bird)
    urls = retrieve_urls(bird_dict)

    table = Table(show_lines=True, expand=True, show_header=False)

    table.add_column(justify="left", style="cyan")
    table.add_column(justify="left", style="green")

    table.add_row("[bold] About[/bold]", "")
    add_row_if_present(table, "🦜 Bird name:", bird_dict["name"])
    add_row_if_present(table, "📸 Photos (click to open in browser):", urls)
    add_row_if_present(table, "🔍 Scientific name:", bird_dict["sci_name"])
    add_row_if_present(table, "🌍 Region:", format_region(bird_dict["region"]))
    add_row_if_present(table, "📏 Bird size:", bird_size(bird_dict))
    add_row_if_present(table, "📗 Protection status:", bird_dict["status"])

    table = add_recording_rows(table, best_recording)

    console.print(Panel(table, title="🕊️ Bird Card"))


def retrieve_urls(bird: dict) -> str:
    image_urls = json.loads(bird["images"])
    urls = " | ".join(
        f"[blue][link={url}]Image: {i}[/link][/blue]"
        for i, url in enumerate(image_urls, 1)
    )
    return urls


def format_region(region: str) -> str:
    return f"{", ".join(json.loads(region))}"


def add_row_if_present(table: Table, label: str, value: Optional[str]) -> None:
    if value:
        return table.add_row(label, value)


def bird_size(bird: dict) -> Optional[str]:
    return f"{bird["length_min"]} - {bird["length_max"]} cm"


def add_recording_rows(table: Table, best_recording: Optional[sqlite3.Row]) -> Table:
    if not best_recording:
        return table

    table.add_row("[bold] Best Recording[/bold]", "")
    table.add_row("🎙 Recorded by:", best_recording["recorder"])
    table.add_row("📍 Location:", f"{best_recording["location"]} - {best_recording["country"]}")
    table.add_row("📅 Date:", best_recording["date"])
    table.add_row("⌛ Duration:", best_recording["record_length"])
    table.add_row("🎶 Voice type:", best_recording["type"].title())
    return table
