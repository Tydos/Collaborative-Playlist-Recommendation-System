import time
import os
from src.utils.logging import get_logger
from src.utils.config import load_config
from src.extract_tracks import extract_tracks  # your main extraction function

logger = get_logger("benchmark")
config = load_config()
PROCESSED_DATA_PATH = config.get("processed_data_path", "processed_tracks.csv")
DATASET_PATH = config.get("dataset_path", "dataset/data")


def benchmark(func, *args, **kwargs):
    """
    Generic benchmark wrapper.
    Returns (success, duration_seconds)
    """
    t0 = time.perf_counter()
    success = func(*args, **kwargs)
    t1 = time.perf_counter()
    return success, t1 - t0


if __name__ == "__main__":
    total_time = 0
    file_count = 0

    for file in os.listdir(DATASET_PATH):
        if file.endswith(".json"):
            file_count += 1
            input_path = os.path.join(DATASET_PATH, file)
            output_path = os.path.join(
                os.path.dirname(PROCESSED_DATA_PATH),
                file.replace(".json", ".csv")
            )
            success, duration = benchmark(extract_tracks, input_path, output_path)
            if success:
                total_time += duration
                logger.info(f"{file} processed in {duration:.3f}s")

    if file_count > 0:
        logger.info(
            f"Processed {file_count} files | "
            f"average time per file = {total_time/file_count:.3f}s"
        )