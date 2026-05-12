import sqlite3

import pytest

import database
import project

BIRD_FIELDS = [
    "family",
    "id",
    "images",
    "length_max",
    "length_min",
    "name",
    "order_name",
    "region",
    "sci_name",
    "status",
]

RECORDING_FIELDS = [
    "bird_id",
    "country",
    "date",
    "file_url",
    "id",
    "latitude",
    "licence",
    "location",
    "longitude",
    "quality",
    "record_length",
    "recorder",
    "remarks",
    "sonogram",
    "time",
    "type",
    "uploaded_date",
    "xeno_canto_url",
]

connection = database.create_connection()


def test_setup_db():
    cursor = connection.cursor()
    bird_cursor = cursor.execute("SELECT EXISTS(SELECT 1 FROM birds)")

    assert isinstance(project.setup_db(), sqlite3.Connection)
    assert bird_cursor.fetchone()[0] == 1

    bird_recording_cursor = cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM bird_recordings)"
    )
    assert bird_recording_cursor.fetchone()[0] == 1


def test_fetch_bird_names():
    assert type(project.fetch_bird_names(connection)) == list
    assert "Acadian Flycatcher" in project.fetch_bird_names(connection)

    for arg in [None, ""]:
        with pytest.raises(AttributeError):
            assert project.fetch_bird_names(arg)

    with pytest.raises(TypeError):
        assert project.fetch_bird_names()


def test_load_bird(mocker):
    all_bird_names = project.fetch_bird_names(connection)
    mocker.patch("search.find_bird", return_value="Snow Goose")
    bird = project.load_bird(connection, all_bird_names)

    assert isinstance(bird, sqlite3.Row)
    assert sorted(bird.keys()) == BIRD_FIELDS
    assert bird["name"] == "Snow Goose"


def test_load_bird_not_found(mocker):
    mocker.patch("search.find_bird", return_value="Nonexistent Bird")
    bird = project.load_bird(connection, [])
    assert bird is None


def test_load_best_recording(mocker):
    all_bird_names = project.fetch_bird_names(connection)
    mocker.patch("search.find_bird", return_value="Snow Goose")
    bird = project.load_bird(connection, all_bird_names)
    recording = project.load_best_recording(connection, bird)

    assert isinstance(recording, sqlite3.Row)
    assert sorted(recording.keys()) == RECORDING_FIELDS
    assert recording["bird_id"] is not None


def test_load_best_recording_not_found(mocker):
    mocker.patch("search.find_bird", return_value="Snow Goose")
    mocker.patch("database.find_recordings_by_bird_id", return_value=[])
    mocker.patch("api.fetch_bird_recordings", return_value=[])
    mocker.patch("database.find_best_recording", return_value=None)

    bird = project.load_bird(connection, ["Snow Goose"])
    recording = project.load_best_recording(connection, bird)
    assert recording is None


def test_display_bird(mocker):
    play = mocker.patch("bird_song.play_birdsong")
    photos = mocker.patch("photos.display_photos")
    card = mocker.patch("bird_card.display_bird_card")

    bird = {"id": 1, "name": "Snow Goose"}
    recording = {"id": "1", "quality": "A"}

    project.display_bird(bird, recording)

    play.assert_called_once_with(recording)
    photos.assert_called_once_with(bird)
    card.assert_called_once_with(bird, recording)
