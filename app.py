from flask import Flask, render_template, request, redirect, url_for, session
import supabase
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Defina sua secret key

# Carregar variáveis de ambiente
load_dotenv()

# Criar cliente Supabase com variáveis de ambiente
app.supabase = supabase.create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

@app.route('/')
def home():
    user_logged_in = 'user_id' in session
    user_type = session.get('user_type', None)
    return render_template('home.html', logged_in=user_logged_in, user_type=user_type)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        user_data = {'email': email, 'password': password, 'options': {'data': {'user_type': user_type}}}

        try:
            response = app.supabase.auth.sign_up(user_data)
            return redirect(url_for('success'))
        except Exception as e:
            return str(e)

    return render_template('sign_up.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = {'email': email, 'password': password}

        try:
            response = app.supabase.auth.sign_in_with_password(user_data)
            session['user_id'] = response.user.id  # Armazenar o ID do usuário na sessão
            user_metadata = response.user.user_metadata
            session['user_type'] = user_metadata.get('user_type')
            return redirect(url_for('home'))
        except Exception as e:
            return str(e)
    
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'user_id' in session:
        return "Bem-vindo! Login realizado com sucesso."
    else:
        return redirect(url_for('login'))

@app.route('/protected')
def protected():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_type = session.get('user_type')
    if user_type not in ['teacher', 'manager']:
        return "Acesso negado."

    return "Esta é uma página protegida. Você está logado."

@app.route('/manage_students')
def manage_students():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_type = session.get('user_type')
    if user_type not in ['manager']:
        return "Acesso negado."
    
    return "Página de gerenciamento de alunos."

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=False, host='0.0.0.0', port=80)
