from typing import List, Any
import pandas as pd
import logging
import json
import yaml
from pathlib import Path

# Load config
with open(Path(__file__).parent.parent / "config.yaml", "r") as f:
    config = yaml.safe_load(f)
DATASET_PATH = config["dataset_path"]
PROCESSED_DATA_PATH = config["processed_data_path"]

#from the json files, save the playlist and trackid to a dataframe, and return the status
def read_slices(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except Exception as e:
        raise FileNotFoundError(f"Wrong File Path: {e}")
    
def track_gen(jsondata: Any):
    for i in range(1000):
        logging.debug(f"reading playlist {i}")
        for track in jsondata['playlists'][i]['tracks']:
            yield [i, track['track_uri'][14:]]

def extract_tracks(jsondata: Any) -> bool:
    status = False
    if "playlists" not in jsondata.keys():
        raise KeyError("Key not found")
    try:
        df = pd.DataFrame(track_gen(jsondata), columns=["playlist_id", "track_uri"])
        df.to_csv(PROCESSED_DATA_PATH, index=False)
        status = True
        return status
    except Exception as e:
        logging.error(f"extract_tracks failed {e}")
        return status