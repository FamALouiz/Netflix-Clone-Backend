from instances import db

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profiles = db.relationship('Profile', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f'<User {self.email}>'
    
    def save(self) -> None: 
        db.session.add(self)
        db.session.commit()
        
    def delete(self) -> None: 
        db.session.delete(self)
        db.session.commit()
        
    def update(self, email=None, password=None, profile_to_be_added=None) -> None: 
        self.email = email if email is not None else self.email
        self.password = password if password is not None else self.password
        self.profiles.append(profile_to_be_added) if profile_to_be_added is not None else self.profiles
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
        
    def update(self, first_name=None, last_name=None) -> None:
        self.first_name = first_name if first_name is not None else self.first_name
        self.last_name = last_name if last_name is not None else self.last_name
        db.session.commit()