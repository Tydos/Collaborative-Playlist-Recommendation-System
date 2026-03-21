import os
from src.utils.logging import get_logger
from src.utils.config import load_config
from src.track_etl import load_tracks
from src.utils.benchmark import benchmark
from concurrent.futures import ProcessPoolExecutor

logger = get_logger("train")
config = load_config()
DATASET_PATH = config.get("dataset_path", "dataset/data")
PROCESSED_DATA_PATH = config.get("processed_data_path", "processed_tracks.parquet")
LIMIT = config.get("limit", 1000)
CHUNK_SIZE = config.get("chunk_size", 100_000)

def run_full_etl():
    """Run the ETL pipeline for all slices."""
    logger.info("Loading processed data...")

    slice_files = [os.path.join(DATASET_PATH, f) for f in os.listdir(DATASET_PATH) if f.endswith(".json")]
    # slice_files = [os.path.join(DATASET_PATH, "mpd.slice.0-999.json")]  # For testing, process only the first slice

    with ProcessPoolExecutor() as executor:
        # Each worker runs: load_tracks(file, save_directory, limit)
        results = list(executor.map(load_tracks, 
                                    slice_files, 
                                    [PROCESSED_DATA_PATH]*len(slice_files), 
                                    [LIMIT]*len(slice_files)))

    logger.info(f"Processed {sum(results)} total tracks across all slices.")
    logger.info("ETL pipeline finished for all slices")

def run_train():
    """Placeholder for training logic."""
    logger.info("Starting training process...")
    pass

if __name__ == "__main__":
    # Benchmark the full ETL pipeline
    success, duration = benchmark(run_full_etl)
    if success:
        logger.info(f"Full ETL pipeline completed successfully in {duration:.2f} seconds")
    else:
        logger.error(f"Full ETL pipeline failed after {duration:.2f} seconds")
