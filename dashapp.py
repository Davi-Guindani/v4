from dash import Dash, html, dcc, Input, Output
import plotly.graph_objs as go
import pandas as pd
from collections import Counter
from datetime import datetime

def create_dash_app(server):
    dash_app = Dash(server=server, url_base_pathname='/dash/')

    attendances_response = server.supabase.table('ATTENDANCES').select('*').eq('class_id', 8).order('date').execute()
    attendances_response = attendances_response.data
    datas = list([at['date'] for at in attendances_response])
    datas = [datetime.strptime(data, '%Y-%m-%d').date() for data in datas]

    atids = list([at['id'] for at in attendances_response])
    attendances_students_response = server.supabase.table('ATTENDANCES_STUDENTS').select('*').in_('attendance_id', atids).execute()
    attendances_students_response = attendances_students_response.data
    attendances_students_response = sorted(attendances_students_response, key=lambda x: x['attendance_id'])
    attendace_students_counts = Counter(item['attendance_id'] for item in attendances_students_response)
    occurrence_list = list(attendace_students_counts.values())
    
    df = pd.DataFrame(
        {
            'datas': datas,
            'qtd': occurrence_list
        }
    )

    figteste = go.Figure(go.Bar(x=df['datas'], y=df['qtd']))
    figteste.layout = dict(xaxis=dict(type="category"))

    attendances_response = server.supabase.table('ATTENDANCES').select('*').eq('class_id', 1).order('date').execute()
    attendances_response = attendances_response.data
    datas = list([at['date'] for at in attendances_response])
    datas = [datetime.strptime(data, '%Y-%m-%d').date() for data in datas]

    atids = list([at['id'] for at in attendances_response])
    attendances_students_response = server.supabase.table('ATTENDANCES_STUDENTS').select('*').in_('attendance_id', atids).execute()
    attendances_students_response = attendances_students_response.data
    attendances_students_response = sorted(attendances_students_response, key=lambda x: x['attendance_id'])
    attendace_students_counts = Counter(item['attendance_id'] for item in attendances_students_response)
    occurrence_list = list(attendace_students_counts.values())
    
    df = pd.DataFrame(
        {
            'datas': datas,
            'qtd': occurrence_list
        }
    )

    figteste2 = go.Figure(go.Bar(x=df['datas'], y=df['qtd']))
    figteste2.layout = dict(xaxis=dict(type="category"))

    dash_app.layout = html.Div([
        html.H1('Turma 20:00 às 21:15'),
        dcc.Graph(id='grafico teste', figure=figteste),
        html.H1('Turma 18:45 às 20:00'),
        dcc.Graph(id='grafico teste 2', figure=figteste2)
    ])
    
    return dash_app