
from . import public_bp
import funcoes


# Login do Usuário
@public_bp.route('/login', methods=['GET', 'POST'])
def login():
    return funcoes.login()

# Cadastro do Usuário
@public_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    return funcoes.cadastro()

@public_bp.route('/artistas/<artista>')
def artista_perfil(artista):
    return funcoes.artista_perfil(artista)