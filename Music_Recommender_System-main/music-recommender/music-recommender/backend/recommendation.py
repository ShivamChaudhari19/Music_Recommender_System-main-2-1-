import joblib
import numpy as np
import pandas as pd

# Load models and data once when module is imported
knn = joblib.load('knn_model.pkl')
song_names = joblib.load('song_names.pkl')
le_genre = joblib.load('le_genre.pkl')
scaler = joblib.load('scaler.pkl')
# Instead of this line:
# df = pd.read_csv('dataset/music_dataset.csv')

# Use this line (assuming the structure above):
df = pd.read_csv('../dataset/music_dataset.csv') # adjust path if needed

def get_song_features(song_name):
    idx = song_names[song_names['track_name'].str.lower() == song_name.lower()].index
    if len(idx) == 0:
        return None

    features = df.loc[idx[0], ['playlist_genre', 'danceability', 'energy', 'tempo', 'track_popularity']]

    # Encode genre (handle unknown genres safely)
    try:
        genre_encoded = le_genre.transform([features['playlist_genre']])[0]
    except ValueError:
        return None

    feature_vector = np.array([
        genre_encoded,
        features['danceability'],
        features['energy'],
        features['tempo'],
        features['track_popularity']
    ]).reshape(1, -1)

    feature_vector = scaler.transform(feature_vector)
    return feature_vector

def recommend_songs(song_name):
    features = get_song_features(song_name)
    if features is None:
        return []

    distances, indices = knn.kneighbors(features)
    recommended_indices = indices.flatten()[1:]  # exclude the song itself

    recommended_songs = song_names.iloc[recommended_indices]['track_name'].tolist()
    return recommended_songs
