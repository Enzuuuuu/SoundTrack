# SoundTrack
Este projeto é um site voltado para a descoberta de novos músicos e artistas locais, conectando pessoas à cena musical da sua própria região. A plataforma utiliza a localização do usuário para sugerir músicos, bandas e eventos próximos, valorizando talentos locais que muitas vezes passam despercebidos.


**Funções auxiliares**

user_loader(id)
Carrega o usuário logado a partir do banco de dados usando o ID armazenado na sessão.


carregar_shows()
Lê manualmente o arquivo dados.csv e transforma cada linha em um dicionário, retornando uma lista de shows.


pesquisar_shows(shows, termo)
Filtra os shows com base em um termo de busca (artista, data ou local).


filtrar_shows_alfabeticamente(shows)
Ordena os shows em ordem alfabética pelo título.


calcular_proximidades(user_location)
Calcula a distância entre a localização do usuário e cada show usando coordenadas geográficas, retornando os shows ordenados do mais próximo ao mais distante.



 **Rotas da aplicação**
/ (home)

Rota principal do site.
Carrega os shows do CSV, aplica filtros (busca, gênero, ordem alfabética ou preço) e envia os dados para o template index.html.

/login (GET, POST)
GET: exibe a página de login.

POST: valida usuário e senha, autentica o usuário e inicia a sessão.


/cadastro (GET, POST)
GET: exibe a página de cadastro.

POST: cria um novo usuário no banco de dados após validar senha e evitar duplicidade.


/logout

Encerra a sessão do usuário autenticado e redireciona para a página inicial.


/coordenadas (POST)

Recebe latitude e longitude do frontend, converte em um endereço legível usando o Nominatim e retorna o endereço em JSON.


/distancia (POST)

Recebe a localização do usuário em JSON, calcula a distância até cada show e retorna uma lista ordenada por proximidade.




**Tecnologias e Bibliotecas Utilizadas**

Flask
Framework web responsável pelo gerenciamento das rotas, requisições HTTP, renderização de templates HTML e retorno de respostas ao cliente.


Flask-Login
Biblioteca utilizada para o controle de autenticação e sessões de usuários, permitindo login persistente, logout e proteção de rotas.


Flask-SQLAlchemy
ORM (Object-Relational Mapping) empregado para a manipulação do banco de dados SQLite, facilitando a persistência e consulta de dados de usuários.


SQLite
Banco de dados relacional leve, utilizado para armazenamento das informações de autenticação.


Geopy (Nominatim e Geodesic)

Nominatim: serviço de geocodificação reversa para conversão de coordenadas geográficas em endereços textuais.
Geodesic: cálculo da distância real entre dois pontos geográficos, considerando a curvatura da Terra.

JSON / Flask jsonify
Utilizado para troca de dados estruturados entre frontend e backend, viabilizando requisições assíncronas via JavaScript.