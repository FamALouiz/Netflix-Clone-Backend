from models import User, Profile
from flask_restx import Namespace, Resource, fields

profile_ns = Namespace('profiles', description='Profile related operations')

profiles_model = profile_ns.model('Profiles', {
    'id': fields.Integer(readOnly=True, description='The profile identifier'),
    'first_name': fields.String(required=True, description='The profile first name'),
    'last_name': fields.String(required=True, description='The profile last name'),
})

@profile_ns.route('/<int:id>')
class GetUserProfilesResource(Resource): 
    
    @profile_ns.marshal_list_with(profiles_model)
    def get(self, id): 
        user = User.query.get_or_404(id)
        return user.profiles

