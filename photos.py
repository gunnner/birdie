import io
import json
import os
import sqlite3
import tempfile
from typing import Any

import requests
from PIL import Image
from term_image.image import from_file  # type: ignore

from console import console


def display_photos(bird: sqlite3.Row) -> None:
    with console.status("[cyan]Loading photos...[/cyan]", spinner="monkey"):
        bird_image_urls = json.loads(bird["images"])
        images = download_images(bird_image_urls)
        merged_image = merge_images(images)

    render_image(merged_image)


def download_images(bird_image_urls: list[str]) -> list[Any]:
    images = []
    for image_url in bird_image_urls:
        response = requests.get(image_url)
        response.raise_for_status()
        binary_file = Image.open(io.BytesIO(response.content))
        images.append(binary_file)
    return images


def merge_images(images: list[Any]) -> Any:
    min_height = min(img.height for img in images)

    resized = []
    for img in images:
        ratio = min_height / img.height
        new_width = int(img.width * ratio)
        resized.append(img.resize((new_width, min_height)))

    total_width = sum(img.width for img in resized)
    merged_image = Image.new("RGB", (total_width, min_height))

    x_offset = 0
    for img in resized:
        merged_image.paste(img, (x_offset, 0))
        x_offset += img.width

    return merged_image


def render_image(merged_image: Any) -> None:
    with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
        merged_image.save(fp, format="JPEG")
        fp.seek(0)
        fp.close()

        image = from_file(fp.name)
        
        try:
            terminal_height = os.get_terminal_size().lines
            image.height = int(terminal_height / 3.2)
            image.draw(pad_height=1)
        except Exception:
            console.print("[green] Could't render image in terminal. Please use links above to view photos in browser.")
