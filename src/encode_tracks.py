from typing import Any, List, Dict, Tuple
import pandas as pd
# Since the track uri's are strings, we need to convert it into a numeric format for feeding into a KNN model
def encode_tracks(interactions: list[str]) -> Tuple[List[Tuple[int,str]],Dict,Dict]:
   
    track_to_idx = {}
    idx_to_track = {}

    track_counter = 0
    encoded_interactions = []

    # Map each track to an integer, and return the new list and maps
    for playlist_id, track_uri in interactions:
        if track_uri not in track_to_idx:
            track_to_idx[track_uri] = track_counter
            idx_to_track[track_counter] = track_uri
            track_counter += 1

        encoded_interactions.append((playlist_id, track_to_idx[track_uri]))
    return encoded_interactions, track_to_idx, idx_to_track

from scipy.sparse import csr_matrix

def build_matrix(encoded_interactions, track_to_idx):
    rows, cols, data = [], [], []
    for p_id, t_idx in encoded_interactions:
        rows.append(p_id)
        cols.append(t_idx)
        data.append(1)
    X = csr_matrix((data, (rows, cols)), shape=(max(rows) + 1, len(track_to_idx)))
    return X

    df = pd.DataFrame(
        data= encoded_interactions,
        columns= ["playlist_id","track_encoded"]
    )

    df.to_csv("processed_data/playlist_encoded.csv", index=False)
    return encoded_interactions, track_to_idx, idx_to_track