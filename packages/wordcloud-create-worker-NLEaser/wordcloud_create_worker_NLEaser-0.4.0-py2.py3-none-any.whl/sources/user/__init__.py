from werkzeug.security import generate_password_hash
from models.user import UserModel


def create_new_user(email, name, password):
    new_user = UserModel(
        email=email,
        name=name,
        password=generate_password_hash(password)
    )
    new_user.save()
    return new_user
