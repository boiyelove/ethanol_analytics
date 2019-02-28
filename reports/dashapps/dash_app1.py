import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_daq as daq
import json
import dash_bootstrap_components as dbc
from .py_helpers import db_sql
from django_plotly_dash import DjangoDash

app = DjangoDash('1',external_stylesheets=[dbc.themes.BOOTSTRAP])

#app2 = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

## Helper Function to get data. This is run 
def get_batch_data(ferm_num=None):
    SQL = """Select * from dash.current_ferms_batch_metadata where ferm_num = {}""".format(ferm_num)
    engine = db_sql.engine
    df = pd.read_sql(SQL,engine)
    batch_id = df['batch_id'][0]
    SQL_data = """Select a.datetime,a.sensor_id, 
                        a.batch_id, a.asset_name, 
                        a.hour, a.test, a.value :: numeric as value,
                        b.week_avg :: numeric, b.month_avg :: numeric
                    from dash.current_ferms_raw_lab_data a 
                inner join dash.current_ferms_lab_data_kpi b
                on a.sensor_id = b.sensor_id and a.batch_id = {}""".format(batch_id)
    df_data = pd.read_sql(SQL_data,engine)
    return df, df_data


tabs = html.Div([dbc.Tabs(
    [
        dbc.Tab( label="Ferm 601",tab_id ='ferm-601'),
        dbc.Tab( label="Ferm 602",tab_id ='ferm-602'),
        dbc.Tab( label="Ferm 603",tab_id ='ferm-603'),
        dbc.Tab( label="Ferm 604",tab_id ='ferm-604'),
    ],
    id='ferm-tabs',
    card=False,
    active_tab='ferm-601',

)])

header =  html.Div(
        [
        dbc.Row(
            [
                dbc.Col(html.H4('Batch ID: ', id = 'header_batch_id',style={'textAlign':'center'}),width=4),
                dbc.Col(html.H4("Last Test: "), width=4),
                dbc.Col(dcc.Dropdown(id='test_dropdown',placeholder = 'Lab Test timeframe',), width=2),
                dbc.Col(html.Div('SOMETHING'), width=2),
            ]
        ),
              
        ])





body = html.Div([ 
    dbc.Row([ 
        dbc.Col([],width=4), 
        dbc.Col([],width=4),
        dbc.Col([dash_table.DataTable(
                    id='lab_data',
                    columns=[{"name": 'Lab Test', "id": 'test'},
                    {"name": 'value', "id": 'value'},
                    {"name": 'Week Avg', "id": 'week_avg'},
                    {"name": 'Month Avg', "id": 'month_avg'},],
                ),],width=4),
    ])
 ])


app.layout = html.Div(children=[
    html.Div(id='hidden_data',style={'display': 'none'}),
    tabs,
    header,
    body,
    html.Div(id='body_content'),
 
])

@app.callback(
    Output('hidden_data','children'),
    [Input("ferm-tabs", "active_tab")]
)

def load_data(tab):
    tab = int(tab[-3:])
    df, df_data = get_batch_data(tab)
    datasets = {'df':df.to_json(orient='split',date_format='iso'),'df_data':df_data.to_json(orient='split',date_format='iso')}
    return json.dumps(datasets)

@app.callback(
    Output("header_batch_id", "children"), [Input('hidden_data','children')]
)
def switch_tab(int_data):
    datasets = json.loads(int_data)
    df = pd.read_json(datasets['df'],orient='split')
    return 'Batch ID: {}'.format(df['batch_id'][0])

@app.callback(
    Output('test_dropdown','options'),
    [Input('hidden_data','children')]
) 
def set_dropdown(int_data):
    datasets = json.loads(int_data)
    df = pd.read_json(datasets['df_data'],orient='split')
    df = df[['asset_name','hour','datetime']].drop_duplicates().sort_values(by='datetime',ascending = False).reset_index(drop=True)
    df['id'] = df['asset_name'] + '.' + df['hour']
    options = []
    for i in df.to_dict('rows'):
        temp = {'label':i['id'],'value':i['id']}
        options.append(temp)
    return options

@app.callback(
    Output('test_dropdown','value'),
    [Input('test_dropdown','options'),],
) 
def set_dropdown_value(options):
    return options[0]['value']

@app.callback(
    Output('lab_data','data'),
    [Input('test_dropdown','value')],
    [State('hidden_data','children')]
)
def show_data(value,df):
    datasets = json.loads(df)
    df = pd.read_json(datasets['df_data'],orient='split')
    df['id'] = df['asset_name'] + '.' + df['hour']
    df = df[df['id']==value].reset_index(drop=True)
    df[['value','week_avg','month_avg']] = df[['value','week_avg','month_avg']].round(3)
    df = df[['test','value','week_avg','month_avg']].sort_values('test').to_dict('rows')
    return df



# if __name__ == '__main__':
#     app.run_server(debug=True,dev_tools_hot_reload=True,)
