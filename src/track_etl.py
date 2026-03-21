import json
import os
import pandas as pd
from typing import Generator, Dict, Any, Optional
from src.utils.logging import get_logger

logger = get_logger("track_etl")
def extract_tracks(file_path: str, limit: Optional[int] = None) -> Generator[Dict[str, Any], None, None]:
    logger.info(f"Extracting tracks from: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            playlists = data.get("playlists", [])
            logger.info(f"Loaded {len(playlists)} playlists from {os.path.basename(file_path)}")
    except Exception as e:
        logger.error(f"Failed to parse JSON at {file_path}: {str(e)}")
        return

    for i, playlist in enumerate(playlists):
        if limit is not None and i >= limit:
            break
        for track in playlist.get("tracks", []):
            yield {
                "playlist_id": i,
                "track_uri": track.get("track_uri", ""),
                "artist_name": track.get("artist_name", ""),
                "track_name": track.get("track_name", ""),
                "album_name": track.get("album_name", ""),
                "album_uri": track.get("album_uri", "")
            }

def transform_track(track: Dict[str, Any]) -> Dict[str, Any]:
    track["track_uri"] = track["track_uri"].replace("spotify:track:", "") if track["track_uri"] else ""
    track["album_uri"] = track["album_uri"].replace("spotify:album:", "") if track["album_uri"] else ""
    return track

def load_tracks(file_path: str, output_dir: str, limit: Optional[int] = None) -> int:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Created output directory: {output_dir}")

    tracks_gen = extract_tracks(file_path, limit=limit)
    transformed_tracks = [transform_track(t) for t in tracks_gen]
    
    track_count = len(transformed_tracks)
    if track_count == 0:
        logger.warning(f"No tracks found or extracted from {file_path}")
        return 0

    file_name = os.path.basename(file_path).replace(".json", ".parquet")
    output_path = os.path.join(output_dir, file_name)
    
    try:
        df = pd.DataFrame(transformed_tracks)
        df.to_parquet(output_path, index=False)
        logger.info(f"Successfully saved {track_count} tracks to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save parquet for {file_path}: {str(e)}")
        return 0
    
    return track_count