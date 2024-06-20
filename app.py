from flask import Flask, render_template
from dotenv import load_dotenv
import os
from supabase import create_client

app = Flask(__name__)

load_dotenv()
app.supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

@app.route('/', methods=['GET'])
def index():
    try:
        classes = app.supabase.table('CLASSES').select('*').execute()
        classes = classes.data

        teachers = app.supabase.table('TEACHERS').select('*').execute()
        teachers = teachers.data

        core_ids = list(set([c['core_id'] for c in classes]))

        cores = app.supabase.table('CORES').select('*').in_('id', core_ids).execute()
        cores = cores.data

        cores_dict = {core['id']: core['core'] for core in cores}

        for c in classes:
            c['core'] = cores_dict.get(c['core_id'], 'Unknown')

        # Obter dias para cada turma
        classes_ids = [c['id'] for c in classes]
        classes_days = app.supabase.table('CLASSES_DAYS').select('*').in_('class_id', classes_ids).execute()
        classes_days = classes_days.data

        day_ids = list(set([cd['day_id'] for cd in classes_days]))
        days = app.supabase.table('DAYS').select('*').in_('id', day_ids).execute()
        days = days.data

        days_dict = {day['id']: day['day'] for day in days}

        for c in classes:
            c['days'] = [days_dict[cd['day_id']].title() for cd in classes_days if cd['class_id'] == c['id']]

    except Exception as e:
        classes = []
        teachers = []
        print(f"Erro ao buscar turmas e lugares: {e}")

    return render_template('index.html', classes=classes, teachers=teachers)