from flask import Flask, render_template, request, redirect, url_for
import supabase

from dotenv import load_dotenv
import os

app = Flask(__name__)

# Creating Supabase client with env vars
load_dotenv()
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
            session = app.supabase.auth.sign_in_with_password(user_data)
            return redirect(url_for('welcome'))
        except Exception as e:
            return str(e)
    
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    return "Bem-vindo! Login realizado com sucesso."

if __name__ == "__main__":

    app.run(debug=True)
    # app.run(debug=False,host='0.0.0.0', port=80)
