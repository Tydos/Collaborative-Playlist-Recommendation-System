import json
from typing import Any, List
import logging
from pathlib import Path

def list_file_paths(folder_path: str) -> List[str]:

    csvpaths = []
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Does not exist {folder_path}")
    
    #read all csv files in the path object
    for files in folder.glob("*.json"):
        logging.debug(f"reading {files}")
        csvpaths.append(str(files))

    return csvpaths

def read_json_file(file_path: str) -> Any:
    logging.debug(f"opening {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError as e:
        logging.error(f"error: {e}")
        raise
