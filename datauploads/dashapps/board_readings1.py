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

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('4',external_stylesheets=[dbc.themes.BOOTSTRAP])
# app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])# external_stylesheets=external_stylesheets)


inside_style={'backgroundColor':'white','margin':'10px 10px 10px 10px','padding':'5px 5px 5px 5px'}
heading = [{
                    'input_title':'Time',
                    'input_type':'dropdown',
                    'input_options':[{'label':'7:00 AM','value':'7'},{'label':'9:00 AM','value':'9'},
                    {'label':'11:00 AM','value':'11'},{'label':'1:00 PM','value':'13'},
                    {'label':'3:00 PM','value':'15'},{'label':'5:00 PM','value':'17'}],
                    'input_id':'board_reading_4_heading_0',
                },
                {
                    'input_title':'Shift',
                    'input_type':'number',
                    'input_id':'board_reading_4_heading_1',
                },
                {
                    'input_title':'Supervisor',
                    'input_type':'dropdown',
                    'input_options':[{'label':'Ron D','value':'ron'},{'label':'Jarrod P','value':'jarrod'},],
                    'input_id':'board_reading_4_heading_2',
                },

]



liq_tank = [{
                    'input_title':'Brix',
                    'input_type':'number',
                    'input_id':'board_reading_4_liq_0',
                },
                {
                    'input_title':'level',
                    'input_type':'number',
                    'input_id':'board_reading_4_liq_1',
                },
                {
                    'input_title':'gpm',
                    'input_type':'number',
                    'input_id':'board_reading_4_liq_2',
                },
        ]



fermentation = [{
                    'input_title':'Ferm 1 Temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_0',
                },
                {
                    'input_title':'Ferm 1 Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_1',
                },
                {
                    'input_title':'Ferm 2 Temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_2',
                },
                {
                    'input_title':'Ferm 2 Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_3',
                },
                {
                    'input_title':'Ferm 3 Temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_4',
                },
                {
                    'input_title':'Ferm 3 Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_5',
                },
                {
                    'input_title':'Ferm 4 Temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_6',
                },
                {
                    'input_title':'Ferm 4 Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_7',
                },
                {
                    'input_title':'Ferm 5 Temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_8',
                },
                {
                    'input_title':'Ferm 5 Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_9',
                },
                {
                    'input_title':'Ferm 6 Temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_10',
                },
                {
                    'input_title':'Ferm 6 Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_11',
                },
                {
                    'input_title':'Ferm 7 Temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_12',
                },
                {
                    'input_title':'Ferm 7 Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_13',
                },
                {
                    'input_title':'Ferm 8 Temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_14',
                },
                {
                    'input_title':'Ferm 8 Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_15',
                },
                {
                    'input_title':'Ferm 9 Temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_16',
                },
                {
                    'input_title':'Ferm 9 Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_17',
                },
                {
                    'input_title':'Ferm 10 Temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_18',
                },
                {
                    'input_title':'Ferm 10 Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_19',
                },
                {
                    'input_title':'Beer Well Level',
                    'input_type':'number',
                    'input_id':'board_reading_4_ferm_20',
                }]




heat_exchanger = [
                {
                    'input_title':'2400 Status',
                    'input_type':'dropdown',
                    'input_options':[{'label':'Online','value':'online'},{'label':'ready','value':'ready'},{'label':'Ready for Cip','value':'ready_for_cip'},
                                    {'label':'Offline','value':'offline'}],
                    'input_id':'board_reading_4_heat_exchanger_0',
                },
                {
                    'input_title':'2400 Hours',
                    'input_type':'text',
                    'input_id':'board_reading_4_heat_exchanger_1',
                },
                {
                    'input_title':'2500 Status',
                    'input_type':'dropdown',
                    'input_options':[{'label':'Online','value':'online'},{'label':'ready','value':'ready'},{'label':'Ready for Cip','value':'ready_for_cip'},
                                    {'label':'Offline','value':'offline'}],
                    'input_id':'board_reading_4_heat_exchanger_2',
                },
                {
                    'input_title':'2500 Hours',
                    'input_type':'text',
                    'input_id':'board_reading_4_heat_exchanger_3',
                },
                {
                    'input_title':'2600 Status',
                    'input_type':'dropdown',
                    'input_options':[{'label':'Online','value':'online'},{'label':'ready','value':'ready'},{'label':'Ready for Cip','value':'ready_for_cip'},
                                    {'label':'Offline','value':'offline'}],
                    'input_id':'board_reading_4_heat_exchanger_4',
                },
                {
                    'input_title':'2600 Hours',
                    'input_type':'text',
                    'input_id':'board_reading_4_heat_exchanger_5',
                },
                {
                    'input_title':'Beer Preheater 4210',
                    'input_type':'dropdown',
                    'input_options':[{'label':'Online','value':'online'},{'label':'ready','value':'ready'},{'label':'Ready for Cip','value':'ready_for_cip'},
                                    {'label':'Offline','value':'offline'}],
                    'input_id':'board_reading_4_heat_exchanger_6',
                },
                {
                    'input_title':'Beer Preheater 4210 Hours',
                    'input_type':'text',
                    'input_id':'board_reading_4_heat_exchanger_7',
                },
                {
                    'input_title':'Beer Preheater 4220',
                    'input_type':'dropdown',
                    'input_options':[{'label':'Online','value':'online'},{'label':'ready','value':'ready'},{'label':'Ready for Cip','value':'ready_for_cip'},
                                    {'label':'Offline','value':'offline'}],
                    'input_id':'board_reading_4_heat_exchanger_8',
                },
                {
                    'input_title':'Beer Preheater 4220 Hours',
                    'input_type':'text',
                    'input_id':'board_reading_4_heat_exchanger_9',
                },
        ]

milling_data = [{
                    'input_title':'FV-1321 %',
                    'input_type':'number',
                    'input_id':'board_reading_4_milling_0',
                },
                {
                    'input_title':'FV-1322 %',
                    'input_type':'number',
                    'input_id':'board_reading_4_milling_1',
                },
                {
                    'input_title':'FV-1323 %',
                    'input_type':'number',
                    'input_id':'board_reading_4_milling_2',
                },
                {
                    'input_title':'FV-1324 %',
                    'input_type':'number',
                    'input_id':'board_reading_4_milling_3',
                },
                {
                    'input_title':'#1 HM amps',
                    'input_type':'number',
                    'input_id':'board_reading_4_milling_4',
                },
                {
                    'input_title':'#2 HM amps',
                    'input_type':'number',
                    'input_id':'board_reading_4_milling_5',
                },
                {
                    'input_title':'#3 HM amps',
                    'input_type':'number',
                    'input_id':'board_reading_4_milling_6',
                }, 
                {
                    'input_title':'#4 HM amps',
                    'input_type':'number',
                    'input_id':'board_reading_4_milling_7',
                },  
                {
                    'input_title':'Total Corn Feed Bu/Min',
                    'input_type':'number',
                    'input_id':'board_reading_4_milling_8',
                },     
                ]


cook_data = [{
                    'input_title':'Cook Water GPM FCV-2210',
                    'input_type':'number',
                    'input_id':'board_reading_4_cook_0',
                },
                {
                    'input_title':'Total Cook Water GPM',
                    'input_type':'number',
                    'input_id':'board_reading_4_cook_1',
                },
                {
                    'input_title':'Cook Water Level LIT-310',
                    'input_type':'number',
                    'input_id':'board_reading_4_cook_2',
                },
                {
                    'input_title':'Cook Water Temp TT-2210-1',
                    'input_type':'number',
                    'input_id':'board_reading_4_cook_3',
                },
                {
                    'input_title':'NH3 Level %',
                    'input_type':'number',
                    'input_id':'board_reading_4_cook_4',
                },
                {
                    'input_title':'NH3 Level %',
                    'input_type':'number',
                    'input_id':'board_reading_4_cook_5',
                },
                ]
slurry_data = [{
                    'input_title':'pH',
                    'input_type':'number',
                    'input_id':'board_reading_4_slurry_0',
                },
                {
                    'input_title':'solids',
                    'input_type':'number',
                    'input_id':'board_reading_4_slurry_1',
                },
                {
                    'input_title':'level',
                    'input_type':'number',
                    'input_id':'board_reading_4_slurry_2',
                },
                {
                    'input_title':'temp',
                    'input_type':'number',
                    'input_id':'board_reading_4_slurry_3',
                },
                {
                    'input_title':'density',
                    'input_type':'number',
                    'input_id':'board_reading_4_slurry_4',
                },
                {
                    'input_title':'backset gpm',
                    'input_type':'number',
                    'input_id':'board_reading_4_slurry_5',
                },
                ]

ids_list = ['board_reading_4_heading_0',
 'board_reading_4_heading_1',
 'board_reading_4_heading_2',
 'board_reading_4_milling_0',
 'board_reading_4_milling_1',
 'board_reading_4_milling_2',
 'board_reading_4_milling_3',
 'board_reading_4_milling_4',
 'board_reading_4_milling_5',
 'board_reading_4_milling_6',
 'board_reading_4_milling_7',
 'board_reading_4_milling_8',
 'board_reading_4_cook_0',
 'board_reading_4_cook_1',
 'board_reading_4_cook_2',
 'board_reading_4_cook_3',
 'board_reading_4_cook_4',
 'board_reading_4_cook_5',
 'board_reading_4_slurry_0',
 'board_reading_4_slurry_1',
 'board_reading_4_slurry_2',
 'board_reading_4_slurry_3',
 'board_reading_4_slurry_4',
 'board_reading_4_slurry_5',
 'board_reading_4_heat_exchanger_0',
 'board_reading_4_heat_exchanger_1',
 'board_reading_4_heat_exchanger_2',
 'board_reading_4_heat_exchanger_3',
 'board_reading_4_heat_exchanger_4',
 'board_reading_4_heat_exchanger_5',
 'board_reading_4_heat_exchanger_6',
 'board_reading_4_heat_exchanger_7',
 'board_reading_4_heat_exchanger_8',
 'board_reading_4_heat_exchanger_9']


app.layout = html.Div(children=[
    html.Div([
    br_helper.log_header('Board Readings - 1'),
    ],style=inside_style),
        br_helper.create_form(' ',heading),
        br_helper.create_form('Milling',milling_data),
        br_helper.create_form('Cook',cook_data),
        br_helper.create_form('Slurry',slurry_data),
        br_helper.create_form('Heat Exchanger',heat_exchanger),
        br_helper.submit_button('board_reading_4_submit'),
        # html.Div(id='board_readings_4_output')
],style={'backgroundColor':'#f4f5f7','paddingTop':'10px','paddingBottom':'10px'})



@app.callback(
    Output("board_reading_4_submit", "color"), [Input('board_reading_4_submit','n_clicks')],
    [State(i,'value') for i in ids_list],
)
def switch_tab(*args):
    if args[0] not in [None,0]:
        df = pd.DataFrame.from_dict(dict(zip(ids_list, args[1:])),orient='index').reset_index().rename(columns={'index':'id',0:'value'})
        df = df.dropna()
        print(df)
        try:
            df.to_sql(schema='stg',name='log_data',con=db_sql.engine,if_exists='append',index=False)
        except:
            return 'danger'
        return 'success'
    else:
        return 'primary'

    