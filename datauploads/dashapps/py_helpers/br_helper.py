import json
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from pytz import timezone

import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

tz = timezone('America/Chicago')
inside_style={'backgroundColor':'white','margin':'10px 10px 10px 10px','padding':'5px 5px 5px 5px'}

def log_header(log_name):
    return html.Div([
        dbc.Row([
            dbc.Col(
                html.H3(datetime.now().astimezone(timezone('America/Chicago')).strftime("%Y-%m-%d")),style={'textAlign':'center'}
                ,width=4
            ),
            dbc.Col(
                html.H2(log_name)
                ,style={'textAlign':'center'},
                width=4),
            dbc.Col(
                html.H3(datetime.now().astimezone(timezone('America/Chicago')).strftime("%I:%M %p")),style={'textAlign':'center'}
                ,width=4
            ),]),
            ])



def create_input(x):
    if x['input_type'] in ['number','text']:
        return dbc.Input(type=x['input_type'],
                          id=x['input_id'])
    elif x['input_type'] == 'dropdown':
        return dcc.Dropdown(options=x['input_options'],
                id = x['input_id'])



def create_form(section_title,section_inputs):
    return html.Div([
        html.H4(section_title),
        dbc.Row( form=True,children=[
            dbc.Col(
                dbc.FormGroup(
                    [
                    dbc.Label(i['input_title']),
                    create_input(i)
                    ]
                ),xs=12,sm=6,md=6,lg=3,xl=3
            ) for i in section_inputs]  ) ],style=inside_style)


def submit_button(id):
    return dbc.Button("Submit Data", color="primary", block=True,id=id)
