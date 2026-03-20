def clean_data(data):
    """Cleans the input data by removing duplicates and handling missing values."""
    # Remove duplicates
    data = data.drop_duplicates()
    
    # Handle missing values (example: fill with a placeholder or drop)
    data = data.fillna(method='ffill')  # Forward fill as an example
    
    return data

def transform_data(data):
    """Transforms the input data into a suitable format for the KNN model."""
    # Example transformation: encoding categorical variables
    data['track_uri'] = data['track_uri'].apply(lambda x: x.split(':')[-1])  # Keep only the track ID
    return data

def encode_data(data):
    """Encodes the data into numerical format for model training."""
    # Example encoding: mapping track URIs to integers
    track_to_idx = {track: idx for idx, track in enumerate(data['track_uri'].unique())}
    data['track_idx'] = data['track_uri'].map(track_to_idx)
    
    return data, track_to_idx

def preprocess_data(raw_data):
    """Main function to preprocess the raw data."""
    cleaned_data = clean_data(raw_data)
    transformed_data = transform_data(cleaned_data)
    encoded_data, track_to_idx = encode_data(transformed_data)
    
    return encoded_data, track_to_idx