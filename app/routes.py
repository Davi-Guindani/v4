from flask import current_app as app, request, render_template, redirect, url_for

@app.route('/')
def index():
    try:
        classes_response = app.supabase.table('CLASSES').select('*').execute()
        classes = classes_response.data

        teachers_response = app.supabase.table('TEACHERS').select('*').execute()
        teachers = teachers_response.data

        # Obter todos os core_ids únicos das turmas
        core_ids = list(set([c['core_id'] for c in classes]))

        # Buscar todos os núcleos correspondentes aos core_ids
        cores_response = app.supabase.table('CORES').select('*').in_('id', core_ids).execute()
        cores = cores_response.data

        # Criar um dicionário de places para fácil acesso
        cores_dict = {core['id']: core['core'] for core in cores}

        # Adicionar o valor do place a cada classe
        for c in classes:
            c['core'] = cores_dict.get(c['core_id'], 'Unknown')
    except Exception as e:
        classes = []
        print(f"Erro ao buscar turmas e lugares: {e}")
    
    return render_template('index.html', classes=classes, teachers=teachers)

@app.route('/submit', methods=['POST'])
def submit():
    selected_class = request.form.get('class')

    if selected_class:
        processed_data = {
            'class_id': selected_class
        }

        try:
            response = app.supabase.table('your_table_name').insert(processed_data).execute()
            return "Dados enviados com sucesso!"
        except Exception as e:
            return f"Ocorreu um erro: {e}"
    return render_template('index.html', error="Por favor, preencha todos os campos.")
