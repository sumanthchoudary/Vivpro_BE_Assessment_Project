# populate_db.py

from flask import Flask
from models import db, Song
import pandas as pd
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to improve performance by not having tracking 

db.init_app(app)

def populate_database():
    # Load JSON data
    with open('playlist.json', 'r') as file:
        data = json.load(file)

    # Convert JSON data to DataFrame
    df = pd.DataFrame.from_dict(data)

    # Rename 'class' column to 'song_class' to avoid conflict with reserved keyword
    if 'class' in df.columns:
        df.rename(columns={'class': 'song_class'}, inplace=True)

    # Convert numeric columns to appropriate data types
    numeric_columns = [
        'danceability', 'energy', 'key', 'loudness', 'mode', 'acousticness',
        'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms',
        'time_signature', 'num_bars', 'num_sections', 'num_segments', 'song_class'
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            print(f"Warning: Column '{col}' not found in DataFrame.")

    # Create database tables
    with app.app_context():
        db.drop_all()  # Drop existing tables
        db.create_all()  # Create new tables

        # Insert data into the database
        for _, row in df.iterrows():
            song = Song(
                song_id=row.get('id'),
                title=row.get('title'),
                danceability=row.get('danceability'),
                energy=row.get('energy'),
                key=row.get('key'),
                loudness=row.get('loudness'),
                mode=row.get('mode'),
                acousticness=row.get('acousticness'),
                instrumentalness=row.get('instrumentalness'),
                liveness=row.get('liveness'),
                valence=row.get('valence'),
                tempo=row.get('tempo'),
                duration_ms=row.get('duration_ms'),
                time_signature=row.get('time_signature'),
                num_bars=row.get('num_bars'),
                num_sections=row.get('num_sections'),
                num_segments=row.get('num_segments'),
                song_class=row.get('song_class')
            )
            db.session.add(song)

        # Commit the session
        db.session.commit()
        print("Database populated successfully!")

if __name__ == '__main__':
    populate_database()
