from flask import Blueprint, render_template, request, redirect, url_for, session
from ..supabase import supabase_client

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        user_data = {'email': email, 'password': password, 'user_metadata': {'user_type': user_type}}

        try:
            response = supabase_client().auth.sign_up(user_data)
            return redirect(url_for('auth.success'))
        except Exception as e:
            return str(e)

    return render_template('sign_up.html')

@auth_bp.route('/success')
def success():
    return render_template('success.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = {'email': email, 'password': password}

        try:
            response = supabase_client().auth.sign_in_with_password(user_data)
            session['user_id'] = response.user.id  # Armazenar o ID do usuário na sessão
            user_metadata = response.user.user_metadata
            session['user_type'] = user_metadata.get('user_type')
            return redirect(url_for('main.home'))
        except Exception as e:
            return str(e)
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('main.home'))

@auth_bp.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return "Página da Conta"

@auth_bp.route('/my_class')
def my_class():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return "Página da Turma"

@auth_bp.route('/billing')
def billing():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return "Página de Mensalidade"
