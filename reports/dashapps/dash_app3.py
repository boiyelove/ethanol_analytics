import dash
import dash_core_components as dcc
import dash_html_components as html

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('3',external_stylesheets=[dbc.themes.BOOTSTRAP])
# app = dash.Dash(__name__,)# external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Dash App 3'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'scatter', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'scatter', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

# if __name__ == '__main__':
#     app.run_server(debug=True)