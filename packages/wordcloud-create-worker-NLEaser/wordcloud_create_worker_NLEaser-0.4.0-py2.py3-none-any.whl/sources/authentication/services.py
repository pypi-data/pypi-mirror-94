from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import UserModel

jwt = JWTManager()


def authenticate(email, password):
    user = UserModel.objects(email=email).first()
    if user and check_password_hash(user.password, password):
        return user


def get_current_user(identity):
    user = UserModel.objects(email=identity['email']).first()
    return user


jwt.user_loader_callback_loader(get_current_user)
