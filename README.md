# Birdie

#### Video Demo: [Birdie](https://youtu.be/8mfqyEqLais)

#### Description

The main idea behind the project is to provide users with information about various birds: their common name, scientific name, conservation status, range, size, photos, song recordings, location, date, and comments from the author of the entry.

All data is taken from the open API <https://nuthatch.lastelm.software/swagger.html>, provided by <https://nuthatch.lastelm.software/>

This is a terminal application that allows users to select data about a specific bird in three ways: randomly, by entering the bird's name, or by browsing the entire list of available birds and selecting a specific one.

## How to Run

1. Clone the repository
2. Create a `.env` file in the root of the project with your API key:
```API_KEY=your_api_key_here```
3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run the application:

```
python project.py
```

You can get a free API key at <https://nuthatch.lastelm.software/>

## Workflow

1. Run the application locally: execute the command `python project.py` in the terminal.

2. Behind the scenes, a connection is established to the SQLite database—birdie.db. If this is the first time the app is launched, two database tables are created—birds and bird_recordings—with their corresponding attributes, and a request is made to the API <https://nuthatch.lastelm.software> (using the requests library), from which all existing bird entities with images are retrieved and inserted into the bird records in the database. If this is not the first time the program is run, no API request is made, since the data already exists in the database. Next, a database query retrieves all bird names and places them in a list.

3. A while loop is initiated, providing the user with a command line interface that offers four options, implemented using the InquirerPy library:

- Select random bird
- Search by name
- Browse all birds
- Exit

The user can make a selection using the arrow keys on the keyboard. The subsequent flow depends on the selection: the first three options all result in displaying a photo, information about a specific bird, and playing the bird's song if available. The last option, Exit, speaks for itself—it exits the program.

3.1 **Select "Random Bird"** — implements the logic for selecting a random bird from the SQLite database by name

3.2 **Search by name** — implements the logic for searching for a bird by name using inquirer.text. As the user begins typing the bird's name, inquirer.text provides a list of matching bird names, and the user can use the arrow keys to quickly select a bird instead of typing the full name. If the user enters an invalid bird name and presses Enter, they will see the message "Please select a bird from the list using the arrow keys" and will be prompted to enter the bird name again.

3.3 **Browse all birds** — implements the logic for displaying the complete list of birds available in the database in alphabetical order, implemented using inquirer.fuzzy

3.4 **Exit** — exits the program

4.After selecting a bird and finding it in the database, a search is performed for the recording with the best sound quality in the bird_recordings table. If there are no recordings for this bird in the database, a request is sent to the API, from which they are retrieved for the corresponding bird and added to bird_recordings. After that, a query is sent to the database to retrieve the recording with the best quality.

5.Next, the logic for playing the bird song recording, displaying photos of the bird, and creating a card with information about the bird begins:

5.1 **Audio playback** is implemented using the playsound3 library. First, a request is sent to the URL containing the bird song recording, and if the response is successful, this response is written in binary format to a tempfile. We then use the playsound function to play this named tempfile. During this process, the user sees the message: 🎶 Now playing bird song... 🐦

5.2 **Photo display** — while the bird's song is playing, the bird's photo is loading. The implementation is as follows: first, using the console from the rich library, the text "Loading photos..." with a spinner. Then the photos are loaded—in a loop, requests are made to the API using the URLs of the photos from the database. If the response is successful, a binary file is created using Image from the PIL library, and each is added to the list. Then calculations are performed to ensure that all photos in the list have the same height. The photos are resized and added to a new list. After that, these photos are stitched together to display them horizontally in a row. Next, similar actions are performed with the tempfile, and then an instance is created from the image file using the term_image.image library. Next, the terminal size is calculated to dynamically scale the photos. Finally, the photos are rendered. If an error occurs, the user sees the message: Couldn't render image in terminal. Please use the links above to view photos in a browser.

5.3 **Bird card** — using rich.panel and rich.table, a bird card is generated with information about the bird and its sighting.

6.After playing the bird's song, displaying the photo, and showing the bird's card, the user is asked: "Search for another bird?". If the user agrees, the entire flow starts over; if not, the program ends.

## Project Structure

| File | Description |
|---|---|
| `project.py` | Main program file — contains `main` and core functions |
| `database.py` | Handles all database operations |
| `api.py` | Handles all API requests |
| `search.py` | CLI search logic using InquirerPy |
| `bird_card.py` | Bird card display logic |
| `bird_song.py` | Bird song playback logic |
| `photos.py` | Bird photo display logic |
| `console.py` | Rich console initialization |
| `constants.py` | Application constants |
| `birdie.db` | SQLite database |
| `requirements.txt` | Project dependencies |

## Run tests

```
pytest test_project.py
```

## Design Decisions

**SQLite DataBase** — SQLite was chosen because the database is minimal (only two tables), requires no server setup, and is built into Python.

**Modular approach** — all implementation logic is moved into separate modules according to functionality. This prevents `project.py` from becoming an unreadable wall of code and makes each module easy to maintain independently.

**playsound3 for audio playback** - `playsound3` is simple and concise for the single task of playing an audio file.

**InquirerPy for CLI** - InquirerPy provides many useful and easy-to-use functions for building interactive terminal interfaces: fuzzy search, select menus, text input with autocomplete, and confirmation prompts — all in a clean and consistent API.

**Environment variable for API key** — the API key is stored in a `.env` file and loaded via `python-dotenv`. This keeps sensitive credentials out of the codebase and prevents accidental exposure if the repository is made public. A `.env.example` file is provided as a template.

**rich over standard print** — the `rich` library replaced Python's built-in `print` throughout the application. This enables colored text, clickable hyperlinks, loading spinners, and formatted tables — all of which significantly improve the terminal user experience.

**term-image for terminal rendering** — chosen to render photos directly in the terminal without opening a browser. The image height is calculated dynamically based on terminal size to prevent rendering errors on smaller windows.

**PIL (Pillow) for photo stitching** — bird profiles contain multiple photos. Rather than displaying them one below another, Pillow is used to stitch them horizontally into a single image, providing a more compact and visually appealing presentation.

**Type hints** — all functions across the project are annotated with type hints
using Python's `typing` module. This improves code readability and allows static analysis with `mypy`.
