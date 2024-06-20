from flask import Flask
from dotenv import load_dotenv
import os
from supabase import create_client

app = Flask(__name__)

load_dotenv()
app.supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))



@app.route('/')
def hello_world():
    return 'Oi'