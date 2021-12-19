#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import pandas as pd

with open('test1.pkl', 'rb') as handle:
    df_dic2 = pickle.load(handle)

with open('test2.pkl', 'rb') as handle:
    candle_dic = pickle.load(handle)


# In[11]:


today = df_dic2['FB'].index[-4]
# next_date30 = df_dic['FB'].index[-1]
next_days = pd.date_range(today, periods=4, freq='B')
next_date = next_days[1]
next_date3 = next_days[-1]
# daysBTW = int(str(next_date3-today)[:2])+1

# print(today)
# print(next_date)
# print(next_date3)


# In[ ]:


import dash ## local
#from jupyter_dash import JupyterDash # colab
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import dash_auth
from dash.dependencies import Input, Output

USERNAME_PASSWORD_PAIRS = [['prototypeStockPredict', 'StockAI2020!'], ['prototypeStockPredict2', 'StockAI2020!2'], ['prototypeStockPredict3', 'StockAI2020!3']]


options_list = [
    {'label': 'Apple', 'value': 'AAPL'},
    {'label': 'Amazon', 'value': 'AMZN'},
    {'label': 'Facebook', 'value': 'FB'},
    {'label': 'Google', 'value': 'GOOG'},
    {'label': 'Microsoft', 'value': 'MSFT'},
    {'label': 'Neflix', 'value': 'NFLX'},
    {'label': 'XLK', 'value': 'XLK'},
    {'label': 'QQQ', 'value': 'QQQ'}
]

date_options_list = [
    {'label': '2 Days', 'value': -5},
    {'label': '5 Days', 'value': -8},
    {'label': '1 Month', 'value': -27},
    {'label': '3 Month', 'value': -69},
    {'label': '6 Month', 'value': -133},
    {'label': 'All', 'value': 'all'}
]


# Initialize the app
app = dash.Dash(__name__) ## local
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
#app = JupyterDash(__name__) # colab
app.config.suppress_callback_exceptions = True
server = app.server

app.layout = html.Div([
# Setting the main title of the Dashboard
    html.H1("Stock Price Prediction", style={"textAlign": "center"}),

    html.Div([
        html.H1("Please select stock and time period.",
            style={'textAlign': 'center'}),
            # Adding the first dropdown menu and the subsequent time-series graph
            dcc.Dropdown(id='stock_select',
                options=options_list, # multi=True,
                value='AAPL',
                style={"display": "block", "margin-left": "auto",
                    "margin-right": "auto", "width": "60%"}),

            dcc.Dropdown(id='date_select',
                options=date_options_list, # multi=True,
                value=-69,
                style={"display": "block", "margin-left": "auto",
                    "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id='basicGraph'),
#                 dcc.Graph(id='pindexGraph1'),
                dcc.Graph(id='pindexGraph2'),
                dcc.Graph(id='predictionGraph'),
                dcc.Graph(id='volumeGraph'),

            ])
])

@app.callback(Output('basicGraph', 'figure'),
              [Input('stock_select', 'value'), Input('date_select', 'value')])

def update_graph(selected_dropdown, selected_date):

    trace1 = []
    trace2 = []
    trace3 = []
    trace4 = []
    trace5 = []
    trace6 = []
    trace7 = []
    trace8 = []

    if selected_date == 'all':
        result_frame = df_dic2[selected_dropdown].copy()
        candle_frame = candle_dic[selected_dropdown].copy()
    else:
        result_frame = df_dic2[selected_dropdown].copy().iloc[selected_date:]
        candle_frame = candle_dic[selected_dropdown].copy().iloc[selected_date:]

    trace1.append(
      go.Candlestick(x=candle_frame.index, visible='legendonly',
                     open=candle_frame.Open,
                     high=candle_frame.High,
                     low=candle_frame.Low,
                     close=candle_frame.Close,
                     name=f'Candlestick'))

    trace2.append(
      go.Scatter(x=result_frame.index,
                 y=result_frame.MA,
                 mode='lines', opacity=0.8, #fill="tonexty",
                 name=f'MA', #,textposition='bottom center',
                line = dict(color='chocolate')))

    trace3.append(
      go.Scatter(x=result_frame.index,
                 y=result_frame.PMA,
                 mode='lines', opacity=0.9, #fill='tonexty',
                 name=f'PMA',#textposition='bottom center',
                 line = dict(color='blue')))

    trace4.append(
      go.Scatter(x=result_frame.index,
                 y=result_frame.Open, visible='legendonly',
                 mode='lines', opacity=0.8, line=dict(color="orange", width=4, dash='dot'),
                 name=f'Open')) #,textposition='bottom center'))

    trace5.append(
      go.Scatter(x=result_frame.index,
                 y=result_frame.Close, visible='legendonly',
                 mode='lines', opacity=0.6, line=dict(color="teal", width=4, dash='dash'),
                 name=f'Close')) #,textposition='bottom center'))

    trace6.append(
      go.Scatter(x=result_frame.index,
                 y=result_frame.Close_Pred1, visible='legendonly',
                 mode='lines', opacity=0.8, line_color= "cyan",
                 name=f'Predict 1day')) #,textposition='bottom center'))
    trace7.append(
      go.Scatter(x=result_frame.index,
                 y=result_frame.Close_Pred2, visible='legendonly',
                 mode='lines', opacity=0.8, line_color= "magenta",
                 name=f'Predict 2days')) #,textposition='bottom center'))

    trace8.append(
      go.Scatter(x=result_frame.index,
                 y=result_frame.Close_Pred3, visible='legendonly',
                 mode='lines', opacity=0.8, line_color= "navy",
                 name=f'Predict 3days')) #,textposition='bottom center'))

    traces = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8]

    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout( #colorway=["#5E0DAC", '#800000', '#FFA500',
                                    #        '#00FFFF', '#FF00FF','#0000FF'],
            hovermode='x unified',
            height=500,
            margin=dict(
#             t=10, # top margin: 30px, you want to leave around 30 pixels to
#               # display the modebar above the graph.
            b=20, # bottom margin: 10px
#             l=40, # left margin: 10px
#             r=40, # right margin: 10px
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1),
             title=f"{selected_dropdown}", xaxis={'rangeslider': {'visible': False}, 'type': 'date'},
#             yaxis =  {"title":"Price", "range":[min(result_frame.Open)*0.75,max(result_frame.Open*1.1)],
#                       'fixedrange': False},


#             yaxis2={"title":"Volume", "side":"right", "overlaying":"y",
#                     "range":[min(result_frame.Volume),max(result_frame.Volume)*4]},


             shapes=[
                    dict(
                        type="rect",
                        xref="x",
                        yref="paper",
                        x0=next_date+pd.DateOffset(-1),
                        y0="0",
                        x1=result_frame.index[-1],
                        y1="1",
                        fillcolor="lightgray",
                        opacity=0.4,
                        line_width=0,
                        layer="below"
                    ),
                    ],

# #             xaxis={#"title":"Date",
# # #                    'rangeselector': {'buttons': list([
# # #                        {'count': daysBTW, 'label': '1D', 'step': 'day','stepmode': 'backward'},
# # #                        {'count': daysBTW+6, 'label': '5D', 'step': 'day', 'stepmode': 'backward'},
# # #                        {'count': daysBTW+30, 'label': '1M', 'step': 'day', 'stepmode': 'backward'},
# # #                        {'count': daysBTW+92, 'label': '3M', 'step': 'day', 'stepmode': 'backward'},
# # #                        {'count': daysBTW+183, 'label': '6M', 'step': 'day','stepmode': 'backward'},
# # #                        {'step': 'all'}])},
# #                    'rangeslider': {'visible': False},
# #                    'type': 'date'},


              )}

    return figure

@app.callback(Output('pindexGraph2', 'figure'),
              [Input('stock_select', 'value'), Input('date_select', 'value')])

def update_graph4(selected_dropdown, selected_date):

    trace21 = []

    if selected_date == 'all':
        result_frame = df_dic2[selected_dropdown].copy()
    else:
        result_frame = df_dic2[selected_dropdown].copy().iloc[selected_date:]


    trace21.append(
      go.Bar(x=result_frame.index, y=result_frame.constant2,opacity=0.7,
                      name=f'Pindex2',marker_color=result_frame.PIndex_color2))


    traces = [trace21]

    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout( #colorway=["#5E0DAC", '#800000', '#FFA500',
                                    #        '#00FFFF', '#FF00FF','#0000FF'],
            height=10,
            margin=dict(
            t=0, # top margin: 30px, you want to leave around 30 pixels to
              # display the modebar above the graph.
            b=0, # bottom margin: 10px
#             l=40, # left margin: 10px
#             r=40, # right margin: 10px
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1),
             title=f"{selected_dropdown} Pindex2",
             xaxis={'rangeslider': {'visible': False}, 'type': 'date'},
             yaxis = {'showticklabels': False, 'showgrid': False},
#             yaxis =  {"title":"Price", "range":[min(result_frame[:-30].Open)*0.75,max(result_frame[:-30].Open*1.1)],
#                       'fixedrange': False},

                  shapes=[
                    dict(
                        type="rect",
                        xref="x",
                        yref="paper",
                        x0=next_date+pd.DateOffset(-1),
                        y0="0",
                        x1=result_frame.index[-1],
                        y1="1",
                        fillcolor="lightgray",
                        opacity=0.4,
                        line_width=0,
                        layer="below"
                    ),
                    ],

#             yaxis2={"title":"Volume", "side":"right", "overlaying":"y",
#                     "range":[min(result_frame[:-30].Volume),max(result_frame[:-30].Volume)*4]},
              )}


    return figure

@app.callback(Output('predictionGraph', 'figure'),
              [Input('stock_select', 'value'), Input('date_select', 'value')])
def update_graph3(selected_dropdown, selected_date):

    trace6 = []
    trace7 = []
    trace8 = []

    trace11 = []

    if selected_date == 'all':
        result_frame = df_dic2[selected_dropdown].copy()
    else:
        result_frame = df_dic2[selected_dropdown].copy().iloc[selected_date:]


    trace6.append(
      go.Scatter(x=result_frame.index,
                 y=result_frame.Close_Pred1, #visible='legendonly',
                 mode='lines', opacity=0.8, line_color= "cyan",
                 name=f'Predict 1day')) #,textposition='bottom center'))
    trace7.append(
      go.Scatter(x=result_frame.index,
                 y=result_frame.Close_Pred2, #visible='legendonly',
                 mode='lines', opacity=0.8, line_color= "magenta",
                 name=f'Predict 2days')) #,textposition='bottom center'))

    trace8.append(
      go.Scatter(x=result_frame.index,
                 y=result_frame.Close_Pred3, #visible='legendonly',
                 mode='lines', opacity=0.8, line_color= "navy",
                 name=f'Predict 3days')) #,textposition='bottom center'))

    # next day candle: 'Open_Pred', 'Close_Pred1',
    Open = list()
    Close = list()
    High = list()
    Low = list()

    hovertext = list()

    for date in result_frame.index:
        if date != next_date:
            Open.append(None)
            Close.append(None)
            High.append(None)
            Low.append(None)
            hovertext.append(None)
        else:
            Open.append(result_frame.loc[next_date].Open_Pred)
            Close.append(result_frame.loc[next_date].Close_Pred1)
            High.append(max(result_frame.loc[next_date].Open_Pred,result_frame.loc[next_date].Close_Pred1))
            Low.append(min(result_frame.loc[next_date].Open_Pred,result_frame.loc[next_date].Close_Pred1))
            hovertext.append('Open: '+str(result_frame.loc[next_date].Open_Pred)+'<br>Close: '+str(result_frame.loc[next_date].Close_Pred1))

    trace11.append(
      go.Candlestick(x=result_frame.index, visible='legendonly',
                     open=Open,
                     high=High,
                     low=Low,
                     close=Close, opacity=0.7,
                     #increasing_line_color= 'green', decreasing_line_color= 'red',
                     name=f'next candle',
                     text = hovertext,
                     hoverinfo='text'))

    traces = [trace6, trace7, trace8, trace11]

    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout( #colorway=["#5E0DAC", '#800000', '#FFA500',
                                    #        '#00FFFF', '#FF00FF','#0000FF'],
            hovermode='x unified',
            height=300,

            margin=dict(
            t=50, # top margin: 30px, you want to leave around 30 pixels to
#               # display the modebar above the graph.
            b=0, # bottom margin: 10px
#             l=40, # left margin: 10px
#             r=40, # right margin: 10px
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1),
             #title=f"{selected_dropdown}",
             xaxis={'rangeslider': {'visible': False}, 'type': 'date'},

#             yaxis =  {"title":"Price", "range":[min(result_frame[:-30].Open)*0.75,max(result_frame[:-30].Open*1.1)],
#                       'fixedrange': False},

                  shapes=[
                    dict(
                        type="rect",
                        xref="x",
                        yref="paper",
                        x0=next_date+pd.DateOffset(-1),
                        y0="0",
                        x1=result_frame.index[-1],
                        y1="1",
                        fillcolor="lightgray",
                        opacity=0.4,
                        line_width=0,
                        layer="below"
                    ),
                    ],

#             yaxis2={"title":"Volume", "side":"right", "overlaying":"y",
#                     "range":[min(result_frame[:-30].Volume),max(result_frame[:-30].Volume)*4]},
              )}


    return figure

@app.callback(Output('volumeGraph', 'figure'),
              [Input('stock_select', 'value'), Input('date_select', 'value')])

def update_graph2(selected_dropdown, selected_date):

    trace10 = []


    if selected_date == 'all':
        result_frame = df_dic2[selected_dropdown].copy()
    else:
        result_frame = df_dic2[selected_dropdown].copy().iloc[selected_date:]



    trace10.append(
      go.Bar(x=result_frame.index, y=result_frame.Volume,opacity=0.7,
                      name=f'Volume',marker_color=result_frame.colors))


    traces = [trace10]

    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout( #colorway=["#5E0DAC", '#800000', '#FFA500',
                                    #        '#00FFFF', '#FF00FF','#0000FF'],
            height=300,
            margin=dict(
            t=50, # top margin: 30px, you want to leave around 30 pixels to
#               # display the modebar above the graph.
#             b=0, # bottom margin: 10px
#             l=40, # left margin: 10px
#             r=40, # right margin: 10px
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1),

             xaxis={'rangeslider': {'visible': False}, 'type': 'date', "title": f"{selected_dropdown} Volume"},

#             yaxis =  {"title":"Price", "range":[min(result_frame[:-30].Open)*0.75,max(result_frame[:-30].Open*1.1)],
#                       'fixedrange': False},

                  shapes=[
                    dict(
                        type="rect",
                        xref="x",
                        yref="paper",
                        x0=next_date+pd.DateOffset(-1),
                        y0="0",
                        x1=result_frame.index[-1],
                        y1="1",
                        fillcolor="lightgray",
                        opacity=0.4,
                        line_width=0,
                        layer="below"
                    ),
                    ],

#             yaxis2={"title":"Volume", "side":"right", "overlaying":"y",
#                     "range":[min(result_frame[:-30].Volume),max(result_frame[:-30].Volume)*4]},
              )}


    return figure

# Run the app
#app.run_server(mode='inline')  # colab
if __name__ == '__main__':
    app.run_server(debug=True)
