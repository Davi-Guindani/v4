from flask import Blueprint, render_template, session, make_response

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    user_logged_in = 'user_id' in session
    user_type = session.get('user_type', None)
    response = make_response(render_template('home.html', logged_in=user_logged_in, user_type=user_type))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
