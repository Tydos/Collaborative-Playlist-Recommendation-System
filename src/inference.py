"""
inference.py: Script to load the trained KNN model and make recommendations for a given playlist or seed tracks.
"""
import pandas as pd
import pickle
from src.knn_utils import recommend_tracks
from src.utils.config import load_config

# Load config
config = load_config()
PROCESSED_DATA_PATH = config["processed_data_path"]

# 1. Load artifacts
with open("knn_artifacts.pkl", "rb") as f:
    artifacts = pickle.load(f)
knn_model = artifacts["knn_model"]
track_to_idx = artifacts["track_to_idx"]
idx_to_track = artifacts["idx_to_track"]

# 2. Load processed data
print("Loading processed data...")
df = pd.read_csv(PROCESSED_DATA_PATH)

# 3. Select a playlist (or accept user input)
sample_playlist_id = df['playlist_id'].iloc[0]
seed_tracks = df[df['playlist_id'] == sample_playlist_id]['track_uri'].tolist()

# Dummy track_to_details for demonstration
track_to_details = {uri: (uri, "Unknown Artist") for uri in track_to_idx.keys()}

# 4. Make recommendations
recommendations = recommend_tracks(seed_tracks, None, knn_model, track_to_idx, idx_to_track, track_to_details, top_k=10)

print(f"Recommendations for playlist {sample_playlist_id}:")
for rec in recommendations:
    print(rec)
