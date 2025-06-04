from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load models
knn = joblib.load('knn_model.pkl')
song_names = joblib.load('song_names.pkl')
le_genre = joblib.load('le_genre.pkl')
scaler = joblib.load('scaler.pkl')

df = pd.read_csv('music_dataset.csv')

@app.route('/')
def index():
    return "Music Recommendation System Backend"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    song_name = data.get('song')

    idx = song_names[song_names['track_name'].str.lower() == song_name.lower()].index
    if len(idx) == 0:
        return jsonify({'recommendations': []})

    features = df.loc[idx[0], ['playlist_genre', 'danceability', 'energy', 'tempo', 'track_popularity']]
    genre_encoded = le_genre.transform([features['playlist_genre']])[0]

    feature_vector = np.array([
        genre_encoded,
        features['danceability'],
        features['energy'],
        features['tempo'],
        features['track_popularity']
    ]).reshape(1, -1)

    feature_vector = scaler.transform(feature_vector)
    distances, indices = knn.kneighbors(feature_vector)
    recommended_indices = indices.flatten()[1:]

    recommended_songs = song_names.iloc[recommended_indices]['track_name'].tolist()
    return jsonify({'recommendations': recommended_songs})

if __name__ == '__main__':
    app.run(debug=True)
