from sklearn.neighbors import NearestNeighbors
from collections import defaultdict
from src.utils.logging import get_logger

logger = get_logger("knn_utils")

def train_knn(X_items, n_neighbors=5, metric='cosine'):
    logger.info(f"Training KNN model with n_neighbors={n_neighbors}, metric={metric}...")
    knn_model = NearestNeighbors(
        n_neighbors=n_neighbors,
        metric=metric,
        algorithm='brute'
    )
    knn_model.fit(X_items)
    logger.info("KNN model training complete.")
    return knn_model

def recommend_tracks(seed_tracks, X, knn_model, track_to_idx, idx_to_track, track_to_details, top_k=10):
    logger.info(f"Generating recommendations for {len(seed_tracks)} seed tracks...")
    neighbor_scores = defaultdict(float)
    for track_uri in seed_tracks:
        if track_uri not in track_to_idx:
            continue
        track_idx = track_to_idx[track_uri]
        distances, neighbors = knn_model.kneighbors(X.T[track_idx], n_neighbors=top_k + len(seed_tracks))
        neighbors = neighbors[0]
        distances = distances[0]
        for neighbor_idx, distance in zip(neighbors, distances):
            if idx_to_track[neighbor_idx] in seed_tracks:
                continue
            similarity = 1 - distance
            neighbor_scores[neighbor_idx] += similarity
    ranked_neighbors = sorted(neighbor_scores.items(), key=lambda x: x[1], reverse=True)
    top_neighbors = ranked_neighbors[:top_k]
    recommended_tracks = []
    for idx, score in top_neighbors:
        track_uri = idx_to_track[idx]
        track_name, track_artist = track_to_details.get(track_uri, ("Unknown", "Unknown"))
        recommended_tracks.append({
            "track_uri": track_uri,
            "track_name": track_name,
            "track_artist": track_artist,
            "score": score
        })
    logger.info(f"Generated {len(recommended_tracks)} recommendations.")
    return recommended_tracks

