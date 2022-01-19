# Step per min Visualization for 1 Participants
import dash
from dash import dcc
from dash import  html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output

import pandas as pd
import datetime as dt
import numpy as np
import os

app = dash.Dash(__name__)
cwd = os.getcwd()
data_path = os.path.join(cwd,"Data","integrated.csv")
user_dir  =os.path.join(cwd,"Data","Users")
# df = pd.read_csv(data_path,header = 0, index_col= 0)
# df["timestamp"] = pd.to_datetime(df["timestamp"])

users = sorted([file.split(".csv")[0] for file in os.listdir(user_dir)])

def getPlotlyGraph(user):
    # user_df = df.query(f"users == '{user}'")
    user_df = pd.read_csv(os.path.join(user_dir, f"{user}.csv"), header = 0, index_col= 0)
    user_df["timestamp"] = pd.to_datetime(user_df["timestamp"])
    user_df["weekday"] = user_df["timestamp"].dt.weekday

    date = user_df.iloc[0]["timestamp"].date()
    watch_step = user_df.query("device == 'watch'")
    phone_step = user_df.query("device == 'phone'")

    overall = make_subplots(rows=2, cols=1, specs=[[{}], [{}]], shared_xaxes=True, shared_yaxes=True, horizontal_spacing=0, vertical_spacing=0)
    hovertemplate = []
    for _, row in phone_step.iterrows():
        hovertemplate.append(f'''
        weekday: {row["weekday"]}<br>
        Time: {row['timestamp']}<br>
        Step: {row['step']} <br>
        Speed: {row['speed']} <br>
        Distance: {row['distance']} <br>
        Calorie: {row['calorie']}
        ''')
    overall.append_trace(go.Bar(x=phone_step["timestamp"], y= phone_step["step"] , orientation='v', showlegend=True, hovertemplate = hovertemplate, name="phone",  marker=dict(
        color='#1f77b4',
    )), 1, 1)
    hovertemplate = []
    for _, row in watch_step.iterrows():
        hovertemplate.append(f'''
        weekday: {row["weekday"]}<br>
        Time: {row['timestamp']} <br>
        Step: {row['step']} <br>
        Speed: {row['speed']} <br>
        Distance: {row['distance']} <br>
        Calorie: {row['calorie']}
        ''')
    overall.append_trace(go.Bar(x=watch_step["timestamp"], y=-1* np.array(watch_step["step"]), orientation='v', showlegend=True, hovertemplate = hovertemplate, name="watch",  marker=dict(
        color='#ff7f0e',
    )), 2, 1)
    overall.update_yaxes(fixedrange = True,range = [0,150], row=1,col= 1)
    overall.update_yaxes(fixedrange = True,range = [-150,0], row=2,col= 1)
    overall.update_xaxes(range= [date, date + dt.timedelta(days = 1)])
    return overall

app.layout = html.Div(children=[
    dcc.Dropdown(
        id='input_name',
        options= [{'label': i, 'value':i} for i in users],
        value = '1004jeje',
    ),
    dcc.Graph(
        id = 'graph',
    )
])
@app.callback(
    Output("graph", "figure"),
    Input("input_name", "value"),
)
def cb_render(input_name):
    graph = getPlotlyGraph(input_name)
    return graph

if __name__ == '__main__':
    app.run_server(debug=True) 