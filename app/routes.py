from flask import current_app as app, request, render_template, redirect, url_for

@app.route('/')
def index():
    try:
        classes_response = app.supabase.table('CLASSES').select('*').execute()
        classes = classes_response.data

        # Obter todos os place_ids únicos das classes
        place_ids = list(set([c['place_id'] for c in classes]))

        # Buscar todos os lugares correspondentes aos place_ids
        places_response = app.supabase.table('PLACES').select('*').in_('id', place_ids).execute()
        places = places_response.data

        # Criar um dicionário de places para fácil acesso
        places_dict = {place['id']: place['place'] for place in places}

        # Adicionar o valor do place a cada classe
        for c in classes:
            c['place'] = places_dict.get(c['place_id'], 'Unknown')
    except Exception as e:
        classes = []
        print(f"Erro ao buscar turmas e lugares: {e}")
    
    return render_template('index.html', classes=classes)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    selected_class = request.form.get('selected_class')

    if name and email and selected_class:
        processed_data = {
            'name': name.title(),
            'email': email,
            'class_id': selected_class
        }

        try:
            response = app.supabase.table('your_table_name').insert(processed_data).execute()
            return "Dados enviados com sucesso!"
        except Exception as e:
            return f"Ocorreu um erro: {e}"
    return render_template('index.html', error="Por favor, preencha todos os campos.")
