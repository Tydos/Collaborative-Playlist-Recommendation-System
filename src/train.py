import pandas as pd
import pickle
from src.encode_tracks import encode_tracks, build_matrix
from src.knn_utils import train_knn
from src.utils.logging import get_logger
from src.utils.config import load_config

logger = get_logger("train")

# Load config
config = load_config()
PROCESSED_DATA_PATH = config["processed_data_path"]


# 1. Load processed playlist-track data
logger.info("Loading processed data...")
df = pd.read_csv(PROCESSED_DATA_PATH)
interactions = df.values.tolist()


# 2. Encode tracks and build interaction matrix
logger.info("Encoding tracks and building matrix...")
encoded_interactions, track_to_idx, idx_to_track = encode_tracks(interactions)
X = build_matrix(encoded_interactions, track_to_idx)


# 3. Train KNN model
logger.info("Training KNN model...")
knn_model = train_knn(X.T, n_neighbors=10)


# 4. Save artifacts (using pickle)
artifacts = {
    "knn_model": knn_model,
    "track_to_idx": track_to_idx,
    "idx_to_track": idx_to_track
}
with open("knn_artifacts.pkl", "wb") as f:
    pickle.dump(artifacts, f)
logger.info("Training complete. Artifacts saved to knn_artifacts.pkl.")
