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

phone_color = "#ff7f0e"
watch_color = "#1f77b4"
diff_color = "#7f7f7f"

df = pd.read_excel("../Preprocess/all_user.xlsx", index_col  = 0)

def getPlotlyGraph(name, input_timestamp):
    input_timestamp = dt.datetime.strptime(input_timestamp,"%Y-%m-%d")

    step_count = df.query(f"user == '{name}'")

    # overall plots
    watch_step = step_count[step_count["device"] == "watch"]
    watch_step["step"] = [ -step  for step in watch_step["step"]]
    phone_step = step_count[step_count["device"] == "phone"]
    overall = make_subplots(rows=2, cols=1, specs=[[{}], [{}]], shared_xaxes=True,
                        shared_yaxes=True, horizontal_spacing=0, vertical_spacing=0)
    hovertemplate = []
    for idx, row in phone_step.iterrows():
        hovertemplate.append(f"Time: {row['timestamp']} <br>Step: {row['step']}")
    overall.append_trace(go.Bar(x=phone_step["timestamp"], y= phone_step["step"] , orientation='v', showlegend=True, hovertemplate = hovertemplate, name="phone",marker_color = phone_color), 1, 1)
    hovertemplate = []
    for idx, row in watch_step.iterrows():
        hovertemplate.append(f"Time: {row['timestamp']} <br>Step: {row['step']}")
    overall.append_trace(go.Bar(x=watch_step["timestamp"], y= watch_step["step"], orientation='v', showlegend=True, hovertemplate = hovertemplate, name="watch", marker_color = watch_color), 2, 1)
    overall.update_yaxes(fixedrange = True,range = [0,150], row=1,col= 1)
    overall.update_yaxes(fixedrange = True,range = [-150,0], row=2,col= 1)
    overall.update_xaxes(range= [input_timestamp, input_timestamp + dt.timedelta(days = 1)])
    return overall

app.layout = html.Div(children=[
    dcc.Dropdown(
        id='input_name',
        options= [{'label': i, 'value':i} for i in sorted(os.listdir("../Raws"))],
        value='001_andys600'
    ),
    dcc.DatePickerSingle(
        id='timestamp',
        min_date_allowed=dt.date(2021, 7, 1),
        max_date_allowed=dt.date(2021, 8, 31),
        initial_visible_month=dt.date(2021, 8, 1),
        date = dt.date(2021,8,1)
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