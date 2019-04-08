import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import json
import dash_bootstrap_components as dbc
from .py_helpers import db_sql, br_helper
from django_plotly_dash import DjangoDash
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from datetime import datetime
from pytz import timezone
tz = timezone('America/Chicago')

app = DjangoDash('5',external_stylesheets=[dbc.themes.BOOTSTRAP])

inside_style={'backgroundColor':'white','margin':'10px 10px 10px 10px','padding':'5px 5px 5px 5px'}

heading = [{
                    'input_title':'Time',
                    'input_type':'dropdown',
                    'input_options':[{'label':'7:00 AM','value':'7'},{'label':'9:00 AM','value':'9'},
                    {'label':'11:00 AM','value':'11'},{'label':'1:00 PM','value':'13'},
                    {'label':'3:00 PM','value':'15'},{'label':'5:00 PM','value':'17'}],
                    'input_id':'board_reading_5_heading_0',
                },
                {
                    'input_title':'Shift',
                    'input_type':'number',
                    'input_id':'board_reading_5_heading_1',
                },
                {
                    'input_title':'Supervisor',
                    'input_type':'dropdown',
                    'input_options':[{'label':'Ron D','value':'ron'},{'label':'Jarrod P','value':'jarrod'},],
                    'input_id':'board_reading_5_heading_2',
                },

]



beer_column = [{
                    'input_title':'Feed Rate',
                    'input_type':'number',
                    'input_id':'board_reading_5_beer_0',
                },
                {
                    'input_title':'Feed Temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_beer_1',
                },
                {
                    'input_title':'Bottom Temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_beer_2',
                },
                {
                    'input_title':'Top Pressure',
                    'input_type':'number',
                    'input_id':'board_reading_5_beer_3',
                },
                {
                    'input_title':'Bottom Pressure',
                    'input_type':'number',
                    'input_id':'board_reading_5_beer_4',
                },
        ]

rectifier = [
{
                    'input_title':'Differential Temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_rectifier_0',
                },
                {
                    'input_title':'Bottom Presure',
                    'input_type':'number',
                    'input_id':'board_reading_5_rectifier_1',
                },
                {
                    'input_title':'Reflux Rate',
                    'input_type':'number',
                    'input_id':'board_reading_5_rectifier_2',
                },
                {
                    'input_title':'Draw Rate',
                    'input_type':'number',
                    'input_id':'board_reading_5_rectifier_3',
                },
                {
                    'input_title':'190 proof',
                    'input_type':'number',
                    'input_id':'board_reading_5_rectifier_4',
                },
]

side_stripper = [
{
                    'input_title':'Mid Temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_side_stripper_0',
                },
                {
                    'input_title':'Bottom Temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_side_stripper_1',
                },
                {
                    'input_title':'Steam Valve',
                    'input_type':'number',
                    'input_id':'board_reading_5_side_stripper_2',
                },
                {
                    'input_title':'Bottom Pressure',
                    'input_type':'number',
                    'input_id':'board_reading_5_side_stripper_3',
                },
]
sieve = [
                {
                    'input_title':'Feed Temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_sieve_0',
                },
                {
                    'input_title':'Feed GPM',
                    'input_type':'number',
                    'input_id':'board_reading_5_sieve_1',
                },
                {
                    'input_title':'Back PSI sp',
                    'input_type':'number',
                    'input_id':'board_reading_5_sieve_2',
                },
                {
                    'input_title':'Outlet Temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_sieve_3',
                },
                                {
                    'input_title':'Sieve Proof',
                    'input_type':'number',
                    'input_id':'board_reading_5_sieve_4',
                },
                {
                    'input_title':'Karl Fischer',
                    'input_type':'number',
                    'input_id':'board_reading_5_sieve_5',
                },
                {
                    'input_title':'Regan Proof',
                    'input_type':'number',
                    'input_id':'board_reading_5_sieve_6',
                },
]

tanks = [
                    {
                    'input_title':'Total Oil Production',
                    'input_type':'number',
                    'input_id':'board_reading_5_tank_0',
                },
                {
                    'input_title':'Thin Stillage Level',
                    'input_type':'number',
                    'input_id':'board_reading_5_tank_1',
                },
                {
                    'input_title':'Syrup Tank - 5301 Level',
                    'input_type':'number',
                    'input_id':'board_reading_5_tank_2',
                },
                                {
                    'input_title':'Syrup Tank - 5310 Level',
                    'input_type':'number',
                    'input_id':'board_reading_5_tank_3',
                },
                                {
                    'input_title':'Syrup Tank - 5305 Level',
                    'input_type':'number',
                    'input_id':'board_reading_5_tank_4',
                },
                                {
                    'input_title':'Syrup Tank - 620 Level',
                    'input_type':'number',
                    'input_id':'board_reading_5_tank_5',
                },
]

tri_canter = [{
                    'input_title':'Spin Loss',
                    'input_type':'number',
                    'input_id':'board_reading_5_tri_canter_0',
                },
                {
                    'input_title':'Impeller Size',
                    'input_type':'number',
                    'input_id':'board_reading_5_tri_canter_1',
                },]

centrifuge = [{
                    'input_title':'Centrifuge 1 - Amps',
                    'input_type':'number',
                    'input_id':'board_reading_5_centrifuge_0',
                },
                {
                    'input_title':'Centrifuge 1 - cake Moisture',
                    'input_type':'number',
                    'input_id':'board_reading_5_centrifuge_1',
                },
                {
                    'input_title':'Centrifuge 2 - Amps',
                    'input_type':'number',
                    'input_id':'board_reading_5_centrifuge_2',
                },
                {
                    'input_title':'Centrifuge 2 - cake Moisture',
                    'input_type':'number',
                    'input_id':'board_reading_5_centrifuge_3',
                },
                {
                    'input_title':'Centrifuge 3 - Amps',
                    'input_type':'number',
                    'input_id':'board_reading_5_centrifuge_4',
                },
                {
                    'input_title':'Centrifuge 3 - cake Moisture',
                    'input_type':'number',
                    'input_id':'board_reading_5_centrifuge_5',
                },
                {
                    'input_title':'Centrifuge 4 - Amps',
                    'input_type':'number',
                    'input_id':'board_reading_5_centrifuge_6',
                },
                {
                    'input_title':'Centrifuge 4 - cake Moisture',
                    'input_type':'number',
                    'input_id':'board_reading_5_centrifuge_7',
                },
                {
                    'input_title':'Total GPM',
                    'input_type':'number',
                    'input_id':'board_reading_5_centrifuge_8',
                },]

dryer=[
    {
                    'input_title':'Dryer A - outlet temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_dryer_0',
                },
                {
                    'input_title':'Dryer A - outlet moisture',
                    'input_type':'number',
                    'input_id':'board_reading_5_dryer_1',
                },
                {
                    'input_title':'Dryer A - Syrup Rate',
                    'input_type':'number',
                    'input_id':'board_reading_5_dryer_2',
                },
                {
                    'input_title':'Dryer B - outlet temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_dryer_3',
                },
                {
                    'input_title':'Dryer B - outlet moisture',
                    'input_type':'number',
                    'input_id':'board_reading_5_dryer_4',
                },
                {
                    'input_title':'Dryer B - Syrup Rate',
                    'input_type':'number',
                    'input_id':'board_reading_5_dryer_5',
                },
                {
                    'input_title':'Dryer B - waste cip gpm',
                    'input_type':'number',
                    'input_id':'board_reading_5_dryer_6',
                },
                {
                    'input_title':'Dryer C - outlet temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_dryer_7',
                },
                {
                    'input_title':'Dryer C - outlet moisture',
                    'input_type':'number',
                    'input_id':'board_reading_5_dryer_8',
                },
                {
                    'input_title':'Dryer C - Syrup Rate',
                    'input_type':'number',
                    'input_id':'board_reading_5_dryer_9',
                },
]

fluid_bed =[
                {
                    'input_title':'Outlet Moisture',
                    'input_type':'number',
                    'input_id':'board_reading_5_fluid_bed_0',
                },
                {
                    'input_title':'color',
                    'input_type':'number',
                    'input_id':'board_reading_5_fluid_bed_1',
                },
                {
                    'input_title':'PDIT-5601-2',
                    'input_type':'number',
                    'input_id':'board_reading_5_fluid_bed_2',
                },
]

utilities = [
                {
                    'input_title':'T.O Temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_utilities_0',
                },
                {
                    'input_title':'Turbine Gas Flow',
                    'input_type':'number',
                    'input_id':'board_reading_5_utilities_1',
                },
                {
                    'input_title':'Cooling Tower - Level',
                    'input_type':'number',
                    'input_id':'board_reading_5_utilities_2',
                },
                {
                    'input_title':'Cooling Tower - Temp',
                    'input_type':'number',
                    'input_id':'board_reading_5_utilities_3',
                },
                {
                    'input_title':'Plant Air Pressure',
                    'input_type':'number',
                    'input_id':'board_reading_5_utilities_4',
                }

]

ids_list = ['board_reading_5_heading_0',
 'board_reading_5_heading_1',
 'board_reading_5_heading_2',
 'board_reading_5_beer_0',
 'board_reading_5_beer_1',
 'board_reading_5_beer_2',
 'board_reading_5_beer_3',
 'board_reading_5_beer_4',
 'board_reading_5_rectifier_0',
 'board_reading_5_rectifier_1',
 'board_reading_5_rectifier_2',
 'board_reading_5_rectifier_3',
 'board_reading_5_rectifier_4',
 'board_reading_5_side_stripper_0',
 'board_reading_5_side_stripper_1',
 'board_reading_5_side_stripper_2',
 'board_reading_5_side_stripper_3',
 'board_reading_5_sieve_0',
 'board_reading_5_sieve_1',
 'board_reading_5_sieve_2',
 'board_reading_5_sieve_3',
 'board_reading_5_sieve_4',
 'board_reading_5_sieve_5',
 'board_reading_5_sieve_6',
 'board_reading_5_tank_0',
 'board_reading_5_tank_1',
 'board_reading_5_tank_2',
 'board_reading_5_tank_3',
 'board_reading_5_tank_4',
 'board_reading_5_tank_5',
 'board_reading_5_tri_canter_0',
 'board_reading_5_tri_canter_1',
 'board_reading_5_centrifuge_0',
 'board_reading_5_centrifuge_1',
 'board_reading_5_centrifuge_2',
 'board_reading_5_centrifuge_3',
 'board_reading_5_centrifuge_4',
 'board_reading_5_centrifuge_5',
 'board_reading_5_centrifuge_6',
 'board_reading_5_centrifuge_7',
 'board_reading_5_centrifuge_8',
 'board_reading_5_dryer_0',
 'board_reading_5_dryer_1',
 'board_reading_5_dryer_2',
 'board_reading_5_dryer_3',
 'board_reading_5_dryer_4',
 'board_reading_5_dryer_5',
 'board_reading_5_dryer_6',
 'board_reading_5_dryer_7',
 'board_reading_5_dryer_8',
 'board_reading_5_dryer_9',
 'board_reading_5_fluid_bed_0',
 'board_reading_5_fluid_bed_1',
 'board_reading_5_fluid_bed_2',
 'board_reading_5_utilities_0',
 'board_reading_5_utilities_1',
 'board_reading_5_utilities_2',
 'board_reading_5_utilities_3',
 'board_reading_5_utilities_4']

app.layout = html.Div(children=[
    html.Div([
    br_helper.log_header('Board Readings - 2'),
    ],style=inside_style),
        br_helper.create_form(' ',heading),
        br_helper.create_form('Beer Column',beer_column),
        br_helper.create_form('Rectifier',rectifier),
        br_helper.create_form('Side Stripper',side_stripper),
        br_helper.create_form('Sieves',sieve),
        br_helper.create_form('Tanks',tanks),
        br_helper.create_form('Tri Canter',tri_canter),
        br_helper.create_form('Centrifuge',centrifuge),
        br_helper.create_form('Dryer',dryer),
        br_helper.create_form('Fluid Bed Cooler',fluid_bed),
        br_helper.create_form('Utilities',utilities),
        br_helper.submit_button('board_reading_5_submit'),
        html.Div(id='board_readings_5_output')
],style={'backgroundColor':'#f4f5f7','paddingTop':'10px','paddingBottom':'10px'})



@app.callback(
    Output("board_readings_5_output", "children"), [Input('board_reading_5_submit','n_clicks')],
    [State(i,'value') for i in ids_list],
)
def switch_tab(*args):
    if args[0] not in [None,0]:
        df = pd.DataFrame.from_dict(dict(zip(ids_list, args[1:])),orient='index').reset_index().rename(columns={'index':'id',0:'value'})
        df = df[df['value'] != None]
        print(df)
        df.to_sql(schema='stg',name='log_data',con=db_sql.engine,if_exists='append',index=False)