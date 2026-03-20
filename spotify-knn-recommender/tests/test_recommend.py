import pytest
from src.recommend import recommend_tracks

def test_recommend_tracks():
    seed_tracks = ['track1', 'track2']
    X = ...  # Load or create the sparse matrix for testing
    knn_model = ...  # Initialize or load the trained KNN model
    track_to_idx = ...  # Create a mapping from track URI to index
    idx_to_track = ...  # Create a mapping from index to track URI
    track_to_details = ...  # Create a mapping from track URI to (name, artist)

    recommended = recommend_tracks(seed_tracks, X, knn_model, track_to_idx, idx_to_track, track_to_details, top_k=10)

    assert len(recommended) == 10  # Check that 10 recommendations are returned
    assert all('track_uri' in r for r in recommended)  # Ensure each recommendation has a track_uri
    assert all('track_name' in r for r in recommended)  # Ensure each recommendation has a track_name
    assert all('track_artist' in r for r in recommended)  # Ensure each recommendation has a track_artist

    # Additional assertions can be added to check the content of recommendations if needed.