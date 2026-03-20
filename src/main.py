
from src.read_data import read_json_file, list_file_paths
from src.extract_tracks import extract_tracks
from src.encode_tracks import encode_tracks

import logging
import yaml
from pathlib import Path
import pandas as pd
from src.read_data import read_json_file, list_file_paths
from src.extract_tracks import extract_tracks
from src.encode_tracks import encode_tracks, build_matrix
from src.knn_utils import train_knn, recommend_tracks
logging.basicConfig(level=logging.DEBUG)

# Load config
with open(Path(__file__).parent.parent / "config.yaml", "r") as f:
    config = yaml.safe_load(f)
DATASET_PATH = config["dataset_path"]
PROCESSED_DATA_PATH = config["processed_data_path"]

def main():
    # 1. Extract tracks from all JSON slices (if not already processed)
    jsonfiles = list_file_paths(DATASET_PATH)
    for jsondata in jsonfiles:
        json_data = read_json_file(jsondata)
        extract_tracks(json_data)

    # 2. Load processed playlist-track data
    df = pd.read_csv(PROCESSED_DATA_PATH)
    interactions = df.values.tolist()

    # 3. Encode tracks and build interaction matrix
    encoded_interactions, track_to_idx, idx_to_track = encode_tracks(interactions)
    X = build_matrix(encoded_interactions, track_to_idx)

    # 4. Train KNN model
    knn_model = train_knn(X.T, n_neighbors=10)

    # 5. Recommend tracks for a sample playlist (first playlist in processed data)
    sample_playlist_id = df['playlist_id'].iloc[0]
    seed_tracks = df[df['playlist_id'] == sample_playlist_id]['track_uri'].tolist()
    # Dummy track_to_details for demonstration
    track_to_details = {uri: (uri, "Unknown Artist") for uri in track_to_idx.keys()}
    recommendations = recommend_tracks(seed_tracks, X, knn_model, track_to_idx, idx_to_track, track_to_details, top_k=10)

    print("Sample recommendations for playlist", sample_playlist_id)
    for rec in recommendations:
        print(rec)

if __name__ == "__main__":
    main()