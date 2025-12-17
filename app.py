from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user  
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from flask import jsonify

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

# Rota para a página inicial
import os
import csv
#carregando os shows do csv
def carregar_shows():
    if not os.path.exists('data/dados.csv'):
        return []
    shows = []
    with open('data/dados.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            shows.append(row)
    return shows

def pesquisar_shows(shows, termo):
    termo = termo.lower()
    resultados = []
    for show in shows:
        if (termo in show['artista'].lower() or
            termo in show['data'].lower() or
            termo in show['local'].lower()):
            resultados.append(show)
    return resultados

def filtrar_shows_alfabeticamente(shows):
    return sorted(shows, key=lambda x: x['titulo'].lower())
@app.route('/')
def home():
    import csv

    with open("data/dados.csv", newline="", encoding="utf-8") as f:
        dist = list(csv.DictReader(f))
    latitudes = []
    longitudes = []
    shows = carregar_shows()
    alfabeto = filtrar_shows_alfabeticamente(shows)
    resultados = pesquisar_shows(shows, request.args.get('pesquisa', ''))
    if resultados:
        shows = resultados
    if alfabeto:
        shows = sorted(shows, key=lambda x: x['titulo'].lower())
    else:
        shows = shows
          
    latitudes = []
    longitudes = []  

    for linha in dist:
        latitudes.append(float(linha["latitude"]))
        longitudes.append(float(linha["longitude"]))  

    return render_template(
    "index.html",
    latitudes=latitudes,
    longitudes=longitudes,
    shows=shows, resultados=resultados, dist=dist, user=current_user
)
    
# Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()



@app.route("/coordenadas", methods=["POST"])
def coordenadas():
    try:

        latitude_str = request.form.get("latitude")
        longitude_str = request.form.get("longitude")

        # Verifica se os dados foram recebidos
        if not latitude_str or not longitude_str:
            return jsonify({"address": "Erro: Dados de latitude/longitude ausentes"}), 400

        # Converte para float antes de usar na biblioteca
        lat = float(latitude_str)
        lon = float(longitude_str)

        geolocator = Nominatim(user_agent="myGeolocator")
        location = geolocator.reverse((lat, lon), language='pt')

        if location:
            address = location.address
        else:
            address = "Endereço não encontrado"

        return jsonify({"address": address})
    except Exception as e:
        return jsonify({"address": f"Erro ao processar a solicitação: {str(e)}"}), 500

@app.route("/distancia", methods=["POST"])
def distancia():
    data = request.get_json()

    user_location = (
        float(data["latitude"]),
        float(data["longitude"])
    )

    proximidades = []

    with open("data/dados.csv", newline="", encoding="utf-8") as f:
        shows = csv.DictReader(f)

        for show in shows:
            show_location = (
                float(show["latitude"]),
                float(show["longitude"])
            )

            distancia_km = geodesic(user_location, show_location).kilometers

            proximidades.append({
                "titulo": show["titulo"],
                "distancia_km": round(distancia_km, 2)
            })

    proximidades.sort(key=lambda x: x["distancia_km"])

    return jsonify(proximidades)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)