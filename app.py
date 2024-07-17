from flask import Flask, render_template, request, redirect, url_for, session
import supabase
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')

app.supabase = supabase.create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = {'email': email, 'password': password}

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
            session['user_id'] = response.user.id 
            return redirect(url_for('welcome'))
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
    
    return "Esta é uma página protegida. Você está logado."

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
