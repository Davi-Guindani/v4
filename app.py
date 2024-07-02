from flask import Flask, render_template
from supabase import create_client
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Creating Supabase client with env vars
load_dotenv()
app.supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

@app.route('/')
def sign_up():

    return render_template("sign_up.html")

@app.route('/login')
def login():

    return render_template("login.html")

if __name__ == "__main__":

    app.run(debug=False)
    # app.run(debug=False,host='0.0.0.0', port=80)
