import logging
from pathlib import Path

def get_logger(name: str = "spotify_recommender") -> logging.Logger:
    """
    Returns a logger instance that logs to both console and a central file in log/.
    Usage: logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        
        # Console handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Central file handler
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "project.log", mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(logging.INFO)
    return logger
