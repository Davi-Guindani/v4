from flask import current_app as app, jsonify, request, render_template, redirect, url_for

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

        # Criar um dicionário de core para fácil acesso
        cores_dict = {core['id']: core['core'] for core in cores}

        # Adicionar o valor do core a cada classe
        for c in classes:
            c['core'] = cores_dict.get(c['core_id'], 'Unknown')
    except Exception as e:
        classes = []
        print(f"Erro ao buscar turmas e lugares: {e}")

    return render_template('index.html', classes=classes, teachers=teachers)

@app.route('/get_students', methods=['GET'])
def get_students():
    class_id = request.args.get('class_id')
    try:
        # Buscar os registros da tabela CLASSES_STUDENTS para a turma selecionada
        classes_students_response = app.supabase.table('CLASSES_STUDENTS').select('*').eq('class_id', class_id).execute()
        classes_students = classes_students_response.data

        # Obter todos os student_ids
        student_ids = [cs['student_id'] for cs in classes_students]

        # Buscar os alunos correspondentes aos student_ids
        students_response = app.supabase.table('STUDENTS').select('*').in_('id', student_ids).execute()
        students = students_response.data

        # Preparar a resposta com os dados dos alunos
        students_data = [{'id': student['id'], 'name': student['name']} for student in students]
        return jsonify({'students': students_data})

    except Exception as e:
        print(f"Erro ao buscar alunos: {e}")
        return jsonify({'error': 'Erro ao buscar alunos'}), 500
