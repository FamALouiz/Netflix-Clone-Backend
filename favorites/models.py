from instances import db

class Favorite(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f'<Favorite {self.id}>'
    
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
        
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    def update(self, user_id=None, movie_id=None) -> None:
        self.user_id = user_id if user_id is not None else self.user_id
        self.movie_id = movie_id if movie_id is not None else self.movie_id
        
        db.session.commit()