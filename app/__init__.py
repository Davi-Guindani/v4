from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    load_dotenv()
    from .supabase import supabase_client
    app.supabase = supabase_client()

    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.protected import protected_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(protected_bp)

    return app
