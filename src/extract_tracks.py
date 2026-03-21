from typing import Any
import os
import pandas as pd
import json
from src.utils.logging import get_logger
from src.utils.config import load_config

logger = get_logger("extract_tracks")
config = load_config()
PROCESSED_DATA_PATH = config.get("processed_data_path", "processed_tracks.csv")
DATASET_PATH = config.get("dataset_path", "dataset/data")

def extract_tracks(file_path: str, processed_data_path: str) -> bool:
    """
    Extracts track and playlist information from the playlists in a JSON file and saves to CSV.
    Extracted columns: playlist_id, track_uri (without 'spotify:track:'), num_followers, artist_name, track_name, album_name, album_uri.
    Returns True if successful, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        playlists = data["playlists"]
    except Exception as e:
        logger.error(f"Failed to read or parse file {file_path}: {e}")
        raise
    
    rows = [
        [
            i,
            track.get("track_uri", ""),
            playlist.get("num_followers", 0),
            track.get("artist_name", ""),
            track.get("track_name", ""),
            track.get("album_name", ""),
            track.get("album_uri", "")
        ]
        for i, playlist in enumerate(playlists[:1000])
        for track in playlist.get("tracks", [])
    ]

    try:
        df = pd.DataFrame(rows, columns=["playlist_id", "track_uri", "num_followers", "artist_name", "track_name", "album_name", "album_uri"])
        # Ensure output directory exists
        output_dir = os.path.dirname(processed_data_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        df.to_csv(processed_data_path, index=False)
        logger.info(f"Saved extracted tracks to {processed_data_path} (rows: {len(df)})")
        return True
    except Exception as e:
        logger.error(f"extract_tracks failed: {e}")
        return False
    
if __name__ == "__main__":
    file_path = f"{DATASET_PATH}/mpd.slice.0-999.json"
    success = extract_tracks(file_path, processed_data_path=PROCESSED_DATA_PATH)
    if success:
        logger.info("Track extraction completed successfully.")
    else:
        logger.error("Track extraction failed.")