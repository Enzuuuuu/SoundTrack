from flask import  render_template, request, jsonify, redirect, url_for, current_app
from flask_login import  login_user, current_user
from models import User
from geopy.distance import geodesic
from db import db
import os
import csv




# funções base para a home
def home()-> list:
    
    # shows == lista referente a tabela dados.csv
    shows = carregar_csv()

    #Parametros para filtrar --> A tabela contendo todos os shows e o valor da pesquisa
    shows_filtrados =  pesquisar_shows(shows, request.args.get('pesquisa', ''))


    # Pega as linhas referentes as latitudades e longitudes dos shows 
    latitudes = [float(linha["latitude"]) for linha in shows]
    longitudes = [float(linha["longitude"]) for linha in shows]

    #Pega a linha referente a Gêneros
    generos_disponiveis = sorted(list(set(show['genero'] for show in shows_filtrados)))

    #O usuário que esta logado no momento
    user = current_user
    #Diferenciação de página de Logado e não Logado
    if user.is_authenticated:
        return render_template(
            'artist/index.html', 
            shows=shows_filtrados,  
            user=current_user, 
            latitudes=latitudes, 
            longitudes=longitudes,
            generos=generos_disponiveis
        )
    
    else:
        return render_template(
            'public/index.html', 
            shows=shows_filtrados, 
            user=current_user, 
            latitudes=latitudes, 
            longitudes=longitudes,
            generos=generos_disponiveis
        )



def carregar_csv()->list:
    # Função principal da função == Carregar toda a tabela dados.csv e redirecionar para funções adjacentes trabalharem com ela
    # Entrada: "dados.csv"  Saída: Uma lista com todas as informações da tabela csv
    # Primeiro ele abre o aquivo
    try:
        with open( "data/dados.csv", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.read().splitlines()
    except FileNotFoundError:
        linhas = []


    tabela = []
    # Separa cabeçalho 
    if linhas:
        cabecalho = linhas[0].split(',')
        # Show == uma lista contendo um string de tudo
        # Valores == uma lista contendo varias strings a respeito de todos as informações
        for show in linhas[1:]:
            valores = show.split(',')
        #infos == separação de cada uma das informações
            infos = {}
            for i in range(len(cabecalho)):
                if i < len(valores):
                    infos[cabecalho[i]] = valores[i] 
        #tabela == compilação dessas informações
            tabela.append(infos)
    return tabela


def pesquisar_shows(shows:list, termo:str) -> list:
    #Função principal: filtrar a lista de shows, organizando-as ou efetivamente exibindo apenas os shows dentro do escopo de interesse
    # Ao todo são 4 filtros, dois organizacionais ( alfabetico e preço ) e dois filtros de escopo ( barra de pesquisa e Gênero )
    # A saída é uma lista que vai ser usada para a geração das páginas


    #shows == lista completa
    #termo == barra de pesquisa ( se houver )

    resultados = shows
    if termo:
        #pesquisa é uma função referente ao "buscar" na barra de escrever
        resultados = pesquisa(resultados, termo)
    
    #puxa da URL se foi adicionado filtro de gênero
    genero_selecionado = request.args.get('filtro_genero', '')
    #puxa da URL se foi adicionado filtro
    ordenar = request.args.get('ordenar', '')

    #Filtro de Gênero
    # show --> cada linha
    if genero_selecionado:
        lista_filtrada_genero = []
        for show in resultados:
            if show.get('genero', '').lower() == genero_selecionado.lower():
                lista_filtrada_genero.append(show)
        
    #Ordenação ordem alfabética
    if ordenar == 'alfabetica':
        resultados = sorted(resultados, key=lambda x: x.get('titulo', '').lower())

    #Ordenação preço
    elif ordenar == 'preco':
        resultados = sorted(resultados, key=lambda x: x.get('preco'))

    return resultados


def pesquisa(shows:list, termo:str)-> list:
    # A função é referente ao uso da barra de pesquisa do site
    # A saída é a lista com a exibilção única do que foi pesquisado

    termo = termo.lower()
    resultados = []
    for show in shows:
        # verificação se o termo ( conteudo da barra de pesquisa) bate com o nome do artista // dara // local
        if (termo in show['artista'].lower() or
            termo in show['data'].lower() or
            termo in show['local'].lower()):
            resultados.append(show)
    return resultados



#FUNÇÕES REFERENTES A GEOLOCALIZAÇÃO

# Função responsável por obter a coordenada do usuário e calcular o quao longe o usuário esta de cada um dos shows
# a entrada das coordenadas é através de um json 
# a função se comunica com o geolocalizacao.js
#a saída é um json contendo o quão próximo o usuario esta de cada um dos shows
def distancia():
    data = request.get_json()

    user_location = (
        float(data["latitude"]),
        float(data["longitude"])
    )

    proximidades = calcular_proximidades(user_location)
    return jsonify(proximidades)

#cálculo da função acima
def calcular_proximidades(user_location):
    proximidades = []
    #abre o csv e já define as linhas
    try:
        with open("data/dados.csv", newline="", encoding="utf-8") as f:
            linhas = f.read().splitlines()
    except FileNotFoundError:
        return proximidades
    
    if not linhas:
        return proximidades
    #define o cabeçalho
    cabecalho = linhas[0].split(',')
    #linhas == string grande com todas as informações
    #linha == iterador do FOR
    #valores == lista contendo cada informação das linhas ( ou seja de cada show ) todos em str

    #show == dicionario que associa o cabeçalho com o seu valor
    #show_location == lista que contém latitude e longitude de um show
    for linha in linhas[1:]:
        valores = linha.split(',')
        show = {}

        for i in range(len(cabecalho)):
            show[cabecalho[i]] = valores[i] if i < len(valores) else ""

        show_location = (
            float(show["latitude"]),
            float(show["longitude"])
        )
        # geodesic --> função que precisa de duas coordenadas e calcula a distancia entre elas
        distancia_km = geodesic(user_location, show_location).kilometers


        # proximidades == lista que contém sub-listas, cada uma delas contendo o nome do show e sua distância do usuário
        proximidades.append({
            "titulo": show["titulo"],
            "distancia_km": round(distancia_km, 2)
        })

    proximidades.sort(key=lambda x: x["distancia_km"])
    return proximidades

#função responsável pela página de "Shows próximos"
def shows_proximos():
    shows = carregar_csv()

    latitudes = [float(linha["latitude"]) for linha in shows]
    longitudes = [float(linha["longitude"]) for linha in shows]
    
    return render_template(
        'shows_proximos.html', 
        shows=shows, 
        user=current_user, 
        latitudes=latitudes, 
        longitudes=longitudes
    )


# função de logar usuario
def login():
    if request.method == 'GET':
        return render_template('public/login.html')
    #variaveis que pegam o nome e senha do banco de dados
    name = request.form.get('name')
    password = request.form.get('password')

    #se a senha e o usuario bater com o banco de dados, o usuario entra no site
    user = db.session.query(User).filter_by(name=name, password=password).first()
    if not user:
        return render_template('public/login.html', error="Usuário ou senha incorretos!", name=name)
    
    login_user(user)
    return redirect(url_for('home'))

# função de cadastrar novos usuarios
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
       
    if request.method == 'GET':
        return render_template('public/cadastro.html')
    # três variaveis, sendo que duas irão para o banco e uma é só a confirmação de senha
    elif request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        # verificação caso as duas senhas não esteja batendo
        if password != confirmpassword: 
            return render_template('public/cadastro.html', error="As senhas não coincidem!", name=name)
        
        # verifica se o usuario escolhido já não existe no banco de dados
        existing_user = db.session.query(User).filter_by(name=name).first()
        if existing_user:
            return render_template('public/cadastro.html', error='Usuário já existe!', name=name)
        
        # cria o usuario novo
        new_user = User(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('home'))

  
def artista_perfil(id_artista):
    artist_data = []
    caminho_csv2 = os.path.join(current_app.root_path, 'data', 'artistas.csv')
    if os.path.exists(caminho_csv2):
        with open(caminho_csv2, mode='r', encoding='utf-8') as arquivo:
            ler_csv = csv.DictReader(arquivo)
            for linha in ler_csv:
                if linha.get('id', '').strip() == id_artista:
                    artist_data = linha
                    artist_data = {
                        'id': linha.get('id', '').strip(),
                        'nome': linha.get('Nome', '').strip(),
                        'genero': linha.get('Genero', '').strip(),
                        'bio': linha.get('Bio', '').strip(),
                        'instagram': linha.get('Instagram', '').strip()
                    }
                    break

    if artist_data:
        return render_template('info_artista.html', artist=artist_data)
    else:
        return "Artista não encontrado", 404
    
           