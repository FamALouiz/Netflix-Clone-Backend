from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api

from auth.app import auth_ns
from config import DevConfig
from instances import db
from movies.app import movie_ns, movies_ns
from profiles.app import profile_ns
from favorites.app import favorites_ns

app = Flask(__name__)

app.config.from_object(DevConfig)

CORS(app)

api = Api(app, doc='/doc', title='Netlix Clone API', version='1.0')

# Register namespaces
api.add_namespace(auth_ns)
api.add_namespace(profile_ns)
api.add_namespace(movies_ns)
api.add_namespace(movie_ns)
api.add_namespace(favorites_ns)

with app.app_context() as context: 
    db.init_app(app)
    db.create_all()
    
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=DevConfig.DEBUG)