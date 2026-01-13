from flask import render_template, redirect, url_for
from flask_login import current_user
from . import public_bp
from flask import request, flash
from db import db
from models import User
from flask_login import login_user
import funcoes


#inicialização a partir do público
@public_bp.route('/')
def home():
    return funcoes.home()

# Login do Usuário
@public_bp.route('/login', methods=['GET', 'POST'])
def login():
    return funcoes.login()

# Cadastro do Usuário
@public_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    funcoes.cadastro()


