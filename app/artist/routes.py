from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user 
from . import artist_bp
from db import db
from models import User
import funcoes

# Home principal na visão do artista
@artist_bp.route('/dashboard')
@login_required
def dashboard():
    shows = funcoes.carregar_shows()
    dist = funcoes.carregar_csv()
    shows_filtrados =  funcoes.pesquisar_shows(shows, request.args.get('pesquisa', ''))

    latitudes = [float(linha["latitude"]) for linha in dist]
    longitudes = [float(linha["longitude"]) for linha in dist]

    for s in shows_filtrados[:5]:
        print(s["titulo"], s.get("distancia_km"))
    
    return render_template(
        'artist/index.html', 
        shows=shows, 
        dist=dist, 
        user=current_user, 
        latitudes=latitudes, 
        longitudes=longitudes
    )
    

# Logout (saindo da conta) 
@artist_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))