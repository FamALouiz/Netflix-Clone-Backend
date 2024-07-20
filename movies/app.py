from flask import request
from flask_restx import Namespace, Resource, fields

from .models import Movie, Genre

movies_ns = Namespace('movies', description='Movies related operations')

movie_ns = Namespace('movie', description='Movie related operations')

movie_model = movie_ns.model('Movie', {
    'id': fields.Integer(readOnly=True, description='The movie unique identifier'),
    'title': fields.String(required=True, description='The movie title'),
    'description': fields.String(required=True, description='The movie description'),
    'video_url': fields.String(required=True, description='The movie video url'),
    'thumbnail_url': fields.String(required=True, description='The movie thumbnail url'),
    'duration_in_minutes': fields.Integer(required=True, description='The movie duration in minutes'),
    'genre': fields.String(required=True, description='The movie genre', attribute='genre.name'),
})

genre_model = movies_ns.model('Genre', {
    'id': fields.Integer(readOnly=True, description='The genre unique identifier'),
    'name': fields.String(required=True, description='The genre name')
})

@movies_ns.route('/')
class MoviesResource(Resource):
    
    @movies_ns.marshal_list_with(movie_model)
    def get(self):
        return Movie.query.all(), 200
    
    @movies_ns.expect(movie_model, validate=True)
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
    
@movies_ns.route('/genres/')
class GenresResource(Resource): 
        
        @movies_ns.marshal_list_with(genre_model)
        def get(self): 
            genres = Genre.query.all()
            return genres, 200
        
        @movies_ns.expect(genre_model, validate=True)
        @movies_ns.marshal_with(genre_model)
        def post(self): 
            data = request.get_json()
            genre_name = data['name']
            
            try: 
                genre = Genre(name=genre_name)
                genre.save()
                
                return genre, 201
            except Exception as e: 
                return {'message': str(e)}, 404

@movies_ns.route('/genre/<int:id>')    
class GenreResource(Resource): 
    
    @movies_ns.marshal_with(genre_model)
    def get(self, id): 
        genre = Genre.query.get_or_404(id)
        return genre, 200
    
@movie_ns.route('/<int:id>')
class MovieResource(Resource): 
    
    @movie_ns.marshal_with(movie_model)
    def get(self, id): 
        movie = Movie.query.get_or_404(id)
        return movie, 200
    
    

