from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import timedelta

# 1. IMPORTAÇÕES DE ARQUIVOS LOCAIS
from db import db
from models import User
import funcoes

# Importa os Blueprints (certifique-se de que os arquivos existem em app/public e app/artist)
from app.public.routes import public_bp
from app.artist.routes import artist_bp

# Cria a aplicação Flask
app = Flask(__name__)
app.secret_key = 'banana'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)

# 2. CONFIGURAÇÃO DO BANCO DE DADOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados no app (Resolve o RuntimeError)
db.init_app(app)

# 3. CONFIGURAÇÃO DO LOGIN MANAGER
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login' # Define a rota de login padrão

@lm.user_loader
def user_loader(id):
    # .get() é a forma mais eficiente de buscar por ID no SQLAlchemy atual
    return db.session.get(User, int(id))

# 4. REGISTRO DE BLUEPRINTS
# Isso permite que você use subpastas para organizar seu código
app.register_blueprint(public_bp)
app.register_blueprint(artist_bp)

# --- ROTAS PRINCIPAIS ---

@app.route('/')
def home():
    return funcoes.home()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    name = request.form.get('name')
    password = request.form.get('password')

    user = db.session.query(User).filter_by(name=name, password=password).first()
    if not user:
        return render_template('login.html', error="Usuário ou senha incorretos!", name=name)
    
    login_user(user)
    return redirect(url_for('home'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    
    name = request.form.get('name')
    password = request.form.get('password')
    confirmpassword = request.form.get('confirmpassword')

    if password != confirmpassword: 
        return render_template('cadastro.html', error="As senhas não coincidem!")
    
    existing_user = db.session.query(User).filter_by(name=name).first()
    if existing_user:
        return render_template('cadastro.html', error='Usuário já existe!', name=name)
    
    new_user = User(name=name, password=password)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# --- FUNÇÕES AUXILIARES ---

@app.route("/coordenadas", methods=["POST"])
def coordenadas():
    return funcoes.coordenadas()

@app.route("/distancia", methods=["POST"])
def distancia():
    return funcoes.distancia()

# --- INICIALIZAÇÃO ---

if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas do banco de dados automaticamente
        db.create_all()
    app.run(debug=True)