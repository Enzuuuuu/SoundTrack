from flask import render_template, request, redirect, url_for, current_app 
import os
from flask_login import logout_user, login_required, current_user
from . import artist_bp
import csv

@artist_bp.route('/marcar_show')
@login_required
def marcar_show():
    return render_template('artist/marcar_show.html', user=current_user)

@artist_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    csv_path = os.path.join(current_app.root_path, 'data', 'artistas.csv')
    user_id = str(current_user.id)
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        genero = request.form.get('genero')
        bio = request.form.get('bio')
        instagram = request.form.get('instagram')

        linhas_atualizadas = []
        usuario_encontrado = False

        # 1. Ler o arquivo e atualizar a lista na memória
        if os.path.exists(csv_path):
            with open(csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == user_id:
                        # Substitui pelos novos dados
                        linhas_atualizadas.append([user_id, nome, genero, bio, instagram])
                        usuario_encontrado = True
                    else:
                        linhas_atualizadas.append(row)

        # 2. Se o usuário não existia no CSV, adicionamos uma nova linha
        if not usuario_encontrado:
            linhas_atualizadas.append([user_id, nome, genero, bio, instagram])

        # 3. Reescrever o arquivo com a lista completa (ou nova ou atualizada)
        try:
            with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(linhas_atualizadas)
            
            return redirect(url_for('artist.profile'))
        except Exception as e:
            return f"Erro ao atualizar: {e}"

    # Lógica GET para exibir os dados (como já tínhamos feito)
    user_data = None
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == user_id:
                    user_data = {'nome': row[1], 'genero': row[2], 'bio': row[3], 'instagram': row[4]}
                    break

    return render_template('artist/profile.html', user=current_user, data=user_data)

@artist_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
