from flask import request
from flask_restx import Namespace, Resource, fields

from .models import Movie, Genre

movies_ns = Namespace('movies', description='Movies related operations')

movie_ns = Namespace('movie', description='Movie related operations')

movie_model = movie_ns.model('Movie', {
    'title': fields.String(required=True, description='The movie title'),
    'description': fields.String(required=True, description='The movie description'),
    'video_url': fields.String(required=True, description='The movie video url'),
    'thumbnail_url': fields.String(required=True, description='The movie thumbnail url'),
    'duration_in_minutes': fields.Integer(required=True, description='The movie duration in minutes'),
    'genre': fields.String(required=True, description='The movie genre', attribute='genre.name'),
})

@movies_ns.route('/')
class MoviesResource(Resource):
    
    @movies_ns.marshal_list_with(movie_model)
    def get(self):
        return Movie.query.all(), 200
    
    @movies_ns.expect(movie_model)
    @movies_ns.marshal_with(movie_model)
    def post(self):
        data = request.get_json()
        
        title = data['title']
        description = data['description']
        video_url = data['video_url']
        thumbnail_url = data['thumbnail_url']
        duration_in_minutes = data['duration_in_minutes']
        genre_name = data['genre']
        
        try: 
            genre = Genre.query.filter_by(name=genre_name).first()
            movie = Movie(title=title, description=description, video_url=video_url, thumbnail_url=thumbnail_url, duration_in_minutes=duration_in_minutes, genre_id=genre.id)
            movie.save()
            
            return movie, 201
        except Exception as e: 
            return {'message': str(e)}, 404
    
@movie_ns.route('/<int:id>')
class MovieResource(Resource): 
    
    @movie_ns.marshal_with(movie_model)
    def get(self, id): 
        movie = Movie.query.get_or_404(id)
        return movie, 200
    
    

