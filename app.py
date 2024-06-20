from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

@app.route('/')
def hello_world():
    return os.getenv('SUPABASE_URL')