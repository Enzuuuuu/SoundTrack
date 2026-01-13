from flask import render_template, request, redirect, url_for, current_app 
import os
from flask_login import logout_user, login_required, current_user
from . import artist_bp
import csv

@artist_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # DEBUG: Verifique se isso aparece no seu terminal preto/VS Code
        print("Tentando salvar dados...") 
        
        nome = request.form.get('nome')
        genero = request.form.get('genero')
        bio = request.form.get('bio')
        instagram = request.form.get('instagram')
        
        print(f"Dados: {nome}, {genero}")

        # Caminho absoluto para evitar erros de localização
        csv_path = os.path.join(current_app.root_path, 'data', 'artistas.csv')

        try:
            with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([nome, genero, bio, instagram])
            
            print("Sucesso ao gravar no CSV!")
            return redirect(url_for('artist.profile')) # Ajuste conforme seu Blueprint
            
        except Exception as e:
            print(f"ERRO DE ESCRITA: {e}")
            return f"Erro técnico: {e}"

    return render_template('artist/profile.html')

@artist_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
