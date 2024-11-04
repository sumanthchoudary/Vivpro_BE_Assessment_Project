# routes.py

from flask import Blueprint, request, jsonify, abort
from models import db, Song

bp = Blueprint('routes', __name__)

@bp.route('/songs', methods=['GET'])
def get_songs():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    pagination = Song.query.paginate(page=page, per_page=limit, error_out=False)
    songs = [song.to_dict() for song in pagination.items]
    return jsonify({
        'songs': songs,
        'total': pagination.total,
        'pages': pagination.pages,
        'page': pagination.page
    })

@bp.route('/songs/title/<string:title>', methods=['GET'])
def get_song_by_title(title):
    songs = Song.query.filter(Song.title.ilike(f'%{title}%')).all()
    if not songs:
        abort(404, description="Song not found")
    return jsonify([song.to_dict() for song in songs])

@bp.route('/songs/<int:id>/rate', methods=['POST'])
def rate_song(id):
    data = request.get_json()
    if not data or 'rating' not in data:
        abort(400, description="Rating is required")
    rating_value = data.get('rating')
    if not isinstance(rating_value, (int, float)) or not (1 <= rating_value <= 5):
        abort(400, description="Invalid rating value. It must be a number between 1 and 5.")

    song = Song.query.get_or_404(id, description="Song not found")

    # Update total_rating and num_ratings
    song.total_rating += rating_value
    song.num_ratings += 1
    db.session.commit()

    return jsonify({
        'message': 'Rating submitted',
        'average_rating': song.average_rating,
        'num_ratings': song.num_ratings,
        'song': song.to_dict()
    }), 200

@bp.route('/songs/<int:id>', methods=['GET'])
def get_song(id):
    song = Song.query.get_or_404(id, description="Song not found")
    return jsonify(song.to_dict())

# Error Handlers
@bp.errorhandler(400)
def bad_request(error):
    return jsonify({'error': error.description}), 400

@bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': error.description}), 404
