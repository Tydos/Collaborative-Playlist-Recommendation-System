from typing import List, Any
import pandas as pd
import logging
def extract_tracks(jsondata: Any) -> Any:
    
    if "playlists" not in jsondata.keys():
        raise KeyError("Key not found")
    try:
        data = []
        #1000 playlists in one slice
        for i in range(1000):
            logging.debug(f"reading playlist {i}")
            for track in jsondata['playlists'][i]['tracks']:
                data.append([i,track['track_uri'][14:]])
        df = pd.DataFrame(data,columns=["playlist_id","track_uri"])
        df.to_csv("processed_data/playlist_tracks.csv", index=False)
        return data[1]
    
    except Exception as e:
        raise RuntimeError("extract_tracks failed") from e