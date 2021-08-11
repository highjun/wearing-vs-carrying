# Step per min Visualization for 1 Participants

from posix import listdir
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output

import glob
import pandas as pd
import datetime as dt
import json
import os

app = dash.Dash(__name__)

with open("../setting.json") as f:
    setting = json.load(f)
data_arr = {}
for name in os.listdir("../Raw"):
    data_arr[name]= pd.read_csv(glob.glob(f"../Raw/{name}/com.samsung.shealth.tracker.pedometer_step_count.*.csv")[0],
        usecols = [0,2,3,4,5,9,10,11,12], header= 0, names = ["duration","run", "walk", "timestamp", "device", "step", "speed","distance", "calorie"], skiprows=[0,1]).fillna(0)
    start = dt.datetime.strptime(setting[name][0],"%Y-%m-%d %H:%M")
    data_arr[name]["device"].replace(to_replace = 230002, value= "watch", inplace = True)
    data_arr[name]["device"].replace(to_replace = 0,value= "phone", inplace = True)
    data_arr[name].sort_values(["timestamp", "device"], inplace = True)
    data_arr[name]["timestamp"] = [ timestamp  + dt.timedelta(hours = 9) for timestamp in pd.to_datetime(data_arr[name]["timestamp"], format="%Y-%m-%d %H:%M")]
    data_arr[name].insert(0, "weekday", [timestamp.weekday() for timestamp in data_arr[name]["timestamp"]])
    data_arr[name].insert(0, "negative_step", [-step for step in data_arr[name]["step"]])

    data_arr[name].insert(0, "hour", [timestamp.hour for timestamp in data_arr[name]["timestamp"]])
    data_arr[name].insert(0, "day", [(timestamp- start).days for timestamp in data_arr[name]["timestamp"]])

def getPlotlyGraph(name, input_timestamp):
    start = dt.datetime.strptime(setting[name][0],"%Y-%m-%d %H:%M")
    input_timestamp = dt.datetime.strptime(input_timestamp,"%Y-%m-%d")

    step_count = data_arr[name]

    # overall plots
    watch_step = step_count[step_count["device"] == "watch"]
    phone_step = step_count[step_count["device"] == "phone"]
    overall = make_subplots(rows=2, cols=1, specs=[[{}], [{}]], shared_xaxes=True,
                        shared_yaxes=True, horizontal_spacing=0, vertical_spacing=0)
    hovertemplate = []
    for idx, row in phone_step.iterrows():
        hovertemplate.append(f"Time: {row['timestamp']} <br>Duration: {row['duration']} <br>Step: {row['step']} <br>Distance: {row['distance']} <br>Speed: {row['speed']}")
    overall.append_trace(go.Bar(x=phone_step["timestamp"], y= phone_step["step"] , orientation='v', showlegend=True, hovertemplate = hovertemplate, name="phone"), 1, 1)
    hovertemplate = []
    for idx, row in watch_step.iterrows():
        hovertemplate.append(f"Time: {row['timestamp']} <br>Duration: {row['duration']} <br>Step: {row['step']} <br>Distance: {row['distance']} <br>Speed: {row['speed']}")
    overall.append_trace(go.Bar(x=watch_step["timestamp"], y= watch_step["negative_step"], orientation='v', showlegend=True, hovertemplate = hovertemplate, name="watch"), 2, 1)
    overall.update_yaxes(fixedrange = True,range = [0,150], row=1,col= 1)
    overall.update_yaxes(fixedrange = True,range = [-150,0], row=2,col= 1)
    overall.update_xaxes(range= [input_timestamp, input_timestamp + dt.timedelta(days = 1)])
    return overall

app.layout = html.Div(children=[
    dcc.Dropdown(
        id='input_name',
        options= [{'label': i, 'value':i} for i in sorted(os.listdir("../Raw"))],
        value='P1'
    ),
    dcc.DatePickerSingle(
        id='timestamp',
        min_date_allowed=dt.date(2020, 8, 5),
        max_date_allowed=dt.date(2021, 9, 19),
        initial_visible_month=dt.date(2021, 8, 5),
        date = dt.date(2020,12,24)
    ),
    dcc.Graph(
        id = 'graph',
    )
])
@app.callback(
    Output("graph", "figure"),
    Input("input_name", "value"),
    Input("timestamp", "date"),
)
def cb_render(input_name,timestamp):
    graph = getPlotlyGraph(input_name, timestamp)
    return graph

if __name__ == '__main__':
    app.run_server(debug=True)