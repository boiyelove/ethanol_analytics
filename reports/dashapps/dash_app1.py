import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import json
import dash_bootstrap_components as dbc
from .py_helpers import db_sql
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np

plotly_config = {'modeBarButtonsToRemove':['sendDataToCloud','zoom2d','pan2d','select2d','lasso2d','toggleSpikelines',
                'zoomIn2d','zoomOut2d','autoScale2d','resetScale2d','hoverClosestCartesian','hoverCompareCartesian'],
                'displaylogo':False}
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
                        b.week_avg :: numeric, b.month_avg :: numeric,
                        ((week_avg::numeric - value::numeric)/week_avg::numeric) * 100 as week_pct_change,
                        ((month_avg::numeric - value::numeric)/month_avg::numeric) * 100 as month_pct_change
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
                dbc.Col(html.H4('Batch ID: ', id = 'header_batch_id',style={'textAlign':'left'}),width=2),
                dbc.Col(html.H4('Duration: ', id = 'batch_duration'), width=2),
                dbc.Col(dcc.Dropdown(id='lab_test_dropdown',placeholder = 'Lab Test'), width=4),
                dbc.Col(dcc.Dropdown(id='lab_period_dropdown',placeholder = 'Lab Test timeframe',), width=4),
                
            ]
        ),
              
        ])





body = html.Div([ 
    dbc.Row([ 
        dbc.Col([
            dbc.Row([
                dbc.Col(
                     html.Div(id='boxplot_1'),
                     width=4
                ),
                dbc.Col(
                html.Div(id='body_graph') ,width=8)
            ]),
            dbc.Row([
                dbc.Col(
                html.Div(id='body_graph_2')
                ,width=12)
            ]),
            
        ]
        ,width=8,md=8,sm=12), 
        dbc.Col([dash_table.DataTable(
                    id='lab_data',
                    columns=[{"name": 'Lab Test', "id": 'test'},
                    {"name": 'value', "id": 'value'},
                    {"name": 'Week Avg', "id": 'week_avg'},
                    {"name": '% Change', "id": 'week_pct_change'},
                    {"name": 'Month Avg', "id": 'month_avg'},
                    {"name": '% Change', "id": 'month_pct_change'},
                    ],
                    style_table={'overflowX': 'auto'},
                ),],width=4,md=4, sm=6),
    ])
 ])


app.layout = html.Div(children=[
    html.Div(id='hidden_data',style={'display': 'none'}),
    tabs,
    header,
    body, 
])



## Collects all data required from database
@app.callback(
    Output('hidden_data','children'),
    [Input("ferm-tabs", "active_tab")]
)

def load_data(tab):
    tab = int(tab[-3:])
    df, df_data = get_batch_data(tab)
    datasets = {'df':df.to_json(orient='split',date_format='iso'),'df_data':df_data.to_json(orient='split',date_format='iso')}
    return json.dumps(datasets)


## Header Callbacks

# Batch ID
@app.callback(
    Output("header_batch_id", "children"), [Input('hidden_data','children')]
)
def switch_tab(int_data):
    datasets = json.loads(int_data)
    df = pd.read_json(datasets['df'],orient='split')
    return 'Batch ID: {}'.format(df['batch_id'][0])

# Batch Duration
@app.callback(
    Output("batch_duration", "children"), [Input('hidden_data','children')]
)
def switch_tab(int_data):
    datasets = json.loads(int_data)
    df = pd.read_json(datasets['df'],orient='split')
    int(df['ferm_duration'][0])
    return 'Duration: {:.2f} Hours'.format(float(df['ferm_duration'][0]))

# Lab Period - set options
@app.callback(
    Output('lab_period_dropdown','options'),
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

# Lab Period - set value
@app.callback(
    Output('lab_period_dropdown','value'),
    [Input('lab_period_dropdown','options'),],
) 
def set_dropdown_value(options):
    return options[0]['value']

# Lab Test set value
@app.callback(
    Output('lab_test_dropdown','value'),
    [Input('lab_test_dropdown','options'),],
) 
def set_dropdown_value(options):
    return options[0]['value']

# Lab Period - set options
@app.callback(
    Output('lab_test_dropdown','options'),
    [Input('lab_period_dropdown','value'),],
    [State('hidden_data','children')]
) 
def set_dropdown_options(value, df):
    datasets = json.loads(df)
    df = pd.read_json(datasets['df_data'],orient='split')
    options_list = list(df.test.unique())
    options = []
    for i in options_list:
        temp = {'label':i,'value':i}
        options.append(temp)
    return options


## Body

# Lab datatable 
@app.callback(
    Output('lab_data','data'),
    [Input('lab_period_dropdown','value')],
    [State('hidden_data','children')]
)
def show_data(value,df):
    datasets = json.loads(df)
    df = pd.read_json(datasets['df_data'],orient='split')
    df['id'] = df['asset_name'] + '.' + df['hour']
    df = df[df['id']==value].reset_index(drop=True)
    df[['value','week_avg','month_avg','week_pct_change','month_pct_change']] = df[['value','week_avg','month_avg','week_pct_change','month_pct_change']].round(3)
    df[['week_pct_change','month_pct_change']] = df[['week_pct_change','month_pct_change']].round(2)
    df = df[['test','value','week_avg','week_pct_change','month_avg','month_pct_change']].sort_values('test').to_dict('rows')
    return df

## Graph
@app.callback(
    Output('body_graph','children'),
    [Input('lab_test_dropdown','value')],
    [State('hidden_data','children')]
)
def graph_data(value,df):
    datasets = json.loads(df)
    df = pd.read_json(datasets['df_data'],orient='split')
    df = df[df['test']==value].sort_values('datetime').reset_index(drop=True)
    data = []
    for i in df.test.unique():
        trace = go.Scatter(
            x = df[df['test']==i].datetime,
            y = df[df['test']==i].value,
            name = i,
        )
        data.append(trace)
    return dcc.Graph(
    config=plotly_config,
    figure=go.Figure(
        data=data,
        layout=go.Layout(
            title='Batch: {} - {}'.format(df['batch_id'][0],df['test'][0]),
            showlegend=False,
            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
        )
    ),
    style={'height': 300},
    id='my-graph'
)


@app.callback(
    Output('boxplot_1','children'),
    [Input('lab_test_dropdown','value'),
    Input('lab_period_dropdown','value')],
    [State('hidden_data','children')]
)
def graph_data(test,lab_period,df):
    datasets = json.loads(df)
    sensor_id = lab_period + '.' + test
    SQL = """Select * from whse.raw_lab_data where sensor_id = '{}' and datetime > current_Date - 180 and value::numeric != 0""".format(sensor_id)
    engine = db_sql.engine
    df = pd.read_sql(SQL,engine)

    df2 = pd.read_json(datasets['df_data'],orient='split')
    df2 = df2[df2['sensor_id']==sensor_id].sort_values('datetime').reset_index(drop=True)
    trace = go.Scatter(
        x=['Batch {}'.format(df2.batch_id[0])],
        y=df2.value,
        name= 'Batch {}'.format(df2.batch_id[0]),
        marker = {'size':10}
    )
    trace0 = go.Box(
        name='Historical Values',
        y=df.value,
        jitter = 0.3,
        pointpos = -1,
        boxpoints='all',
        )
    data = [trace0,trace]
    return dcc.Graph(figure=go.Figure(
            data=data,
            layout=go.Layout(showlegend=False,)),config=plotly_config)


@app.callback(
    Output('body_graph_2','children'),
    [Input('lab_test_dropdown','value'),
    Input('lab_period_dropdown','value')],
    [State('hidden_data','children')]
)
def graph_data(test,lab_period,df):
    sensor_id = lab_period + '.' + test
    SQL = """Select batch_id, datetime, value from whse.raw_lab_data where sensor_id = '{}' and datetime > current_Date - 180""".format(sensor_id)
    engine = db_sql.engine
    df = pd.read_sql(SQL,engine)
    df = df.sort_values('datetime').reset_index(drop=True)
    data = [go.Scatter(
            x = df.datetime,
            y = df.value,
            name = 'i',
        )]
    return dcc.Graph(
        config = plotly_config,
        
        figure=go.Figure(
            data=data,
            layout=go.Layout(
                showlegend=False,
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
            ),
            style={'height': 300},
            id='g2'
        )
