from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    class_name = request.form.get('class')
    date = request.form.get('date')
    teacher = request.form.get('teacher')
    list_items = request.form.get('specific[]')

    # Concatena os itens da lista em uma string
    list_items_str = request.form.get('list')

    # Verifica se o arquivo já existe
    file_exists = os.path.isfile('dados.xlsx')

    # Se o arquivo não existir, cria um novo DataFrame e salva
    if not file_exists:
        df = pd.DataFrame(columns=['Turma', 'Data', 'Professor', 'Lista'])
        df.to_excel('dados.xlsx', index=False)

    # Carrega os dados existentes
    df = pd.read_excel('dados.xlsx')

    # Cria um novo DataFrame com os novos dados
    new_data = pd.DataFrame({'Turma': [class_name], 'Data': [date], 'Professor': [teacher], 'Lista': [list_items_str]})

    # Concatena os DataFrames
    df = pd.concat([df, new_data], ignore_index=True)

    # Salva os dados atualizados no arquivo
    df.to_excel('dados.xlsx', index=False)

    print(f'Turma: {class_name}')
    print(f'Data: {date}')
    print(f'Professor: {teacher}')
    print(f'Lista: {list_items_str}')
    
    return f'Dados recebidos e armazenados: Turma - {class_name}, Data - {date}, Professor - {teacher}, Lista - {list_items_str}'

if __name__ == '__main__':
    app.run(debug=True)
