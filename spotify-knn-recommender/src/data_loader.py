import pandas as pd
import json

def load_data(file_path: str) -> pd.DataFrame:
    """Load the dataset from a JSON file and return it as a DataFrame."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data['playlists'])

def extract_tracks(playlists: pd.DataFrame) -> pd.DataFrame:
    """Extract track information from playlists DataFrame."""
    track_data = []
    for _, playlist in playlists.iterrows():
        for track in playlist['tracks']:
            track_data.append({
                'playlist_id': playlist['pid'],
                'track_uri': track['track_uri'],
                'track_name': track['track_name'],
                'artist_name': track['artist_name']
            })
    return pd.DataFrame(track_data)

def save_data(data: pd.DataFrame, output_path: str) -> None:
    """Save the DataFrame to a CSV file."""
    data.to_csv(output_path, index=False)