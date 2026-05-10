import os
import sys

from dotenv import load_dotenv

load_dotenv()


if not os.getenv("API_KEY"):
    sys.exit("API_KEY is not set in .env")

ERROR_MESSAGES = {
    "http_error": "Something went wrong",
    "connection_error": "Connection error",
    "json_error": "Failed to parse JSON.",
}

USER_CHOICES = {
    "by_name": "Search by name",
    "all_birds": "Browse all birds",
    "random": "Select random bird",
}

HEADERS = {
    "accept": "application/json",
    "API-Key": os.getenv("API_KEY"),
}

BIRD_LIST_URI = "https://nuthatch.lastelm.software/v2/birds"
BIRD_URI = "https://nuthatch.lastelm.software/birds/"
SUCCESS_STATUS_CODE = 200
