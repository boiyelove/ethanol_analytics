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

app = DjangoDash('6',external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

app.layout = html.Div(children=[
'TESTING'
])

