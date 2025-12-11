from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user  
from flask_sqlalchemy import SQLAlchemy

# Cria a aplicação Flask
app = Flask(__name__)

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
            return 'Usuário ou senha inválidos'
        
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

        # Verifica se as senhas coincidem
        if password != confirmpassword: 
            return 'As senhas não coincidem!'
        
        # Verifica se o usuário já existe
        existing_user = db.session.query(User).filter_by(name=name).first()
        if existing_user:
            return 'Usuário já existe!'
        
        new_user = User(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('home'))

# Logout    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()

# Executa o aplicativo Flask
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)