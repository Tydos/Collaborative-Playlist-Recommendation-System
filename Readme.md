# Spotify Song Recommendation Project

## Project Description

This project builds a playlist-based song recommender using the Spotify Million Playlist Dataset (MPD).

Current approach:
- extract playlist-track data from raw JSON
- build a playlist-track interaction matrix
- train an item-based KNN model
- generate track recommendations

## Dataset Description

The dataset is the Spotify MPD, stored as many JSON slices in [dataset/data](dataset/data).

Each slice file contains about 1000 playlists, for example:
- [dataset/data/mpd.slice.0-999.json](dataset/data/mpd.slice.0-999.json)

Typical raw fields used by this project:
- playlist-level: `pid`, `num_followers`
- track-level: `track_uri`, `track_name`, `artist_name`, `album_name`, `album_uri`

Example shape (simplified):

```json
{
	"playlists": [
		{
			"pid": 0,
			"num_followers": 1,
			"tracks": [
				{
					"track_uri": "spotify:track:...",
					"track_name": "...",
					"artist_name": "...",
					"album_name": "...",
					"album_uri": "spotify:album:..."
				}
			]
		}
	]
}
```

## Data Cleaning / Preparation

Cleaning and preparation currently includes:
- reading raw JSON safely
- selecting required playlist and track fields
- filling missing optional values with defaults (for example empty strings or `0`)
- writing extracted rows to CSV
- auto-creating output folder when it does not exist

Output columns in extracted CSV:
- `playlist_id`
- `track_uri`
- `num_followers`
- `artist_name`
- `track_name`
- `album_name`
- `album_uri`

## Functions and Their Uses

### Data Extraction
- `extract_tracks(file_path, processed_data_path)` in [src/extract_tracks.py](src/extract_tracks.py)
	- Reads one JSON slice and writes cleaned playlist-track rows to CSV.

### Data Reading Helpers
- `list_file_paths(folder_path)` in [src/read_data.py](src/read_data.py)
	- Lists JSON files in a dataset folder.
- `read_json_file(file_path)` in [src/read_data.py](src/read_data.py)
	- Reads one JSON file.

### Feature Encoding
- `encode_tracks(interactions)` in [src/encode_tracks.py](src/encode_tracks.py)
	- Maps track IDs/URIs to numeric indices.
- `build_matrix(encoded_interactions, track_to_idx)` in [src/encode_tracks.py](src/encode_tracks.py)
	- Builds sparse playlist-track interaction matrix.

### Model Utilities
- `train_knn(X_items, n_neighbors, metric)` in [src/knn_utils.py](src/knn_utils.py)
	- Trains item-based nearest-neighbor model.
- `recommend_tracks(...)` in [src/knn_utils.py](src/knn_utils.py)
	- Generates ranked recommendations from seed tracks.

### Utilities
- `load_config(...)` in [src/utils/config.py](src/utils/config.py)
	- Loads project config from [config.yaml](config.yaml).
- `get_logger(name)` in [src/utils/logging.py](src/utils/logging.py)
	- Standard project logger.
- `benchmark(func, *args, **kwargs)` in [src/utils/benchmark.py](src/utils/benchmark.py)
	- Measures extraction runtime per file.

## General Code Running Guidelines

1. Create and activate virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run extraction (single file default):

```bash
python -m src.extract_tracks
```

4. Run benchmark on all JSON slices:

```bash
python -m src.utils.benchmark
```

5. Train model:

```bash
python -m src.train
```

6. Run inference:

```bash
python -m src.inference
```

7. Run tests:

```bash
python -m pytest -q
```
