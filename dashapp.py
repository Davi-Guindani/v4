from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

def create_dash_app(flask_app):
    dash_app = Dash(server=flask_app, url_base_pathname='/dash/')
    
    data = {
        'frutas': ['Maçã', 'Banana', 'Laranja', 'Uva', 'Pêssego'],
        'qtd': [10, 5, 8, 12, 3]
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x='frutas', y='qtd')

    dash_app.layout = html.Div([
        html.H1('Dashboardzada'),
        dcc.Graph(id='grafico', figure=fig)
    ])
    
    return dash_app
