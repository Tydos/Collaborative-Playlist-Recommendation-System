
## Spotify Collaborative Playlist Recommendation System

Using the Spotify million playlists dataset, the goal is to build a good song recommendation model that can buiid music playlists of the same vibe. 

### Dataset

Spotify Million Playlists [paper](https://dl.acm.org/doi/abs/10.1145/3240323.3240342):

*Ching-Wei Chen, Paul Lamere, Markus Schedl, and Hamed Zamani. Recsys Challenge 2018: Automatic Music Playlist Continuation. In Proceedings of the 12th ACM Conference on Recommender Systems (RecSys ’18), 2018.*


### Preliminary Results

| Metric                  | Value  |
|-------------------------|--------|
| Average Precision@10    | 0.086  |
| Average Recall@10       | 0.861  |
| Average NDCG@10         | 0.836  |
| Average Hit Rate@10     | 0.861  |
| Average MRR@10          | 0.828  |
| Coverage                | 0.191  |

*These results were obtained using a simple K-Nearest Neighbours model on 1000 playlists without any hyperparameter tuning.*

## Code-to-Pipeline Mapping

| Pipeline Step                | Script/Module                        | Description                                      |
|------------------------------|--------------------------------------|--------------------------------------------------|
| Data Ingestion               | src/read_data.py                     | Loads and lists JSON playlist files               |
| Data Extraction              | src/extract_tracks.py                | Extracts (playlist_id, track_uri) pairs           |
| Track Encoding & Matrix      | src/encode_tracks.py                 | Encodes tracks, builds interaction matrix         |
| Model Training (KNN)         | src/knn_utils.py                     | Trains KNN model on item (track) matrix          |
| Recommendation Generation    | src/knn_utils.py                     | Generates recommendations using KNN               |
| Evaluation                   | src/knn_utils.py                     | Computes metrics (Precision@K, Recall@K, etc.)    |
| Pipeline Orchestration       | src/main.py, notebooks/knn.ipynb     | Runs the full workflow, demo and experimentation  |

## Technical Pipeline Overview

1. **Data Ingestion:**
	- Load the Spotify Million Playlist Dataset (MPD) from JSON files. Each file contains 1,000 playlists, with metadata and track lists.

2. **Data Extraction:**
	- Parse each playlist to extract (playlist_id, track_uri) pairs. Store these pairs in a structured format (CSV or Parquet) for efficient downstream processing.

3. **Track Encoding & Matrix Construction:**
	- Assign a unique integer index to each track URI. Construct a sparse playlist-track interaction matrix, where rows represent playlists and columns represent tracks. Each entry is 1 if the playlist contains the track, 0 otherwise.

4. **Model Training (KNN):**
	- Use the item-based (track-based) interaction matrix to fit a K-Nearest Neighbors model (using cosine similarity). This model identifies tracks that frequently co-occur in playlists.

5. **Recommendation Generation:**
	- For a given set of seed tracks (e.g., from a user's playlist), retrieve the nearest neighbors for each seed track using the trained KNN model. Aggregate and rank candidate tracks by similarity score, excluding tracks already present in the seed set.

6. **Evaluation:**
	- Assess recommendation quality using metrics such as Precision@K, Recall@K, NDCG@K, Hit Rate, and MRR, comparing recommended tracks to ground-truth playlist continuations.
