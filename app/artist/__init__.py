from flask import Blueprint

# Cria o blueprint 'admin'
artist_bp = Blueprint('artist', __name__, template_folder='templates')

# Importa as rotas
from . import routes