from flask_restx import Namespace, Resource, fields
from flask import request
from models import User
from movies.models import Movie

favorites_ns = Namespace('favorites', description='Favorites related operations')

favorite_model = favorites_ns.model('Favorite', {
    'movie_id': fields.Integer(required=True, description='The movie id'),
    'user_id': fields.Integer(required=True, description='The user id')
})

@favorites_ns.route('/<int:user_id>')
class FavoritesResource(Resource):
    
    @favorites_ns.expect(favorite_model)
    def put(self, user_id):        
        movie_id = request.args.get('movieId')
        
        # Check if user is valid
        user = User.query.get_or_404(user_id)
        
        # Check if movie is valid 
        movie = Movie.query.get_or_404(movie_id)
        user.update(favorite_to_be_added=movie_id)
        return None, 200