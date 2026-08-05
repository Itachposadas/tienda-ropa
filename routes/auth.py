from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user = Usuario.query.filter_by(nombre_usuario=request.form.get('nombre_usuario')).first()
        if user and user.check_password(request.form.get('contrasena')):
            login_user(user)
            flash('¡Bienvenido!', 'success')
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('index'))