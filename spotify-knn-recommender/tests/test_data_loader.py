import pytest
from src.data_loader import read_data

def test_read_data_valid():
    data = read_data('data/sample_data.json')
    assert data is not None
    assert isinstance(data, dict)  # Assuming the data is loaded as a dictionary

def test_read_data_invalid():
    with pytest.raises(FileNotFoundError):
        read_data('data/non_existent_file.json')

def test_read_data_empty_file():
    data = read_data('data/empty_file.json')
    assert data == {}  # Assuming an empty file returns an empty dictionary

def test_read_data_format():
    data = read_data('data/sample_data.json')
    assert 'playlists' in data  # Check if 'playlists' key exists in the loaded data
    assert isinstance(data['playlists'], list)  # Check if 'playlists' is a list

def test_read_data_content():
    data = read_data('data/sample_data.json')
    assert len(data['playlists']) > 0  # Ensure there is at least one playlist
    assert 'tracks' in data['playlists'][0]  # Check if 'tracks' key exists in the first playlist
    assert isinstance(data['playlists'][0]['tracks'], list)  # Check if 'tracks' is a list in the first playlist