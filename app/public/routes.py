
from . import public_bp
import funcoes

# Home
@public_bp.route('/')
def home():
    return funcoes.home()

@public_bp.route("/coordenadas", methods=["POST"])
def coordenadas():
    return funcoes.coordenadas()

@public_bp.route("/distancia", methods=["POST"])
def distancia():
    return funcoes.distancia()

@public_bp.route('/shows_proximos')
def shows_proximos():
    return funcoes.shows_proximos()


# Login do Usuário
@public_bp.route('/login', methods=['GET', 'POST'])
def login():
    return funcoes.login()

# Cadastro do Usuário
@public_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    return funcoes.cadastro()

@public_bp.route('/artistas/<id>')
def artista_perfil(id):
    return funcoes.artista_perfil(id)