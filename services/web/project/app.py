import os

from flask import g

from . import auth, create_app
from .models import User


app = create_app(os.getenv("CONFIG_TYPE"))


@auth.verify_password
def verify_password(name, password):
    user = User.query.filter_by(name=name).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)
