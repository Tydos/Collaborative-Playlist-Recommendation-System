
import json
from typing import Any, List
from pathlib import Path
from src.utils.logging import get_logger
from src.utils.config import load_config

logger = get_logger("read_data")

# Load config
config = load_config()
DATASET_PATH = config["dataset_path"]

def list_file_paths(folder_path: str) -> List[str]:

    csvpaths = []
    folder = Path(folder_path) if folder_path else Path(DATASET_PATH)

    if not folder.exists():
        logger.error(f"Does not exist {folder_path}")
        raise FileNotFoundError(f"Does not exist {folder_path}")
    
    #read all csv files in the path object
    for files in folder.glob("*.json"):
        logger.debug(f"reading {files}")
        csvpaths.append(str(files))

    return csvpaths

def read_json_file(file_path: str) -> Any:
    logger.debug(f"opening {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError as e:
        logger.error(f"error: {e}")
        raise

def encode_track_details(jsondata, num_playlists=1000):
    track_to_details = {}
    playlist_tracks = {}
    for i in range(num_playlists):
        playlist_tracks[i] = []
        for track in jsondata['playlists'][i]['tracks']:
            track_uri = track['track_uri'][14:]
            track_name = track['track_name']
            track_artist = track['artist_name']
            playlist_tracks[i].append(track_uri)
            if track_uri not in track_to_details:
                track_to_details[track_uri] = (track_name, track_artist)
    return track_to_details, playlist_tracks

def decode_track_details(track_uri, track_to_details):
    return track_to_details.get(track_uri, (None, None))
