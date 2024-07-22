from flask import Blueprint, session
from ..decorators import login_required

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/welcome')
@login_required
def welcome():
    return "Bem-vindo! Login realizado com sucesso."

@protected_bp.route('/protected')
@login_required
def protected():
    user_type = session.get('user_type')
    if user_type not in ['teacher', 'manager']:
        return "Acesso negado."
    return "Esta é uma página protegida. Você está logado."

@protected_bp.route('/manage_students')
@login_required
def manage_students():
    user_type = session.get('user_type')
    if user_type not in ['manager']:
        return "Acesso negado."
    return "Página de gerenciamento de alunos."
