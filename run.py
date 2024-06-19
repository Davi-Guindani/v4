from flask import Flask, jsonify, request, render_template
from config import Config
from supabase import create_client
from dashapp import create_dash_app


server = Flask(__name__)
server.config.from_object(Config)

SUPABASE_URL = server.config['SUPABASE_URL']
SUPABASE_KEY = server.config['SUPABASE_KEY']

server.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@server.route('/', methods=['GET'])
def index():
    try:
        classes_response = server.supabase.table('CLASSES').select('*').execute()
        classes = classes_response.data

        teachers_response = server.supabase.table('TEACHERS').select('*').execute()
        teachers = teachers_response.data

        core_ids = list(set([c['core_id'] for c in classes]))

        cores_response = server.supabase.table('CORES').select('*').in_('id', core_ids).execute()
        cores = cores_response.data

        cores_dict = {core['id']: core['core'] for core in cores}

        for c in classes:
            c['core'] = cores_dict.get(c['core_id'], 'Unknown')

        # Obter dias para cada turma
        classes_ids = [c['id'] for c in classes]
        classes_days_response = server.supabase.table('CLASSES_DAYS').select('*').in_('class_id', classes_ids).execute()
        classes_days = classes_days_response.data

        day_ids = list(set([cd['day_id'] for cd in classes_days]))
        days_response = server.supabase.table('DAYS').select('*').in_('id', day_ids).execute()
        days = days_response.data

        days_dict = {day['id']: day['day'] for day in days}

        for c in classes:
            c['days'] = [days_dict[cd['day_id']].title() for cd in classes_days if cd['class_id'] == c['id']]

    except Exception as e:
        classes = []
        teachers = []
        print(f"Erro ao buscar turmas e lugares: {e}")

    return render_template('index.html', classes=classes, teachers=teachers)

@server.route('/get_students', methods=['GET'])
def get_students():
    class_id = request.args.get('class_id')
    try:
        classes_students_response = server.supabase.table('CLASSES_STUDENTS').select('*').eq('class_id', class_id).execute()
        classes_students = classes_students_response.data

        student_ids = [cs['student_id'] for cs in classes_students]

        students_response = server.supabase.table('STUDENTS').select('*').in_('id', student_ids).execute()
        students = students_response.data

        students_data = [{'id': student['id'], 'name': student['name'], 'last_name': student['last_name']} for student in students]
        return jsonify({'students': students_data})

    except Exception as e:
        print(f"Erro ao buscar alunos: {e}")
        return jsonify({'error': 'Erro ao buscar alunos'}), 500
    
@server.route('/submit', methods=['POST'])
def submit():
    try:
        teacher_id = request.form.get('teacher')
        class_id = request.form.get('class')
        date = request.form.get('date')
        selected_students = request.form.getlist('students')

        if not (teacher_id and class_id and date):
            return render_template('index.html', error="Por favor, preencha todos os campos.")

        existing_attendance_response = server.supabase.table('ATTENDANCES').select('*').eq('class_id', class_id).eq('date', date).execute()
        existing_attendance = existing_attendance_response.data

        if existing_attendance:
            return jsonify({'error': 'Registro duplicado', 'attendance_id': existing_attendance[0]['id']}), 409
        
        attendance_data = {
            'teacher_id': teacher_id,
            'class_id': class_id,
            'date': date
        }
        response = server.supabase.table('ATTENDANCES').insert(attendance_data).execute()
        attendance_id = response.data[0]['id']

        for student_id in selected_students:
            attendance_students_data = {
                'attendance_id': attendance_id,
                'student_id': student_id
            }
            server.supabase.table('ATTENDANCES_STUDENTS').insert(attendance_students_data).execute()
        
        return jsonify({'success': 'Dados enviados com sucesso!'})
    
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")
        return jsonify({'error': 'Erro ao enviar dados.'}), 500
    
@server.route('/edit_attendance/<int:attendance_id>', methods=['GET', 'POST'])
def edit_attendance(attendance_id):
    if request.method == 'GET':
        try:
            attendance_response = server.supabase.table('ATTENDANCES').select('*').eq('id', attendance_id).execute()
            attendance = attendance_response.data[0]

            # Buscar todos os alunos da turma
            class_id = attendance['class_id']
            classes_students_response = server.supabase.table('CLASSES_STUDENTS').select('*').eq('class_id', class_id).execute()
            classes_students = classes_students_response.data

            student_ids = [cs['student_id'] for cs in classes_students]
            students_response = server.supabase.table('STUDENTS').select('*').in_('id', student_ids).execute()
            students = students_response.data

            # Buscar alunos já registrados na presença
            attendance_students_response = server.supabase.table('ATTENDANCES_STUDENTS').select('*').eq('attendance_id', attendance_id).execute()
            attendance_students = attendance_students_response.data
            registered_student_ids = [ats['student_id'] for ats in attendance_students]

            teachers_response = server.supabase.table('TEACHERS').select('*').execute()
            teachers = teachers_response.data

            return render_template('edit_attendance.html', attendance=attendance, students=students, teachers=teachers, registered_student_ids=registered_student_ids)
        
        except Exception as e:
            print(f"Erro ao buscar registro de presença: {e}")
            return jsonify({'error': 'Erro ao buscar registro de presença.'}), 500

    if request.method == 'POST':
        try:
            date = request.form.get('date')
            teacher_id = request.form.get('teacher')
            selected_students = request.form.getlist('students')

            attendance_data = {
                'date': date,
                'teacher_id': teacher_id
            }
            server.supabase.table('ATTENDANCES').update(attendance_data).eq('id', attendance_id).execute()

            server.supabase.table('ATTENDANCES_STUDENTS').delete().eq('attendance_id', attendance_id).execute()
            for student_id in selected_students:
                attendance_students_data = {
                    'attendance_id': attendance_id,
                    'student_id': student_id
                }
                server.supabase.table('ATTENDANCES_STUDENTS').insert(attendance_students_data).execute()
            
            return jsonify({'success': 'Dados atualizados com sucesso!'})
        
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")
            return jsonify({'error': 'Erro ao atualizar dados.'}), 500

app = create_dash_app(server)

if __name__ == '__main__':
    server.run(debug=True,host='0.0.0.0', port=5000)