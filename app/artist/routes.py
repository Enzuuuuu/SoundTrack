from flask import render_template, request, redirect, url_for, current_app 
import os
from flask_login import logout_user, login_required, current_user
from . import artist_bp
import csv

@artist_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    csv_path = os.path.join(current_app.root_path, 'data', 'artistas.csv')
    if request.method == 'POST':
        # DEBUG: Verifique se isso aparece no seu terminal preto/VS Code
        print("Tentando salvar dados...") 
        
        nome = request.form.get('nome')
        genero = request.form.get('genero')
        bio = request.form.get('bio')
        instagram = request.form.get('instagram')
        
        user_id = str(current_user.id)
        print(f"Dados: {nome}, {genero}")

        
        
        try:
            with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([user_id,nome, genero, bio, instagram])
            
            print("Sucesso ao gravar no CSV!")
            return redirect(url_for('artist.profile')) # Ajuste conforme seu Blueprint
            
        except Exception as e:
            print(f"ERRO DE ESCRITA: {e}")
            return f"Erro técnico: {e}"
# --- LÓGICA PARA CARREGAR OS DADOS DO USUÁRIO ---
    user_data = {}
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # Se a primeira coluna for o ID do usuário logado, pegamos os dados
                if row and row[0] == str(current_user.id):
                    user_data = {
                        'nome': row[1],
                        'genero': row[2],
                        'bio': row[3],
                        'instagram': row[4]
                    }
    
    return render_template('artist/profile.html', user=current_user, data=user_data)

@artist_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
