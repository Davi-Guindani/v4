from flask import Blueprint, render_template, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    user_logged_in = 'user_id' in session
    user_type = session.get('user_type', None)
    return render_template('home.html', logged_in=user_logged_in, user_type=user_type)
