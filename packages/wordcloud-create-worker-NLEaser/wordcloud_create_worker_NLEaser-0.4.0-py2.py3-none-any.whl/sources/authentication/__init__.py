from flask_jwt_extended import create_access_token, get_jwt_identity

from models.user import UserSchema
from sources.authentication.services import authenticate


class AuthenticationService:
    def __init__(self):
        self.schema = UserSchema()

    def authenticate(self, email, password):
        user = authenticate(email, password)
        if user:
            access_token = create_access_token(self.schema.dump(user))
            return access_token

    def get_current_user(self):
        return get_jwt_identity()
