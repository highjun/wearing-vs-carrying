# Visualization of Step Count Raw Data along with time
import dash
from dash import dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots


import os
import pandas as pd
import datetime as dt

app = dash.Dash(__name__)
cwd = os.getcwd()
user_dir  =os.path.join(cwd,"Data","Users")
users = sorted([file.split(".csv")[0] for file in os.listdir(user_dir)])

color = {'phone': '#1f77b4', 'watch':'#ff7f0e'}
def getPlotlyGraph(uid,date):
    udf = pd.read_csv(os.path.join(user_dir, f"{uid}.csv"), header = 0, index_col= 0)
    udf["timestamp"] = pd.to_datetime(udf["timestamp"])
    udf["weekday"] = udf["timestamp"].dt.weekday
    date  = dt.datetime.strptime(date, '%Y-%m-%d').date()
    start = udf.iloc[0]['timestamp'].date()
    end = udf.iloc[-1]['timestamp'].date()
    if date < start:
        date = start
    elif date > end:
        date = end
    fig = make_subplots(rows=2, cols=1, specs=[[{}], [{}]], 
                        shared_xaxes=True, shared_yaxes=True, 
                        horizontal_spacing=0, vertical_spacing=0)
    datas = []
    for idx, device in enumerate(['phone','watch']):
        datas.append(udf.query("device == @device"))
        hovertemplate = []
        columns = ['step', 'weekday', 'timestamp', 'speed','distance','calorie']
        for row in datas[idx][columns].to_numpy():
            desc = ''
            for cdx, column in enumerate(columns):
                desc += f'{column}: {row[cdx]}<br>\n'
            hovertemplate.append(desc)
        fig.append_trace(
            go.Bar(x=datas[idx]["timestamp"], y= datas[idx]["step"] *(1-2*idx) , orientation='v', showlegend=True, hovertemplate = hovertemplate, name=device,  marker=dict(color= color[device])),
            row = idx+1, col = 1)
    fig.update_yaxes(fixedrange = True, range = [0,200], row=1,col= 1)
    fig.update_yaxes(fixedrange = True, range = [-200,0], row=2,col= 1)
    fig.update_xaxes(range= [date, date + dt.timedelta(days = 1)])
    fig.update_layout(
        yaxis = dict(
            tickmode = 'array',
            tickvals = [0, 100, 200],
            ticktext = [0, 100, 200],
            title = 'Smartphone'
        ),
        yaxis2 = dict(
            tickmode = 'array',
            tickvals = [0, -100, -200],
            ticktext = [0, 100, 200],
            title = 'Wearable'
        )
    )
    return fig, date

app.layout = html.Span(children=[
    dcc.Dropdown(
        id='uid',
        options= [{'label': i, 'value':i} for i in users],
        value = 'P01',
    ),
    dcc.DatePickerSingle(
        id='date',
        min_date_allowed=dt.date(2021, 1, 1),
        max_date_allowed=dt.date(2022, 6, 1),
        initial_visible_month=dt.date(2000, 1, 1),
        date=dt.date(2000,1,1)
    ),
    dcc.Graph(
        id = 'graph',
    )
])
@app.callback(
    [Output("graph", "figure"),
    Output('date','date')],
    Input("uid", "value"),
    Input('date', 'date')
)
def cb_render(uid, date):
    graph,date = getPlotlyGraph(uid,date)
    return graph, date

if __name__ == '__main__':
    app.run_server(debug=True)