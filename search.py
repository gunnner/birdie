import random
import sys
from typing import Optional

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from console import console
from constants import USER_CHOICES


def find_bird(birds: list[str]) -> Optional[str]:
    user_choice = show_main_menu()

    if user_choice is None:
        sys.exit(0)

    if user_choice == USER_CHOICES["by_name"]:
        return search_by_name(birds)
    elif user_choice == USER_CHOICES["all_birds"]:
        return browse_all(birds)
    elif user_choice == USER_CHOICES["random"]:
        return random_bird(birds)
    else:
        raise ValueError(f"Unknown choice: {user_choice}")


def show_main_menu() -> Optional[str]:
    action = inquirer.select(
        message="How would you like to find a bird?",
        choices=[
            USER_CHOICES["random"],
            USER_CHOICES["by_name"],
            USER_CHOICES["all_birds"],
            Choice(value=None, name="Exit"),
        ],
        default=USER_CHOICES["random"],
    ).execute()

    return action


def search_by_name(birds: list[str]) -> str | None:
    completer: dict[str, str | None] = {name: None for name in birds}

    while True:
        bird_name = inquirer.text(
            message="Start typing a bird name:",
            completer=completer,
            multicolumn_complete=True,
            validate=lambda result: len(result) > 1,
            invalid_message="Minimum 2 characters",
        ).execute()

        if bird_name in birds:
            return bird_name

        console.print("[red]Please select a bird from the list using the arrow keys.")


def browse_all(birds: list[str]) -> str:
    action = inquirer.fuzzy(
        message="Browse all birds:",
        choices=sorted(birds),
        max_height="70%",
    ).execute()

    return action


def random_bird(birds: list[str]) -> str:
    return random.choice(birds)


def confirm_search_again() -> bool:
    return inquirer.confirm(message="Search for another bird?", default=True).execute()
