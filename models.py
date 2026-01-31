from db import db
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user 
from werkzeug.security import generate_password_hash, check_password_hash

# classe para modelo de usuario do flask_login
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(256), nullable=False)
    
    def setpass(self, passw: str):
        self.password = generate_password_hash(passw)

    def getpass(self, passw: str):
        return check_password_hash(self.password, passw)