import json
from pathlib import Path

import pandas as pd

from src.track_etl import extract_tracks, transform_track, load_tracks


def _write_json(path: Path, payload: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f)


def test_extract_tracks_respects_limit_and_fields(tmp_path):
    file_path = tmp_path / "slice.json"
    _write_json(
        file_path,
        {
            "playlists": [
                {
                    "tracks": [
                        {
                            "track_uri": "spotify:track:111",
                            "artist_name": "Artist A",
                            "track_name": "Song A",
                            "album_name": "Album A",
                            "album_uri": "spotify:album:aaa",
                        }
                    ]
                },
                {
                    "tracks": [
                        {
                            "track_uri": "spotify:track:222",
                            "artist_name": "Artist B",
                            "track_name": "Song B",
                            "album_name": "Album B",
                            "album_uri": "spotify:album:bbb",
                        }
                    ]
                },
            ]
        },
    )

    rows = list(extract_tracks(str(file_path), limit=1))
    assert len(rows) == 1
    assert rows[0]["playlist_id"] == 0
    assert rows[0]["track_uri"] == "spotify:track:111"
    assert rows[0]["artist_name"] == "Artist A"
    assert rows[0]["track_name"] == "Song A"
    assert rows[0]["album_name"] == "Album A"
    assert rows[0]["album_uri"] == "spotify:album:aaa"


def test_transform_track_strips_prefixes_and_handles_empty():
    transformed = transform_track(
        {
            "track_uri": "spotify:track:xyz",
            "album_uri": "spotify:album:abc",
            "track_name": "T",
            "album_name": "A",
            "artist_name": "R",
        }
    )

    assert transformed["track_uri"] == "xyz"
    assert transformed["album_uri"] == "abc"

    transformed_empty = transform_track(
        {
            "track_uri": "",
            "album_uri": "",
            "track_name": "",
            "album_name": "",
            "artist_name": "",
        }
    )

    assert transformed_empty["track_uri"] == ""
    assert transformed_empty["album_uri"] == ""


def test_load_tracks_creates_dir_and_writes_parquet(monkeypatch, tmp_path):
    file_path = tmp_path / "slice.json"
    _write_json(
        file_path,
        {
            "playlists": [
                {
                    "tracks": [
                        {
                            "track_uri": "spotify:track:123",
                            "artist_name": "Artist1",
                            "track_name": "Track1",
                            "album_name": "Album1",
                            "album_uri": "spotify:album:abc",
                        },
                        {
                            "track_uri": "spotify:track:456",
                            "artist_name": "Artist2",
                            "track_name": "Track2",
                            "album_name": "Album2",
                            "album_uri": "spotify:album:def",
                        },
                    ]
                }
            ]
        },
    )

    out_dir = tmp_path / "parquet_out"
    captured = {}

    def fake_to_parquet(self, path, index=False):
        captured["path"] = str(path)
        captured["index"] = index
        captured["df"] = self.copy()

    monkeypatch.setattr(pd.DataFrame, "to_parquet", fake_to_parquet)

    count = load_tracks(str(file_path), str(out_dir), limit=None)

    assert count == 2
    assert out_dir.exists()
    assert captured["path"].endswith("slice.parquet")
    assert captured["index"] is False
    assert captured["df"].iloc[0]["track_uri"] == "123"
    assert captured["df"].iloc[0]["album_uri"] == "abc"


def test_load_tracks_returns_zero_when_no_tracks(monkeypatch, tmp_path):
    file_path = tmp_path / "empty_slice.json"
    _write_json(file_path, {"playlists": []})

    out_dir = tmp_path / "out"

    def fail_if_called(*args, **kwargs):
        raise AssertionError("to_parquet should not be called when there are no tracks")

    monkeypatch.setattr(pd.DataFrame, "to_parquet", fail_if_called)

    count = load_tracks(str(file_path), str(out_dir), limit=None)
    assert count == 0
