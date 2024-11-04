# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.String, unique=True)
    title = db.Column(db.String)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    key = db.Column(db.Integer)
    loudness = db.Column(db.Float)
    mode = db.Column(db.Integer)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence = db.Column(db.Float)
    tempo = db.Column(db.Float)
    duration_ms = db.Column(db.Integer)
    time_signature = db.Column(db.Integer)
    num_bars = db.Column(db.Integer)
    num_sections = db.Column(db.Integer)
    num_segments = db.Column(db.Integer)
    song_class = db.Column(db.Integer)

    # New columns for rating system
    total_rating = db.Column(db.Float, default=0)
    num_ratings = db.Column(db.Integer, default=0)

    @property # to call as an attribute 
    def average_rating(self):
        if self.num_ratings == 0:
            return None
        return round(self.total_rating / self.num_ratings, 2)

    def to_dict(self):
        song_dict = {
            'id': self.id,
            'song_id': self.song_id,
            'title': self.title,
            'danceability': self.danceability,
            'energy': self.energy,
            'key': self.key,
            'loudness': self.loudness,
            'mode': self.mode,
            'acousticness': self.acousticness,
            'instrumentalness': self.instrumentalness,
            'liveness': self.liveness,
            'valence': self.valence,
            'tempo': self.tempo,
            'duration_ms': self.duration_ms,
            'time_signature': self.time_signature,
            'num_bars': self.num_bars,
            'num_sections': self.num_sections,
            'num_segments': self.num_segments,
            'class': self.song_class,
            'average_rating': self.average_rating,
            'num_ratings': self.num_ratings
        }
        return song_dict
