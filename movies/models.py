from instances import db


# Movie genre model
class Genre(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    movies = db.relationship('Movie', backref='genre', lazy=True)
    
    def __repr__(self) -> str:
        return f'<Genre {self.name}>'
    
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
        
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    def update(self, name=None, movie_to_be_added=None) -> None:
        self.name = name if name is not None else self.name
        self.movies.append(movie_to_be_added) if movie_to_be_added is not None else None
        
        db.session.commit()
        
# Movie model
class Movie(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    video_url = db.Column(db.String(255), nullable=True)
    thumbnail_url = db.Column(db.String(255), nullable=True)
    duration_in_minutes = db.Column(db.Integer(), nullable=True)
    genre_id = db.Column(db.Integer(), db.ForeignKey('genre.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f'<Movie {self.title} {self.year}>'
    
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
        
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    def update(self, title=None, description=None, video_url=None, thumbnail_url=None, duration_in_minutes=None, genre_id=None) -> None:
        self.title = title if title is not None else self.title
        self.description = description if description is not None else self.description
        self.video_url = video_url if video_url is not None else self.video_url
        self.thumbnail_url = thumbnail_url if thumbnail_url is not None else self.thumbnail_url
        self.duration_in_minutes = duration_in_minutes if duration_in_minutes is not None else self.duration_in_minutes
        self.genre_id = genre_id if genre_id is not None else self.genre_id
        
        db.session.commit()