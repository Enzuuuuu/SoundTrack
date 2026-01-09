from flask import  render_template, request, jsonify
from flask_login import current_user 
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


#inicializador da rota padrão (home)
def home():
    shows = carregar_shows()
    dist = carregar_csv()
    shows_filtrados =  pesquisar_shows(shows, request.args.get('pesquisa', ''))

    latitudes = [float(linha["latitude"]) for linha in dist]
    longitudes = [float(linha["longitude"]) for linha in dist]

    for s in shows_filtrados[:5]:
        print(s["titulo"], s.get("distancia_km"))
    
    user = current_user
    if user.is_authenticated:
        return render_template(
            'artist/index.html', 
            shows=shows, 
            dist=dist, 
            user=current_user, 
            latitudes=latitudes, 
            longitudes=longitudes
        )
    else:
        return render_template(
            'public/index.html', 
            shows=shows, 
            dist=dist, 
            user=current_user, 
            latitudes=latitudes, 
            longitudes=longitudes
        )



# para conseguir a variavel dist ( leitura manual do csv)
def carregar_csv():
    try:
        with open("data/dados.csv", "r", encoding="utf-8") as f:
            linhas = f.read().splitlines()
    except FileNotFoundError:
        linhas = []

    dist = []

    if linhas:
        cabecalho = linhas[0].split(',')

        for linha in linhas[1:]:
            valores = linha.split(',')

            row = {}
            for i in range(len(cabecalho)):
                row[cabecalho[i]] = valores[i] if i < len(valores) else ""

            dist.append(row)
    return dist


# função para pesquisa
def pesquisar_shows():
    resultados = pesquisar_shows(shows, request.args.get('pesquisa', ''))
    ordenar = request.args.get('ordenar', '')
    if resultados:
        shows = resultados
    
    genero_filtro = request.args.get('genero', '')
    if ordenar == 'genero' and genero_filtro:
        shows = [show for show in shows if show.get('genero', '').lower() == genero_filtro.lower()]
    if ordenar == 'alfabetica':
        shows = sorted(shows, key=lambda x: x['titulo'].lower())
    
    if ordenar == 'preco':
        shows = sorted(shows, key=lambda x: float(x.get('preco', float('inf'))))
        return shows
    


# vara a tabela csv e cataloga os Shows
def carregar_shows():
    try:
        with open('data/dados.csv', 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.read().splitlines()
    except FileNotFoundError:
        return []

    if not linhas:
        return []

    shows = []

    cabecalho = linhas[0].split(',')

    for linha in linhas[1:]:
        valores = linha.split(',')

        row = {}
        for i in range(len(cabecalho)):
            if i < len(valores):
                row[cabecalho[i]] = valores[i]
            else:
                row[cabecalho[i]] = ""

        shows.append(row)

    return shows



# função para pesquisa
def pesquisar_shows(shows, termo):
    termo = termo.lower()
    resultados = []
    for show in shows:
        if (termo in show['artista'].lower() or
            termo in show['data'].lower() or
            termo in show['local'].lower()):
            resultados.append(show)
    return resultados



#inicialização em ordem alfabética por padrão
def filtrar_shows_alfabeticamente(shows):
    return sorted(shows, key=lambda x: x['titulo'].lower())



# função para descobrir localização a partir de coordenadas
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

# função para calcular distâncias entre o usuário e os shows
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

    try:
        with open("data/dados.csv", newline="", encoding="utf-8") as f:
            linhas = f.read().splitlines()
    except FileNotFoundError:
        return proximidades

    if not linhas:
        return proximidades

    cabecalho = linhas[0].split(',')

    for linha in linhas[1:]:
        valores = linha.split(',')
        show = {}

        for i in range(len(cabecalho)):
            show[cabecalho[i]] = valores[i] if i < len(valores) else ""

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
    return proximidades



