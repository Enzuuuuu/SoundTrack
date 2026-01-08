from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user  
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import funcoes

# Cria a aplicação Flask
app = Flask(__name__)
app.secret_key = 'banana'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)
lm = LoginManager()
lm.init_app(app)

# Essa coisa aqui cria banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Função para carregar o usuário
@lm.user_loader
def user_loader(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user

# Modelo de Usuário
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), unique=True)
    password= db.Column(db.String())

# Rota de Login    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = db.session.query(User).filter_by(name=name, password=password).first()
        if not user:
            return render_template('login.html', error="Usuário ou senha incorretos!", name=name)
        
        login_user(user)
        return redirect(url_for('home'))

# Rota de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        session['username'] = name

        # Verifica se as senhas coincidem
        if password != confirmpassword: 
            return render_template('cadastro.html', error="As senhas não coincidem!")
        
        # Verifica se o usuário já existe
        existing_user = db.session.query(User).filter_by(name=name).first()
        if existing_user:
            return render_template('cadastro.html', error='Usuário já existe!', name=name)
        
        # Criação de um novo usuário
        new_user = User(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('home'))
    

# Logout (saindo da conta)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def carregar_shows():
    return funcoes.carregar_shows()

def pesquisar_shows(shows, termo):
    funcoes.pesquisar_shows(shows, termo)

def filtrar_shows_alfabeticamente(shows):
    return sorted(shows, key=lambda x: x['titulo'].lower())


@app.route('/')
def home():
    return funcoes.home()  
    
# Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()



@app.route("/coordenadas", methods=["POST"])
def coordenadas():
    return funcoes.coordenadas()

@app.route("/distancia", methods=["POST"])
def distancia():
    return funcoes.distancia()



def calcular_proximidades(user_location):
    return funcoes.calcular_proximidades(user_location)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)