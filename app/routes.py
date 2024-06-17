from flask import current_app as app, jsonify, request, render_template, redirect, url_for

@app.route('/', methods=['GET'])
def index():
    try:
        classes_response = app.supabase.table('CLASSES').select('*').execute()
        classes = classes_response.data

        teachers_response = app.supabase.table('TEACHERS').select('*').execute()
        teachers = teachers_response.data

        core_ids = list(set([c['core_id'] for c in classes]))

        cores_response = app.supabase.table('CORES').select('*').in_('id', core_ids).execute()
        cores = cores_response.data

        cores_dict = {core['id']: core['core'] for core in cores}

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

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Obter os dados do formulário
        teacher_id = request.form.get('teacher')
        class_id = request.form.get('class')
        date = request.form.get('date')
        selected_students = request.form.getlist('students')  # Lista de IDs dos alunos marcados

        print(teacher_id)
        print(class_id)
        print(date)
        print(selected_students)

        # Verificar se todos os campos foram preenchidos
        if not (teacher_id and class_id and date):
            return render_template('index.html', error="Por favor, preencha todos os campos.")
        
        # Inserir dados na tabela ATTENDANCES
        attendance_data = {
            'teacher_id': teacher_id,
            'class_id': class_id,
            'date': date
        }
        response = app.supabase.table('ATTENDANCES').insert(attendance_data).execute()
        attendance_id = response.data[0]['id']  # Obter o ID da chamada de presença inserida
        
        # Inserir dados na tabela ATTENDANCES_STUDENTS para cada aluno selecionado
        for student_id in selected_students:
            attendance_students_data = {
                'attendance_id': attendance_id,
                'student_id': student_id
            }
            app.supabase.table('ATTENDANCES_STUDENTS').insert(attendance_students_data).execute()
        
        return "Dados enviados com sucesso!"
    
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")
        return render_template('index.html', error="Erro ao enviar dados.")