import dash
from dash.dependencies import State, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import dash_table
import pandas as pd
from .py_helpers import db_sql
import json 
import plotly.graph_objs as go
import plotly.figure_factory as ff

app = DjangoDash('3',external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)


def get_experiment_results(ex_id):
    df_dict = {}
    engine = db_sql.engine
    if ex_id == 0:
        SQL = """ Select experiment_id, experiment_name, (change_date :: date) :: varchar, assets, goal, status, create_user from whse.dim_experimentation_metadata 
            """.format(ex_id)
        df = pd.read_sql(SQL,engine)
        df_dict['metadata'] = df.to_json(orient='split', date_format='iso')
    elif ex_id != None:
        SQL = """ Select * from experimentation.current_results 
            where id =  {};""".format(ex_id)

        df = pd.read_sql(SQL,engine)
        df_dict['current_results'] = df.to_json(orient='split', date_format='iso')
        df_dict['sensor_list'] = df[['sensor_id','sensor_description']].to_json(orient='split', date_format='iso')
        SQL = """ Select id, name, change_date, assets, goal, status, create_user from whse.dim_experimentation_metadata 
            where id =  {};""".format(ex_id)
        df = pd.read_sql(SQL,engine)
        df_dict['metadata'] = df.to_json(orient='split', date_format='iso')
    return df_dict


def get_experiment_metadata():
    SQL = """Select experiment_id as value, experiment_name as label from whse.dim_experimentation_metadata
            order by experiment_id desc
            ;"""
    engine = db_sql.engine
    df = pd.read_sql(SQL,engine)
    df_dict =  df.to_dict('rows')
    df_dict.append({'label':'Home','value':0})
    df_dict = sorted(df_dict, key=lambda k: k['value']) 
    return df_dict

def main_page():
    return html.Div([
    dbc.Row(
        dbc.Col(html.H6('Experiment List',style={'textAlign':'left'}),width=12)
    ),
    dbc.Row(
        dbc.Col(
            dash_table.DataTable(
            id='experiments_table',
            style_as_list_view=True,
                style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },

        )
            ,width=12)
    ),
    ])

def details_page(ex_id):
    return html.Div([
    dbc.Row([
        dbc.Col(html.H6('Experiment {}'.format(ex_id),style={'textAlign':'left'}),width=4),
        dbc.Col(
            dcc.Dropdown(id='sensor_selection',
            ),
            
        width=4)],
        justify="between"
    ),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='sensor_table',
                style_as_list_view=True,
                style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },
            ),width=6
        ),
        dbc.Col(
            dbc.Row([
                dbc.Col(
                    html.Div(id='graph_one')
                ,width=12),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(id='graph_two')
                ,width=12)
            ]),
        width=6)]
    ),
])



app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Dropdown(id = 'page_selection',
                    options=get_experiment_metadata(),
                    value=0
                )),
            width=4
        ),
        ]
    ),
    dbc.Row(
        dbc.Col(
            html.Div(id='page-content'),width=12
        )
    ),
    
    html.Div(id='hidden_data',style={'display':'none'}),
    html.Div(id='hidden_two',style={'display':'none'})
])




@app.callback(Output('hidden_data', 'children'), 
[Input('page_selection', 'value')])
def clean_data(value):
     datasets = get_experiment_results(value)
     return json.dumps(datasets)

# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('page_selection', 'value')])
def display_page(value):
    print(value)
    if value == 0:
        return main_page()
    else:
        return details_page(value)


@app.callback(
    Output('experiments_table','columns'),
    [Input('hidden_data', 'children')])
def update_graph_1(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    df = pd.read_json(datasets['metadata'], orient='split')
    columns=[{"name": i, "id": i} for i in df.columns]
    return columns

@app.callback(
    Output('experiments_table', 'data'),
    [Input('hidden_data', 'children')])
def update_graph_1(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    df = pd.read_json(datasets['metadata'], orient='split')
    data=df.to_dict("rows")
    return data




@app.callback(
    Output('sensor_table','columns'),
    [Input('hidden_data', 'children')])
def update_sensor_table_col(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    df = pd.read_json(datasets['current_results'], orient='split')
    df= df[['sensor_description','asset_category','mean','new_mean','sd','new_sd','statistic','pvalue']]
    columns=[{"name": i, "id": i} for i in df.columns]
    return columns

@app.callback(
    Output('sensor_table', 'data'),
    [Input('hidden_data', 'children')])
def update_sensor_table(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    df = pd.read_json(datasets['current_results'], orient='split')
    df= df[['sensor_description','asset_category','mean','new_mean','sd','new_sd','statistic','pvalue']].round(2)
    data=df.to_dict("rows")
    return data








@app.callback(
    Output('sensor_selection', 'options'),
    [Input('hidden_data', 'children'),],
    )
def u(jsonified_cleaned_data):
    print('I"M HERE LOOK AT ME22')
    datasets = json.loads(jsonified_cleaned_data)
    print(datasets.keys())
    if 'sensor_list' in datasets.keys():
        df = pd.read_json(datasets['sensor_list'], orient='split')
        df = df.rename(columns={'sensor_id':'value','sensor_description':'label'})
        print(df)
        data=df.to_dict("rows")
        return data
    else:
        return [{'label':'None','value':None}]


@app.callback(
    Output('sensor_selection', 'value'),
    [Input('sensor_selection', 'options'),],
    )
def u(options):

    return options[0]['value']


@app.callback(
    Output('graph_one', 'children'),
    [Input('sensor_selection', 'value')],
    [State('page_selection', 'value')]
    )
def hide_data(sensor_id,experiment_id):
    if experiment_id not in [None,0]:
        SQL = """Select value, time, (case when time > change_date then   'after'
                                                                when time <= change_date then 'before'
                                                                end)as group from 
            ( Select experiment_id, b.sensor_id, sensor_description, change_date, lookback_window, analysis_window,a.asset_category,d.value,d.time from 
            (Select experiment_id, change_date, lookback_window, analysis_window, unnest(assets) as asset_category from whse.dim_experimentation_metadata 
                where id = {} 
            ) a
            inner join sensor_metadata b
            on a.asset_category = b.asset_category and sensor_id = '{}' 
            inner join  whse.agg_hour_sensor_values d
            on b.sensor_id = d.sensor_id and d.time between change_date:: date - lookback_window and change_date:: date + analysis_window 
            ) k
            order by time""" .format(experiment_id, sensor_id)
        engine = db_sql.engine
        df = pd.read_sql(SQL, engine)
        df['value'] = pd.to_numeric(df['value'])
        df['time'] = pd.to_datetime(df['time'])
        df = df.round(2)
        graph1 = dcc.Graph(
            figure=go.Figure(
            data=[
                go.Line(
                    x=df[df['group']=='before']['time'],
                    y=df[df['group']=='before']['value'],
                    name='Before',
                ),
                go.Line(
                    x=df[df['group']=='after']['time'],
                    y=df[df['group']=='after']['value'],
                    name='After',
                ),

            ],
            layout=go.Layout(
                showlegend=True,
                legend=go.layout.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph'
        )

        before = df[df['group']=='before']['value']
        after = df[df['group']=='after']['value']
        hist_data = [before, after]
        group_labels = ['before', 'after']
        bins = (df.value.max() - df.value.min()) / 25
        fig = ff.create_distplot(hist_data, group_labels,bin_size = bins,show_rug=True,show_hist=True)
        graph2 = dcc.Graph(figure=fig)
        return html.Div([dbc.Row(
        dbc.Col(html.Div(graph1)
        )),
        dbc.Row(
            dbc.Col(
                html.Div(graph2)
            )
        )])



     



