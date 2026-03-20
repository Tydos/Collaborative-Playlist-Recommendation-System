import pytest
from src.preprocess import extract_tracks, encode_tracks, build_matrix

def test_extract_tracks():
    jsondata = {
        "playlists": [
            {
                "tracks": [
                    {"track_uri": "spotify:track:1", "track_name": "Track 1", "artist_name": "Artist 1"},
                    {"track_uri": "spotify:track:2", "track_name": "Track 2", "artist_name": "Artist 2"}
                ]
            },
            {
                "tracks": [
                    {"track_uri": "spotify:track:3", "track_name": "Track 3", "artist_name": "Artist 3"}
                ]
            }
        ]
    }
    expected_output = [
        [0, "1"],
        [0, "2"],
        [1, "3"]
    ]
    assert extract_tracks(jsondata) == expected_output

def test_encode_tracks():
    interactions = [
        [0, "1"],
        [0, "2"],
        [1, "3"]
    ]
    encoded_interactions, track_to_idx, idx_to_track = encode_tracks(interactions)
    
    assert len(encoded_interactions) == 3
    assert track_to_idx["1"] == 0
    assert track_to_idx["2"] == 1
    assert track_to_idx["3"] == 2
    assert idx_to_track[0] == "1"
    assert idx_to_track[1] == "2"
    assert idx_to_track[2] == "3"

def test_build_matrix():
    encoded_interactions = [
        (0, 0),
        (0, 1),
        (1, 2)
    ]
    track_to_idx = {"1": 0, "2": 1, "3": 2}
    matrix = build_matrix(encoded_interactions, track_to_idx)
    
    assert matrix.shape == (2, 3)  # 2 playlists, 3 tracks
    assert matrix[0, 0] == 1
    assert matrix[0, 1] == 1
    assert matrix[1, 2] == 1
    assert matrix[1, 0] == 0  # No interaction for track 1 in playlist 1