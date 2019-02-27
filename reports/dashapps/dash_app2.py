import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('2',external_stylesheets=[dbc.themes.BOOTSTRAP])
# app = dash.Dash(__name__,)# external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Dash App 2'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

# if __name__ == '__main__':
#     app.run_server(debug=True)