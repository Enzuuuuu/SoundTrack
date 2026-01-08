from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user 
from . import artist_bp
from db import db
from models import User

# Dashboard do Artista
@artist_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('artist/index.html', user=current_user)


# Logout (saindo da conta) 
@artist_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))