from db import db
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user 
# Modelo de Usuário
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), unique=True)
    password= db.Column(db.String())