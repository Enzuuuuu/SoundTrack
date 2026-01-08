from flask import render_template, redirect, url_for
from flask_login import current_user
from . import public_bp
from flask import request, flash
from db import db
from models import User
from flask_login import login_user

@public_bp.route('/')
def index():
    return render_template('public/index.html')

# Redirecionar para login público se necessário
@public_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('artist.dashboard'))
    
    if request.method == 'GET':
        return render_template('public/login.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        user = db.session.query(User).filter_by(name=name, password=password).first()
        if not user:
            return render_template('public/login.html', error="Usuário ou senha incorretos!", name=name)
        
        login_user(user)
        return redirect(url_for('artist.dashboard'))

@public_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('artist.dashboard'))
    
    
    
    if request.method == 'GET':
        return render_template('public/cadastro.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        # Verifica se as senhas coincidem
        if password != confirmpassword: 
            return render_template('public/cadastro.html', error="As senhas não coincidem!", name=name)
        
        # Verifica se o usuário já existe
        existing_user = db.session.query(User).filter_by(name=name).first()
        if existing_user:
            return render_template('public/cadastro.html', error='Usuário já existe!', name=name)
        
        # Criação de um novo usuário
        new_user = User(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('artist.dashboard'))
