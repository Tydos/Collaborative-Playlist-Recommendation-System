# Spotify Song Recommendation Project

## Project Description

This project builds a playlist-based song recommendation system using the Spotify Million Playlist Dataset (MPD). The pipeline extracts playlist-track interactions from raw JSON, prepares model-ready data, and supports item-based nearest-neighbor recommendation workflows.

## ETL Pipeline (What Changed and Why)

The initial ETL approach loaded JSON slices into memory and wrote flattened CSV output, which was simple but slow at scale. The current ETL in [src/track_etl.py](src/track_etl.py) uses generators for streaming extraction, applies lightweight track normalization, and writes Parquet outputs for better I/O performance. The pipeline was then parallelized in [src/train.py](src/train.py) using `ProcessPoolExecutor` on MacBook M3 cores, reducing end-to-end ETL time from about 277 seconds to about 50 seconds while processing roughly 6 million tracks across 1 million playlists.

Additionally, using Apache Spark for the ETL step (instead of pandas/ProcessPoolExecutor) saved about 5 more seconds on the same workload

## Dataset Description

The dataset is stored as MPD JSON slices under [dataset/data](dataset/data), with each slice containing approximately 1000 playlists, for example [dataset/data/mpd.slice.0-999.json](dataset/data/mpd.slice.0-999.json). The project primarily uses playlist and track metadata fields such as `pid`, `track_uri`, `track_name`, `artist_name`, `album_name`, and `album_uri`.

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

Cleaning includes safe JSON parsing, field selection, default handling for missing metadata, URI normalization by stripping Spotify prefixes, and Parquet output writing with automatic output-directory creation. The extracted dataset currently contains `playlist_id`, `track_uri`, `artist_name`, `track_name`, `album_name`, and `album_uri`.

## Functions and Their Uses

| Function | File | Purpose |
|---|---|---|
| `extract_tracks(file_path)` | [src/track_etl.py](src/track_etl.py) | Streams track rows from JSON slices. |
| `transform_track(track)` | [src/track_etl.py](src/track_etl.py) | Normalizes fields (for example URI prefixes). |
| `load_tracks(file_path, output_dir)` | [src/track_etl.py](src/track_etl.py) | Writes transformed rows to parquet per slice. |
| `load_config()` | [src/utils/config.py](src/utils/config.py) | Loads project config from [config.yaml](config.yaml). |
| `get_logger(name)` | [src/utils/logging.py](src/utils/logging.py) | Provides centralized logging. |
| `benchmark(func, *args, **kwargs)` | [src/utils/benchmark.py](src/utils/benchmark.py) | Measures ETL/runtime performance. |
| `encode_tracks(interactions)` | [src/encode_tracks.py](src/encode_tracks.py) | Encodes track IDs for model input. |
| `build_matrix(encoded_interactions, track_to_idx)` | [src/encode_tracks.py](src/encode_tracks.py) | Builds sparse interaction matrix. |
| `train_knn(X_items, n_neighbors, metric)` | [src/knn_utils.py](src/knn_utils.py) | Trains item-based KNN model. |
| `recommend_tracks(...)` | [src/knn_utils.py](src/knn_utils.py) | Produces ranked track recommendations. |

## General Code Running Guidelines

Install dependencies:

```bash
pip install -r requirements.txt
```

Run ETL:

```bash
python -m src.track_etl
```

Run benchmark:

```bash
python -m src.utils.benchmark
```

Run parallel ETL orchestration:

```bash
python -m src.train
```

Run inference:

```bash
python -m src.inference
```

Run tests:

```bash
python -m pytest -q
```
