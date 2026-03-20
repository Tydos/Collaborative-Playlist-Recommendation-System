from sklearn.neighbors import NearestNeighbors
import numpy as np
from collections import defaultdict

def train_knn(X_items, n_neighbors=5, metric='cosine'):
    knn_model = NearestNeighbors(
        n_neighbors=n_neighbors,
        metric=metric,
        algorithm='brute'
    )
    knn_model.fit(X_items)
    return knn_model

def recommend_tracks(seed_tracks, X, knn_model, track_to_idx, idx_to_track, track_to_details, top_k=10):
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
    return recommended_tracks

def precision_at_k(recommended, ground_truth, k=10):
    top_k = recommended[:k]
    hits = sum([1 for t in top_k if t in ground_truth])
    return hits / k

def recall_at_k(recommended, ground_truth, k=10):
    top_k = recommended[:k]
    hits = sum([1 for t in top_k if t in ground_truth])
    return hits / len(ground_truth) if len(ground_truth) > 0 else 0.0

def ndcg_at_k(recommended, ground_truth, k=10):
    dcg = 0.0
    for i, t in enumerate(recommended[:k]):
        if t in ground_truth:
            dcg += 1 / np.log2(i + 2)
    ideal_hits = min(len(ground_truth), k)
    idcg = sum([1 / np.log2(i + 2) for i in range(ideal_hits)])
    return dcg / idcg if idcg > 0 else 0.0

def hit_rate_at_k(recommended, ground_truth, k=10):
    top_k = recommended[:k]
    return 1.0 if any(t in ground_truth for t in top_k) else 0.0

def mrr_at_k(recommended, ground_truth, k=10):
    top_k = recommended[:k]
    for i, t in enumerate(top_k):
        if t in ground_truth:
            return 1.0 / (i + 1)
    return 0.0
