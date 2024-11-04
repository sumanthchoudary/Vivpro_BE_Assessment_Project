# tests/test_routes.py

import pytest
from app import app
from models import db, Song

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_songs.db'
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Add a sample song for testing
            song = Song(
                song_id='test_id',
                title='Test Song',
                danceability=0.5,
                energy=0.5,
                key=5,
                loudness=-5.0,
                mode=1,
                acousticness=0.1,
                instrumentalness=0.0,
                liveness=0.1,
                valence=0.5,
                tempo=120.0,
                duration_ms=180000,
                time_signature=4,
                num_bars=100,
                num_sections=5,
                num_segments=500,
                song_class=1
            )
            db.session.add(song)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_songs(client):
    response = client.get('/songs')
    assert response.status_code == 200
    data = response.get_json()
    assert 'songs' in data
    assert data['total'] >= 1

def test_get_song_by_title(client):
    response = client.get('/songs/title/Test Song')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert data[0]['title'] == 'Test Song'

def test_rate_song(client):
    # Get the song ID
    with app.app_context():
        song = Song.query.filter_by(title='Test Song').first()
        song_id = song.id

    # Submit first rating
    response = client.post(f'/songs/{song_id}/rate', json={'rating': 4})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Rating submitted'
    assert data['average_rating'] == 4.0
    assert data['num_ratings'] == 1

    # Submit second rating
    response = client.post(f'/songs/{song_id}/rate', json={'rating': 5})
    assert response.status_code == 200
    data = response.get_json()
    assert data['average_rating'] == 4.5
    assert data['num_ratings'] == 2
