from instances import db
from favorites.models import Favorite
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profiles = db.relationship('Profile', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='users', lazy=True)

    def __repr__(self) -> str:
        return f'<User {self.id} {self.email}>'
    
    def save(self) -> None: 
        db.session.add(self)
        db.session.commit()
        
    def delete(self) -> None: 
        db.session.delete(self)
        db.session.commit()
        
    def update(self, email=None, password=None, profile_to_be_added=None, favorite_to_be_added=None) -> None: 
        self.email = email if email is not None else self.email
        self.password = password if password is not None else self.password
        if profile_to_be_added is not None: self.profiles.append(profile_to_be_added) 
        if favorite_to_be_added is not None: 
            movie_ids = [favorite.movie_id for favorite in self.favorites]
            if int(favorite_to_be_added) not in movie_ids:
                new_favorite = Favorite(user_id=self.id, movie_id=favorite_to_be_added)
                new_favorite.save()
                self.favorites.append(new_favorite)
            else:
                Favorite.query.filter_by(user_id=self.id, movie_id=favorite_to_be_added).delete()
                self.favorites = [favorite for favorite in self.favorites if favorite.movie_id != favorite_to_be_added]
                
        db.session.commit()
        
class Profile(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f'<Profile {self.first_name} {self.last_name}>'
    
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
        
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    def update(self, first_name=None, last_name=None, user_id=None) -> None:
        self.first_name = first_name if first_name is not None else self.first_name
        self.last_name = last_name if last_name is not None else self.last_name
        self.user_id = user_id if user_id is not None else self.user_id
        db.session.commit()