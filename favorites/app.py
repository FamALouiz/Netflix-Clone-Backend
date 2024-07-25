from flask_restx import Namespace, Resource, fields
from flask import request
from models import User
from movies.models import Movie

favorites_ns = Namespace('favorites', description='Favorites related operations')

@favorites_ns.route('/<int:user_id>')
class FavoritesResource(Resource):
    
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {'favorites': [favorite.movie_id for favorite in user.favorites]}
    
    def put(self, user_id):  
        
        movie_id = request.args.get('movieId')
        
        if movie_id is None: 
            return {'message': 'movieId is required'}, 400        
                    
        # Check if user is valid
        user = User.query.get_or_404(user_id)
        
        # Check if movie is valid 
        movie = Movie.query.get(movie_id)

        if movie is None:
            return {'message': 'Invalid movieId'}, 400
        
        user.update(favorite_to_be_added=movie_id)
        
        return {'message': 'Favorites updated'}, 200
