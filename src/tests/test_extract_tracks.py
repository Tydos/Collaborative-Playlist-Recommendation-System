import json
import pandas as pd
import pytest
from src.extract_tracks import extract_tracks

def make_test_json(path, playlists):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'playlists': playlists}, f)

def test_extract_tracks_basic(tmp_path):
    # Prepare test data
    playlists = [
        {
            'num_followers': 42,
            'tracks': [
                {
                    'track_uri': 'spotify:track:123',
                    'artist_name': 'Artist1',
                    'track_name': 'Track1',
                    'album_name': 'Album1',
                    'album_uri': 'spotify:album:abc'
                },
                {
                    'track_uri': 'spotify:track:456',
                    'artist_name': 'Artist2',
                    'track_name': 'Track2',
                    'album_name': 'Album2',
                    'album_uri': 'spotify:album:def'
                }
            ]
        }
    ]
    json_path = tmp_path / 'test.json'
    make_test_json(json_path, playlists)
    csv_path = tmp_path / 'out.csv'
    # Run extraction
    assert extract_tracks(str(json_path), str(csv_path))
    # Check output
    df = pd.read_csv(
        csv_path,
        keep_default_na=False,
        dtype={"track_uri": "string", "album_uri": "string"},
    )
    assert list(df.columns) == [
        'playlist_id', 'track_uri', 'num_followers', 'artist_name', 'track_name', 'album_name', 'album_uri'
    ]
    assert df.shape[0] == 2
    assert df.iloc[0]['track_uri'] == 'spotify:track:123'
    assert df.iloc[0]['artist_name'] == 'Artist1'
    assert df.iloc[0]['album_uri'] == 'spotify:album:abc'
    assert df.iloc[1]['track_name'] == 'Track2'
    assert df.iloc[1]['num_followers'] == 42

def test_extract_tracks_missing_fields(tmp_path):
    playlists = [
        {
            'num_followers': 0,
            'tracks': [
                {'track_uri': 'spotify:track:789'}
            ]
        }
    ]
    json_path = tmp_path / 'test2.json'
    make_test_json(json_path, playlists)
    csv_path = tmp_path / 'out2.csv'
    assert extract_tracks(str(json_path), str(csv_path))
    df = pd.read_csv(
        csv_path,
        keep_default_na=False,
        dtype={"track_uri": "string", "album_uri": "string"},
    )
    assert df.iloc[0]['artist_name'] == ''
    assert df.iloc[0]['album_name'] == ''
    assert df.iloc[0]['track_uri'] == 'spotify:track:789'

def test_extract_tracks_file_not_found(tmp_path):
    with pytest.raises(Exception):
        extract_tracks(str(tmp_path / 'doesnotexist.json'), str(tmp_path / 'out3.csv'))
