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
