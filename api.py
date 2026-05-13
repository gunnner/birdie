import json
import math

import requests

from constants import BIRD_LIST_URI, BIRD_URI, HEADERS, SUCCESS_STATUS_CODE


def fetch_all_birds() -> list[dict]:
    params = {"page": 1, "pageSize": 25, "hasImg": "true"}
    response = fetch_birds_with_images(params)
    response.raise_for_status()

    data = response.json()
    all_birds = map_birds(data["entities"])

    page_size = data["pageSize"]
    total_entities = data["total"]

    if total_entities > page_size:
        total_pages = math.ceil(total_entities / page_size)

        for page in range(2, total_pages + 1):
            params = {"page": page, "pageSize": 25, "hasImg": "true"}
            response = fetch_birds_with_images(params)
            response.raise_for_status()
            all_birds.extend(map_birds(response.json()["entities"]))

    return all_birds


def map_birds(raw_birds: list[dict]) -> list[dict]:
    results = []

    for bird in raw_birds:
        bird_data = {
            "id":         bird["id"],
            "name":       bird["name"],
            "images":     json.dumps(bird["images"]),
            "length_min": bird.get("lengthMin"),
            "length_max": bird.get("lengthMax"),
            "sci_name":   bird.get("sciName"),
            "family":     bird.get("family"),
            "order_name": bird.get("order"),
            "status":     bird.get("status"),
            "region":     json.dumps(bird.get("region")),
        }

        results.append(bird_data)

    return results


def fetch_birds_with_images(params: dict) -> requests.Response:
    return requests.get(url=BIRD_LIST_URI, params=params, headers=HEADERS, timeout=10)


def fetch_bird_recordings(bird_id: int) -> list[dict]:
    response = requests.get(url=f"{BIRD_URI}{bird_id}", headers=HEADERS, timeout=10)
    response.raise_for_status()

    data = response.json()
    return map_recordings(data["recordings"])


def map_recordings(raw_recordings: list[dict]) -> list[dict]:
    result = []

    for record in raw_recordings:
        records_data = {
            "id":             int(record["id"]),
            "bird_id":        record.get("birdId"),
            "date":           record.get("date"),
            "location":       record.get("loc"),
            "licence":        record.get("lic"),
            "type":           record.get("type"),
            "recorder":       record.get("rec"),
            "remarks":        record.get("rmk"),
            "file_url":       record.get("file"),
            "uploaded_date":  record.get("uploaded"),
            "latitude":       record.get("lat"),
            "longitude":      record.get("lng"),
            "record_length":  record.get("length"),
            "sonogram":       json.dumps(record.get("sono")),
            "xeno_canto_url": record.get("url"),
            "quality":        record.get("q"),
            "time":           record.get("time"),
            "country":        record.get("cnt"),
        }

        result.append(records_data)

    return result
