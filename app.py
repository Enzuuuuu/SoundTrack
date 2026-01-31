
#flask app.py e derivados
from flask import Flask
from flask_login import LoginManager
from datetime import timedelta
from dotenv import load_dotenv
import os
import secrets

#funções e arquivos externos
from db import db
from models import User
import funcoes

# configurações básicas flask
load_dotenv('.env')
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)

# criação do banco de dados do flask_sqlalchemy para login de usuario
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #deixe essa opção desabilitada porquê senão vai consumir mais recursos desnecessariamente
# inicialização do banco de dados
db.init_app(app)

# inicialização do flask login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
# carregamento do usuário
@lm.user_loader
def user_loader(id):
    return db.session.get(User, int(id))

#blueprints
from app.public.routes import public_bp
from app.artist.routes import artist_bp

# registro dos blueprints
app.register_blueprint(public_bp)
app.register_blueprint(artist_bp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)