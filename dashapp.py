from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

def create_dash_app(flask_app):
    dash_app = Dash(server=flask_app, url_base_pathname='/dash/')
    
    # Obter dados de estudantes do Supabase
    students_response = flask_app.supabase.table('STUDENTS').select('*').execute()
    students = students_response.data

    # Criar DataFrame
    students_df = pd.DataFrame(students)

    # Gráfico de pizza para porcentagem de homens e mulheres
    genre_counts = students_df['genre'].value_counts(normalize=True) * 100
    genre_counts = genre_counts.reset_index()
    genre_counts.columns = ['genre', 'percentage']
    fig_pie = px.pie(genre_counts, values='percentage', names='genre', title='Porcentagem de Homens e Mulheres')

    data = {
        'frutas': ['Maçã', 'Banana', 'Laranja', 'Uva', 'Pêssego'],
        'qtd': [10, 5, 8, 12, 3]
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x='frutas', y='qtd')

    dash_app.layout = html.Div([
        html.H1('Dashboardzada'),
        dcc.Graph(id='grafico', figure=fig),
        dcc.Graph(id='grafico_pie', figure=fig_pie)
    ])
    
    return dash_app