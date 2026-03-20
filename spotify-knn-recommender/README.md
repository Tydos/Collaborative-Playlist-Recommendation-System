# Spotify Song Recommendation System

This project implements a song recommendation system using the K-Nearest Neighbors (KNN) algorithm. The system is designed to recommend songs based on user preferences and historical data from Spotify playlists.

## Project Structure

```
spotify-knn-recommender
├── data
│   └── README.md
├── notebooks
│   └── knn.ipynb
├── src
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocess.py
│   ├── knn_model.py
│   ├── recommend.py
│   └── evaluate.py
├── tests
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_preprocess.py
│   ├── test_knn_model.py
│   ├── test_recommend.py
│   └── test_evaluate.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd spotify-knn-recommender
pip install -r requirements.txt
```

## Usage

1. **Data Loading**: Use the `data_loader.py` module to load the dataset from the specified source.
2. **Preprocessing**: The `preprocess.py` module contains functions to clean and prepare the data for modeling.
3. **Model Training**: The KNN model is implemented in `knn_model.py`. Train the model using the preprocessed data.
4. **Recommendation**: Use the `recommend.py` module to generate song recommendations based on user input.
5. **Evaluation**: Evaluate the model's performance using the functions in `evaluate.py`.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.