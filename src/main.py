from src.read_data import read_json_file, list_file_paths
from .extract_tracks import extract_tracks
import logging
logging.basicConfig(level=logging.DEBUG)

if __name__=="__main__":
    jsonfiles = list_file_paths("dataset/data")
    for jsondata in jsonfiles:
        json_data = read_json_file(jsondata)
        extracted_tracks = extract_tracks(json_data)
