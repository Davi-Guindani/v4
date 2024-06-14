from flask import Flask
from supabase import create_client
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    SUPABASE_URL = app.config['SUPABASE_URL']
    SUPABASE_KEY = app.config['SUPABASE_KEY']
    app.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    with app.app_context():
        from . import routes

    return app
