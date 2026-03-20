from sklearn.neighbors import NearestNeighbors
import numpy as np

class KNNModel:
    def __init__(self, n_neighbors=5, metric='cosine'):
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.model = NearestNeighbors(n_neighbors=self.n_neighbors, metric=self.metric, algorithm='brute')

    def fit(self, X):
        self.model.fit(X)

    def predict(self, track_idx):
        distances, indices = self.model.kneighbors(track_idx, n_neighbors=self.n_neighbors)
        return distances, indices

    def recommend(self, track_idx, track_to_idx, idx_to_track):
        distances, neighbors = self.predict(track_idx)
        recommended_tracks = [idx_to_track[idx] for idx in neighbors[0]]
        return recommended_tracks