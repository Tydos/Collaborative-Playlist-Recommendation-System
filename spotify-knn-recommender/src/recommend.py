import numpy as np
from collections import defaultdict

def recommend_tracks(seed_tracks, X, knn_model, track_to_idx, idx_to_track, track_to_details, top_k=10):
    """
    Recommend tracks given seed track(s) using item-based KNN.

    Args:
        seed_tracks: list of track URIs (seed tracks from a playlist)
        X: sparse playlist x track matrix
        knn_model: trained sklearn NearestNeighbors on X.T (item-based)
        track_to_idx: dict mapping track_uri -> track_idx
        idx_to_track: dict mapping track_idx -> track_uri
        track_to_details: dict mapping track_uri -> (track_name, track_artist)
        top_k: number of tracks to recommend

    Returns:
        recommended_tracks: list of dicts with keys: 'track_uri', 'track_name', 'track_artist'
    """
    # Collect neighbors for all seed tracks
    neighbor_scores = defaultdict(float) 

    for track_uri in seed_tracks:
        if track_uri not in track_to_idx:
            continue  # skip unknown tracks

        track_idx = track_to_idx[track_uri]

        distances, neighbors = knn_model.kneighbors(X.T[track_idx], n_neighbors=top_k + len(seed_tracks))

        neighbors = neighbors[0]
        distances = distances[0]

        # Convert distance to similarity (cosine: similarity = 1 - distance)
        for neighbor_idx, distance in zip(neighbors, distances):
            if idx_to_track[neighbor_idx] in seed_tracks:
                continue  # skip seed tracks
            similarity = 1 - distance
            neighbor_scores[neighbor_idx] += similarity

    # Rank neighbors by aggregated similarity
    ranked_neighbors = sorted(neighbor_scores.items(), key=lambda x: x[1], reverse=True)

    # Take top_k
    top_neighbors = ranked_neighbors[:top_k]

    # Decode track info
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

    return recommended_tracks