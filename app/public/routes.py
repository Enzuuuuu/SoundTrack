
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

