from flask import render_template, request, redirect, url_for, current_app 
import os
from flask_login import logout_user, login_required, current_user
from . import artist_bp
import csv
import funcoes


# A função csv.reader() lê um aruqivo csv ( já considerando sua separação por ',' ) linha por linhas os dados sao lidos e retornados como strings

# Foi usado para reduzir o tamanho do codigo e a fins de estudo da biblioteca Csv


#objetivo da função: adquirir informações de um formulário HTML e adicionar como um novo show no dados.csv
@artist_bp.route('/marcar_show', methods=['GET', 'POST'])
@login_required
def marcar_show():
    #definido o endereço de ambas as tabelas
    artistascsv = os.path.join(current_app.root_path, 'data', 'artistas.csv')
    dadoscsv = os.path.join(current_app.root_path, 'data', 'dados.csv')

    #carrega a página
    if request.method == 'GET':
        return render_template('artist/marcar_show.html', user=current_user)
    
    elif request.method == 'POST':
        #Captura dados do formulário
        titulo_show = request.form.get('show')
        local = request.form.get('local')
        data = request.form.get('data')
        hora = request.form.get('hora')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        # Define 0.00 como padrão se o campo preco não estiver no HTML
        preco = request.form.get('preco', '0.00') 

        #em caso do artista não ter editado as informações no /profile tanto o artista qaunto o genero são dados como desconhecido
        artista = 'Desconhecido'
        genero = 'Desconhecido'

        # Faz uma verificação de ID de usuário para determinar o nome do artita e o seu gênero a aprtir de "artistas.csv"
        if os.path.exists(artistascsv):
            with open(artistascsv, mode='r', encoding='utf-8') as file:
                leitor = csv.reader(file)
                next(leitor, None)  # PULA O CABEÇALHO DO ARTISTAS.CSV
                for linha in leitor:
                    if linha and linha[0] == str(current_user.id):
                        artista = linha[1]
                        genero = linha[2]
                        break
        
        # Gera um novo id para o show
        novo_id = 1
        if os.path.exists(dadoscsv):
            with open(dadoscsv, mode='r', encoding='utf-8') as file:
                leitor = csv.reader(file)
                next(leitor, None)  # PULA O CABEÇALHO DO DADOS.CSV
                # Só tenta converter se for um dígito para evitar novos erros
                ids = []
                for linha in leitor:
                    if linha and linha[0].isdigit():
                        ids.append(int(linha[0]))
                if ids:
                    #ele cataloga todos os ids depois usa a função max para peagr o maior deles e adicionar +1
                    novo_id = max(ids) + 1

        # Salva o novo show
        # aqui foi implementado a função csv.writerow() para escrever uma nova coluna de maneira mais rapida e com menos codigo
        try:
            with open(dadoscsv, mode='a', newline='', encoding='utf-8') as file:
                salvar = csv.writer(file)
                salvar.writerow([
                    novo_id, titulo_show, artista, data, 
                    hora, local, genero, preco, latitude, longitude
                ])
            
            # Redirecionar para o perfil para ver o resultado
            return redirect(url_for('artist.profile'))
        
        except Exception as e:
            return f"Erro ao salvar o show: {e}"


#objetivo da função: Editar informaçõe de perfil do artista
@artist_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    #define o endereço dos dois principais atributos
    tabela = os.path.join(current_app.root_path, 'data', 'artistas.csv')
    id = str(current_user.id)
    
    #formulário para peagar as informações do usuario através do formulário
    if request.method == 'POST':
        nome = request.form.get('nome')
        genero = request.form.get('genero')
        bio = request.form.get('bio')
        instagram = request.form.get('instagram')


        #NÂO APAGAR
        #objetivo: verificação de usuário já existe para que ao inves de criar uma nova linha na tabela altere uma ja existente
        linhas_atualizadas = []
        usuario_encontrado = False

        
        if os.path.exists(tabela):
            with open(tabela, mode='r', encoding='utf-8') as file:
                leitor = csv.reader(file)
                for linha in leitor:
                    #se a linha atual e a primeira informação da linha == id
                    # significa que já exite um usuário com esse id ou seja usuaário existente
                    if linha and linha[0] == id:
                        # Substitui pelos novos dados
                        linhas_atualizadas.append([id, nome, genero, bio, instagram])
                        usuario_encontrado = True
                    else:
                        linhas_atualizadas.append(linha)

        #se não existir usuário adicionamos uma nova linha na tabela no final dela
        if not usuario_encontrado:
            linhas_atualizadas.append([id, nome, genero, bio, instagram])

        # reescreve a tabela 
        try:
            with open(tabela, mode='w', newline='', encoding='utf-8') as file:
                escritor = csv.writer(file)
                escritor.writerows(linhas_atualizadas)
            
            return redirect(url_for('artist.profile'))
        except Exception as e:
            return f"Erro ao atualizar: {e}"

    # Lógica GET para exibir os dados
    user_data = None
    if os.path.exists(tabela):
        with open(tabela, mode='r', encoding='utf-8') as file:
            leitor = csv.reader(file)
            for linha in leitor:
                #separação dos dados com suas devidas colunas
                if linha and linha[0] == id:
                    user_data = {'nome': linha[1], 'genero': linha[2], 'bio': linha[3], 'instagram': linha[4]}
                    break

    return render_template('artist/profile.html', user=current_user, data=user_data)


# função de logout
@artist_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@artist_bp.route('/artistas/<id>')
def artista_perfil(id):
    return funcoes.artista_perfil(id)
