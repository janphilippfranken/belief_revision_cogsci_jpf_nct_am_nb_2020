import time as tm
try:
    import scipy.stats
except:
    tm.sleep(1)
    import scipy.stats
import os
import sys

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from scipy.stats import beta
import random 
import math
from flask_script import Manager, Shell

from app import create_app


sys.path.insert(0, os.path.dirname(__file__))


application = create_app(os.getenv('FLASK_ENV') or 'config.ProductionConfig')
manager = Manager(application)



# these names will be available inside the shell without explicit import
def make_shell_context():
    return dict(app=application)


manager.add_command('shell', Shell(make_context=make_shell_context))















########################################################################
# ADDITIONAL PYTHON FUNCTIONALITIES BELOW
########################################################################


# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 10:03:09 2019

@author: s1667143 (Nikos Theodoropoulos)
"""
# from os import chdir
# chdir(r'Z:\Ph.D\Year 3\Project with Philipp')




# css file for style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



########################################################################
# GENERAL FUNCTIONS FOR CREATING THE DATA AND UPDATING 
########################################################################
# creating some data for a line graph
def create_data():
    x = np.linspace(0.01, .99, 100)
    y = beta.pdf(x, 5, 5)
    return x, y

# convert mu and var to a and b parameters for beta distribution
def estBetaPar(mu, var):
    alpha = mu * (mu * (1 - mu) / var - 1)
    beta = alpha * (1 - mu) / mu
    alpha = max([alpha, 1])
    beta = max([beta, 1])
    return alpha, beta

# transforming data (i.e. update distributions based on sliders)
def transform_data(mu, var):
     x, y = create_data()
     a, b = estBetaPar(mu, var)
     y = beta.pdf(x, a, b)
     return{
            'data': [
                {'x': x[:50], 'y': y[:50], 'type': 'scatter', 'name': 'candidate A', 'fill' : 'tozeroy', 'mode':'lines', 'line':{'color':'purple'}},
                {'x': x[50:], 'y': y[50:], 'type': 'scatter', 'name': 'candidate B', 'fill' : 'tozeroy', 'mode':'lines', 'line':{'color':'orange'}}
            ],
            'layout': {
                    'shapes':[{'type' : 'line', 'x0':0.5, 'x1':0.5, 'y0':0, 'y1':y[49],
                               'line' : {'color':'black', 'width' : 3}
                               }],
    
                'title': 'Candidate A vs. candidate B. Whom do you support?',
                'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
                'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.2, 0, .8], 'ticktext':['A', 'neutral', 'B']}
            }
        }

# create one instance of data 
x, y = create_data()


# log slider creator (input is)
def log_slider(position):
    position = 100 - position
    minp = 1;
    maxp = 100;
    minv = np.log(0.0001)
    maxv = np.log(0.0833)
    scale_adjust = (maxv-minv) / (maxp-minp);
    precision = np.exp(minv + scale_adjust*(position-minp))
    return precision
########################################################################




########################################################################
# CREATING THE PLOTS 
########################################################################


# 1 CUSTOM PLOTS USED IN THE INSTRUCTIONS 
########################################################################
# SINGLE SLIDER PLOT ONLY ALLOWING FOR CHANGES OF THE BELIEF
dashapp_test = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=application, requests_pathname_prefix="/experiments/flask_bel_updating/dashplot_test/", routes_pathname_prefix="/dashplot_test/")

opinion_sld_val=[.5]
def call_backs_plot1():
    @dashapp_test.callback(Output('', 'figure'),
              [Input('slider-updatemode-1', 'value')])
    def display_value(mu):
        x,y=create_data_p1(mu)
        return plot1_str(x,y)
    @dashapp_test.callback(Output("slider-1-value", 'children'),
        [Input('slider-updatemode-1', 'value')])
    def display_value_of_sliders(slid_1_v):
        opinion_sld_val[0] = slid_1_v
        return "{}".format(slid_1_v * 100) 
    
def create_data_p1(mu = .5):
    x = np.repeat(mu, 100)
    y = np.linspace(0.01, .99, 100)
    return x, y

def plot1_str(x, y):
    string_plot = {
            'data': [
                {'x': x, 'y': y, 'type': 'scatter', 'name': 'SF', 'line':{'color':'black'}},
            ],
            'layout': {
                'title': '',
                'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
                'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.01, 0.5, .99], 'ticktext':['Morrison', 'neutral', 'Taylor'], 'range':[0,1]}
            }
        }
    return string_plot

x,y=create_data_p1(mu = .5)

dashapp_test.layout = html.Div(children=[
    html.H1(children=''),
    # the graph
    dcc.Graph(
        id='', style = {'width': 800, 'height': 300},
        figure= plot1_str(x,y),
        config={'displayModeBar': False}),
    # first slider division (mean)
    html.Div(id = "slider-1-container", children = ['Belief',
            dcc.Slider(id='slider-updatemode-1',
    min=0.01,
    max=1,
    step = 0.01,
    updatemode = 'drag',
    included=True,
    value=0.5,
    )
            ], style={'width':800}),
    html.Div(id = "slider-1-value")
             ]# end of list of layout
            )# parentheses for layout
call_backs_plot1()

# SINGLE SLIDER PLOT ONLY ALLOWING FOR CHANGES OF CONFIDENCE AFTER BELIEF HAS BEEN RATED 
dashapp_test_2 = dash.Dash(__name__,
                      reactVar = "react-entry-point2",
                      dash_file = 'dash_renderer2.min.js',
                      rendererID ='_dash-renderer2',
                      dash_config = '_dash-config2',
                      dash_scripts_src = '.*dash[-_]renderer2.*',
                      external_stylesheets=external_stylesheets, server=application, requests_pathname_prefix="/experiments/flask_bel_updating/dashplot_test_2/", routes_pathname_prefix="/dashplot_test_2/")

# creating some data for a line graph
def create_data_p2(mu, var):
    x = np.linspace(0.01, .99, 100)
    a, b = estBetaPar(mu, var)
    y = beta.pdf(x, a, b)
    return x, y

min(x, key=lambda xx:abs(xx-opinion_sld_val[0]))


def plot2_str(x, y):
    string_plot = {
            'data': [
                {'x': x, 'y': y, 'type': 'scatter', 'name': 'SF'},
            ],
            'layout': {'shapes':[{'type' : 'line', 'x0':0.66, 'x1':0.66, 'y0':0, 'y1':y[np.argmin([abs(d) for d in 0.66 - x]  )],
                               'line' : {'color':'black', 'width' : 3}
                               }],
                'title': '',
                'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
                'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.01, 0.5, .99], 'ticktext':['Morrison', 'neutral', 'Taylor'], 'range':[0,1]}
            }
        }
    return string_plot

confidence_sld_val=[1]
def call_backs_plot2():
    @dashapp_test_2.callback(Output('', 'figure'),
              [Input('slider-updatemode-2', 'value')])
    def display_value(var):
        x,y=create_data_p2(mu = 0.66, var = log_slider(var))
        return plot2_str(x,y)
    @dashapp_test_2.callback(Output("slider-2-value", 'children'),
        [Input('slider-updatemode-2', 'value')])
    def display_value_of_sliders(slid_2_v):
        confidence_sld_val[0] = slid_2_v
        return "{}".format(slid_2_v) 
    
x,y=create_data_p2(mu = 0.66, var=log_slider(50))


dashapp_test_2.layout = html.Div(children=[
    html.H1(children=''),
    # the graph
    dcc.Graph(
        id='', style = {'width': 800, 'height': 300},
        figure= plot2_str(x,y),
        config={'displayModeBar': False}),
    # first slider division (mean)
    html.Div(id = "slider-2-container", children = ['Confidence',
            dcc.Slider(id='slider-updatemode-2',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
    )
            ], style={'width':800}),
    html.Div(id = "slider-2-value")
             ]# end of list of layout
            )# parentheses for layout
call_backs_plot2()

########################################################################


# MAIN PLOT 1 used for updating beliefs in the instructions 
######################################################################## 
dashapp_main_1  = dash.Dash(__name__,
                      reactVar = "react-entry-point3",
                      dash_file = 'dash_renderer3.min.js',
                      rendererID ='_dash-renderer3',
                      dash_config = '_dash-config3',
                      dash_scripts_src = '.*dash[-_]renderer3.*',
                      external_stylesheets=external_stylesheets, server=application, requests_pathname_prefix="/experiments/flask_bel_updating/dashapp_main_1/", routes_pathname_prefix="/dashapp_main_1/")

# creating some data for a line graph
def create_data_dashapp_main_1(mu, var):
    x = np.linspace(0.01, .99, 100)
    a, b = estBetaPar(mu, var)
    y = beta.pdf(x, a, b)
    return x, y

min(x, key=lambda xx:abs(xx-opinion_sld_val[0]))


def dashapp_main_1_str(x, y, mu):
    string_plot = {
            'data': [
                {'x': x, 'y': y, 'type': 'scatter', 'name': 'SF'},
            ],
            'layout': {'shapes':[{'type' : 'line', 'x0':mu, 'x1':mu, 'y0':0, 'y1':y[np.argmin([abs(d) for d in mu - x]  )],
                               'line' : {'color':'black', 'width' : 3}
                               }],
                'title': '',
                'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
                'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.01, 0.5, .99], 'ticktext':['Morrison', 'neutral', 'Taylor'], 'range':[0,1]}
            }
        }
    return string_plot

def call_backs_dashapp_main_1():
    @dashapp_main_1.callback(Output('', 'figure'),
              [Input('slider-updatemode-1', 'value'),
              Input('slider-updatemode-2', 'value')])
    def display_value(mu, var):
        x,y=create_data_dashapp_main_1(mu = mu/100, var = log_slider(var))
        return dashapp_main_1_str(x,y, mu/100)

    @dashapp_main_1.callback(Output("slider-1-value", 'children'),
        [Input('slider-updatemode-1', 'value')])
    def display_value_of_sliders(slid_1_v):
        return "{}".format(slid_1_v) 

    @dashapp_main_1.callback(Output("slider-2-value", 'children'),
        [Input('slider-updatemode-2', 'value')])
    def display_value_of_sliders(slid_2_v):
        return "{}".format(slid_2_v) 

x,y=create_data_dashapp_main_1(mu = 66/100, var = log_slider(10))

dashapp_main_1.layout = html.Div(children=[
    html.H1(children=''),
    # the graph
    dcc.Graph(
        id='', style = {'width': 800, 'height': 300},
        figure= plot2_str(x,y),
        config={'displayModeBar': False}),
    # first slider division (mean)
    html.Div(id = "slider-1-container", children = ['Belief',
            dcc.Slider(id='slider-updatemode-1',
    min=1,
    max=99,
    step = 1,
    value=66,
    updatemode = 'drag',
    included=True
          )], style={'width':800}),
          html.Div(id = "slider-1-value"),
    # sec slider division (var)
    html.Div(id = "slider-2-container", children = ['Confidence',
            dcc.Slider(id='slider-updatemode-2',
    min=0,
    max=100,
    step = 1,
    value=10,
    updatemode = 'drag',
    included=True
    )
            ], style={'width':800}),
    html.Div(id = "slider-2-value")
             ]# end of list of layout
            )# parentheses for layout
call_backs_dashapp_main_1()

########################################################################

# MAIN PLOT 2 used for prior beliefs in condition 0
######################################################################## 
dashapp_main_2  = dash.Dash(__name__,
                      reactVar = "react-entry-point4",
                      dash_file = 'dash_renderer4.min.js',
                      rendererID ='_dash-renderer4',
                      dash_config = '_dash-config4',
                      dash_scripts_src = '.*dash[-_]renderer4.*',
                      external_stylesheets=external_stylesheets, server=application, requests_pathname_prefix="/experiments/flask_bel_updating/dashapp_main_2/", routes_pathname_prefix="/dashapp_main_2/")

# creating some data for a line graph
def create_data_dashapp_main_2(mu, var):
    x = np.linspace(0.01, .99, 100)
    a, b = estBetaPar(mu, var)
    y = beta.pdf(x, a, b)
    return x, y

min(x, key=lambda xx:abs(xx-opinion_sld_val[0]))


def dashapp_main_2_str(x, y, mu):
    string_plot = {
            'data': [
                {'x': x, 'y': y, 'type': 'scatter', 'name': 'SF'},
            ],
            'layout': {'shapes':[{'type' : 'line', 'x0':mu, 'x1':mu, 'y0':0, 'y1':y[np.argmin([abs(d) for d in mu - x]  )],
                               'line' : {'color':'black', 'width' : 3}
                               }],
                'title': '',
                'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
                'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.01, 0.5, .99], 'ticktext':['Kri', 'neutral', 'Gor'], 'range':[0,1]}
            }
        }
    return string_plot

def call_backs_dashapp_main_2():
    @dashapp_main_2.callback(Output('', 'figure'),
              [Input('slider-updatemode-1', 'value'),
              Input('slider-updatemode-2', 'value')])
    def display_value(mu, var):
        x,y=create_data_dashapp_main_2(mu = mu/100, var = log_slider(var))
        return dashapp_main_2_str(x,y, mu/100)

    @dashapp_main_2.callback(Output("slider-3-value", 'children'),
        [Input('slider-updatemode-1', 'value')])
    def display_value_of_sliders(slid_1_v):
        return "{}".format(slid_1_v) 

    @dashapp_main_2.callback(Output("slider-4-value", 'children'),
        [Input('slider-updatemode-2', 'value')])
    def display_value_of_sliders(slid_2_v):
        return "{}".format(slid_2_v) 
  

dashapp_main_2.layout = html.Div(children=[
    html.H1(children=''),
    # the graph
    dcc.Graph(
        id='', style = {'width': 800, 'height': 300},
        figure= plot2_str(x,y),
        config={'displayModeBar': False}),
    # first slider division (mean)
    html.Div(id = "slider-1-container", children = ['Belief',
            dcc.Slider(id='slider-updatemode-1',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
          )], style={'width':800}),
          html.Div(id = "slider-3-value"),
    # sec slider division (var)
    html.Div(id = "slider-2-container", children = ['Confidence',
            dcc.Slider(id='slider-updatemode-2',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
    )
            ], style={'width':800}),
    html.Div(id = "slider-4-value")
             ]# end of list of layout
            )# parentheses for layout
call_backs_dashapp_main_2()


# MAIN PLOT 3 used for prior posterior for condition 1
######################################################################## 
dashapp_main_3  = dash.Dash(__name__,
                      reactVar = "react-entry-point5",
                      dash_file = 'dash_renderer5.min.js',
                      rendererID ='_dash-renderer5',
                      dash_config = '_dash-config5',
                      dash_scripts_src = '.*dash[-_]renderer5.*',
                      external_stylesheets=external_stylesheets, server=application, requests_pathname_prefix="/experiments/flask_bel_updating/dashapp_main_3/", routes_pathname_prefix="/dashapp_main_3/")

# creating some data for a line graph
def create_data_dashapp_main_3(mu, var):
    x = np.linspace(0.01, .99, 100)
    a, b = estBetaPar(mu, var)
    y = beta.pdf(x, a, b)
    return x, y

min(x, key=lambda xx:abs(xx-opinion_sld_val[0]))


def dashapp_main_3_str(x, y, mu):
    string_plot = {
            'data': [
                {'x': x, 'y': y, 'type': 'scatter', 'name': 'SF'},
            ],
            'layout': {'shapes':[{'type' : 'line', 'x0':mu, 'x1':mu, 'y0':0, 'y1':y[np.argmin([abs(d) for d in mu - x]  )],
                               'line' : {'color':'black', 'width' : 3}
                               }],
                'title': '',
                'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
                'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.01, 0.5, .99], 'ticktext':['Kri', 'neutral', 'Gor'], 'range':[0,1]}
            }
        }
    return string_plot

def call_backs_dashapp_main_3():
    @dashapp_main_3.callback(Output('', 'figure'),
              [Input('slider-updatemode-1', 'value'),
              Input('slider-updatemode-2', 'value')])
    def display_value(mu, var):
        x,y=create_data_dashapp_main_3(mu = mu/100, var = log_slider(var))
        return dashapp_main_3_str(x,y, mu/100)

    @dashapp_main_3.callback(Output("slider-5-value", 'children'),
        [Input('slider-updatemode-1', 'value')])
    def display_value_of_sliders(slid_1_v):
        return "{}".format(slid_1_v) 

    @dashapp_main_3.callback(Output("slider-6-value", 'children'),
        [Input('slider-updatemode-2', 'value')])
    def display_value_of_sliders(slid_2_v):
        return "{}".format(slid_2_v) 
  

dashapp_main_3.layout = html.Div(children=[
    html.H1(children=''),
    # the graph
    dcc.Graph(
        id='', style = {'width': 800, 'height': 300},
        figure= plot2_str(x,y),
        config={'displayModeBar': False}),
    # first slider division (mean)
    html.Div(id = "slider-1-container", children = ['Belief',
            dcc.Slider(id='slider-updatemode-1',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
          )], style={'width':800}),
          html.Div(id = "slider-5-value"),
    # sec slider division (var)
    html.Div(id = "slider-2-container", children = ['Confidence',
            dcc.Slider(id='slider-updatemode-2',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
    )
            ], style={'width':800}),
    html.Div(id = "slider-6-value")
             ]# end of list of layout
            )# parentheses for layout
call_backs_dashapp_main_3()


########################################################################

# MAIN PLOT 4 used for prior beliefs in condition 1
######################################################################## 
dashapp_main_4  = dash.Dash(__name__,
                      reactVar = "react-entry-point6",
                      dash_file = 'dash_renderer6.min.js',
                      rendererID ='_dash-renderer6',
                      dash_config = '_dash-config6',
                      dash_scripts_src = '.*dash[-_]renderer6.*',
                      external_stylesheets=external_stylesheets, server=application, requests_pathname_prefix="/experiments/flask_bel_updating/dashapp_main_4/", routes_pathname_prefix="/dashapp_main_4/")

# creating some data for a line graph
def create_data_dashapp_main_4(mu, var):
    x = np.linspace(0.01, .99, 100)
    a, b = estBetaPar(mu, var)
    y = beta.pdf(x, a, b)
    return x, y

min(x, key=lambda xx:abs(xx-opinion_sld_val[0]))


def dashapp_main_4_str(x, y, mu):
    string_plot = {
            'data': [
                {'x': x, 'y': y, 'type': 'scatter', 'name': 'SF'},
            ],
            'layout': {'shapes':[{'type' : 'line', 'x0':mu, 'x1':mu, 'y0':0, 'y1':y[np.argmin([abs(d) for d in mu - x]  )],
                               'line' : {'color':'black', 'width' : 3}
                               }],
                'title': '',
                'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
                'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.01, 0.5, .99], 'ticktext':['Smali', 'neutral', 'Larko'], 'range':[0,1]}
            }
        }
    return string_plot

def call_backs_dashapp_main_4():
    @dashapp_main_4.callback(Output('', 'figure'),
              [Input('slider-updatemode-1', 'value'),
              Input('slider-updatemode-2', 'value')])
    def display_value(mu, var):
        x,y=create_data_dashapp_main_4(mu = mu/100, var = log_slider(var))
        return dashapp_main_4_str(x,y, mu/100)

    @dashapp_main_4.callback(Output("slider-7-value", 'children'),
        [Input('slider-updatemode-1', 'value')])
    def display_value_of_sliders(slid_1_v):
        return "{}".format(slid_1_v) 

    @dashapp_main_4.callback(Output("slider-8-value", 'children'),
        [Input('slider-updatemode-2', 'value')])
    def display_value_of_sliders(slid_2_v):
        return "{}".format(slid_2_v) 
  

dashapp_main_4.layout = html.Div(children=[
    html.H1(children=''),
    # the graph
    dcc.Graph(
        id='', style = {'width': 800, 'height': 300},
        figure= plot2_str(x,y),
        config={'displayModeBar': False}),
    # first slider division (mean)
    html.Div(id = "slider-1-container", children = ['Belief',
            dcc.Slider(id='slider-updatemode-1',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
          )], style={'width':800}),
          html.Div(id = "slider-7-value"),
    # sec slider division (var)
    html.Div(id = "slider-2-container", children = ['Confidence',
            dcc.Slider(id='slider-updatemode-2',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
    )
            ], style={'width':800}),
    html.Div(id = "slider-8-value")
             ]# end of list of layout
            )# parentheses for layout
call_backs_dashapp_main_4()


# MAIN PLOT 5 used for posterior for condition 1
######################################################################## 
dashapp_main_5  = dash.Dash(__name__,
                      reactVar = "react-entry-point7",
                      dash_file = 'dash_renderer7.min.js',
                      rendererID ='_dash-renderer7',
                      dash_config = '_dash-config7',
                      dash_scripts_src = '.*dash[-_]renderer7.*',
                      external_stylesheets=external_stylesheets, server=application, requests_pathname_prefix="/experiments/flask_bel_updating/dashapp_main_5/", routes_pathname_prefix="/dashapp_main_5/")

# creating some data for a line graph
def create_data_dashapp_main_5(mu, var):
    x = np.linspace(0.01, .99, 100)
    a, b = estBetaPar(mu, var)
    y = beta.pdf(x, a, b)
    return x, y

min(x, key=lambda xx:abs(xx-opinion_sld_val[0]))


def dashapp_main_5_str(x, y, mu):
    string_plot = {
            'data': [
                {'x': x, 'y': y, 'type': 'scatter', 'name': 'SF'},
            ],
            'layout': {'shapes':[{'type' : 'line', 'x0':mu, 'x1':mu, 'y0':0, 'y1':y[np.argmin([abs(d) for d in mu - x]  )],
                               'line' : {'color':'black', 'width' : 3}
                               }],
                'title': '',
                'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
                'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.01, 0.5, .99], 'ticktext':['Smali', 'neutral', 'Larko'], 'range':[0,1]}
            }
        }
    return string_plot

def call_backs_dashapp_main_5():
    @dashapp_main_5.callback(Output('', 'figure'),
              [Input('slider-updatemode-1', 'value'),
              Input('slider-updatemode-2', 'value')])
    def display_value(mu, var):
        x,y=create_data_dashapp_main_5(mu = mu/100, var = log_slider(var))
        return dashapp_main_5_str(x,y, mu/100)

    @dashapp_main_5.callback(Output("slider-9-value", 'children'),
        [Input('slider-updatemode-1', 'value')])
    def display_value_of_sliders(slid_1_v):
        return "{}".format(slid_1_v) 

    @dashapp_main_5.callback(Output("slider-10-value", 'children'),
        [Input('slider-updatemode-2', 'value')])
    def display_value_of_sliders(slid_2_v):
        return "{}".format(slid_2_v) 
  

dashapp_main_5.layout = html.Div(children=[
    html.H1(children=''),
    # the graph
    dcc.Graph(
        id='', style = {'width': 800, 'height': 300},
        figure= plot2_str(x,y),
        config={'displayModeBar': False}),
    # first slider division (mean)
    html.Div(id = "slider-1-container", children = ['Belief',
            dcc.Slider(id='slider-updatemode-1',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
          )], style={'width':800}),
          html.Div(id = "slider-9-value"),
    # sec slider division (var)
    html.Div(id = "slider-2-container", children = ['Confidence',
            dcc.Slider(id='slider-updatemode-2',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
    )
            ], style={'width':800}),
    html.Div(id = "slider-10-value")
             ]# end of list of layout
            )# parentheses for layout
call_backs_dashapp_main_5()


# MAIN PLOT 6 used for prior beliefs in condition 2
######################################################################## 
dashapp_main_6  = dash.Dash(__name__,
                      reactVar = "react-entry-point8",
                      dash_file = 'dash_renderer8.min.js',
                      rendererID ='_dash-renderer8',
                      dash_config = '_dash-config8',
                      dash_scripts_src = '.*dash[-_]renderer8.*',
                      external_stylesheets=external_stylesheets, server=application, requests_pathname_prefix="/experiments/flask_bel_updating/dashapp_main_6/", routes_pathname_prefix="/dashapp_main_6/")

# creating some data for a line graph
def create_data_dashapp_main_6(mu, var):
    x = np.linspace(0.01, .99, 100)
    a, b = estBetaPar(mu, var)
    y = beta.pdf(x, a, b)
    return x, y

min(x, key=lambda xx:abs(xx-opinion_sld_val[0]))


def dashapp_main_6_str(x, y, mu):
    string_plot = {
            'data': [
                {'x': x, 'y': y, 'type': 'scatter', 'name': 'SF'},
            ],
            'layout': {'shapes':[{'type' : 'line', 'x0':mu, 'x1':mu, 'y0':0, 'y1':y[np.argmin([abs(d) for d in mu - x]  )],
                               'line' : {'color':'black', 'width' : 3}
                               }],
                'title': '',
                'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
                'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.01, 0.5, .99], 'ticktext':['Crogo', 'neutral', 'Mirsa'], 'range':[0,1]}
            }
        }
    return string_plot

def call_backs_dashapp_main_6():
    @dashapp_main_6.callback(Output('', 'figure'),
              [Input('slider-updatemode-1', 'value'),
              Input('slider-updatemode-2', 'value')])
    def display_value(mu, var):
        x,y=create_data_dashapp_main_6(mu = mu/100, var = log_slider(var))
        return dashapp_main_6_str(x,y, mu/100)

    @dashapp_main_6.callback(Output("slider-11-value", 'children'),
        [Input('slider-updatemode-1', 'value')])
    def display_value_of_sliders(slid_1_v):
        return "{}".format(slid_1_v) 

    @dashapp_main_6.callback(Output("slider-12-value", 'children'),
        [Input('slider-updatemode-2', 'value')])
    def display_value_of_sliders(slid_2_v):
        return "{}".format(slid_2_v) 
  

dashapp_main_6.layout = html.Div(children=[
    html.H1(children=''),
    # the graph
    dcc.Graph(
        id='', style = {'width': 800, 'height': 300},
        figure= plot2_str(x,y),
        config={'displayModeBar': False}),
    # first slider division (mean)
    html.Div(id = "slider-1-container", children = ['Belief',
            dcc.Slider(id='slider-updatemode-1',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
          )], style={'width':800}),
          html.Div(id = "slider-11-value"),
    # sec slider division (var)
    html.Div(id = "slider-2-container", children = ['Confidence',
            dcc.Slider(id='slider-updatemode-2',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
    )
            ], style={'width':800}),
    html.Div(id = "slider-12-value")
             ]# end of list of layout
            )# parentheses for layout
call_backs_dashapp_main_6()



# MAIN PLOT 7 used for posterior beliefs in condition 2
######################################################################## 
dashapp_main_7  = dash.Dash(__name__,
                      reactVar = "react-entry-point9",
                      dash_file = 'dash_renderer9.min.js',
                      rendererID ='_dash-renderer9',
                      dash_config = '_dash-config9',
                      dash_scripts_src = '.*dash[-_]renderer9.*',
                      external_stylesheets=external_stylesheets, server=application, requests_pathname_prefix="/experiments/flask_bel_updating/dashapp_main_7/", routes_pathname_prefix="/dashapp_main_7/")

# creating some data for a line graph
def create_data_dashapp_main_7(mu, var):
    x = np.linspace(0.01, .99, 100)
    a, b = estBetaPar(mu, var)
    y = beta.pdf(x, a, b)
    return x, y

min(x, key=lambda xx:abs(xx-opinion_sld_val[0]))


def dashapp_main_7_str(x, y, mu):
    string_plot = {
            'data': [
                {'x': x, 'y': y, 'type': 'scatter', 'name': 'SF'},
            ],
            'layout': {'shapes':[{'type' : 'line', 'x0':mu, 'x1':mu, 'y0':0, 'y1':y[np.argmin([abs(d) for d in mu - x]  )],
                               'line' : {'color':'black', 'width' : 3}
                               }],
                'title': '',
                'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
                'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.01, 0.5, .99], 'ticktext':['Crogo', 'neutral', 'Mirsa'], 'range':[0,1]}
            }
        }
    return string_plot

def call_backs_dashapp_main_7():
    @dashapp_main_7.callback(Output('', 'figure'),
              [Input('slider-updatemode-1', 'value'),
              Input('slider-updatemode-2', 'value')])
    def display_value(mu, var):
        x,y=create_data_dashapp_main_7(mu = mu/100, var = log_slider(var))
        return dashapp_main_7_str(x,y, mu/100)

    @dashapp_main_7.callback(Output("slider-13-value", 'children'),
        [Input('slider-updatemode-1', 'value')])
    def display_value_of_sliders(slid_1_v):
        return "{}".format(slid_1_v) 

    @dashapp_main_7.callback(Output("slider-14-value", 'children'),
        [Input('slider-updatemode-2', 'value')])
    def display_value_of_sliders(slid_2_v):
        return "{}".format(slid_2_v) 
  

dashapp_main_7.layout = html.Div(children=[
    html.H1(children=''),
    # the graph
    dcc.Graph(
        id='', style = {'width': 800, 'height': 300},
        figure= plot2_str(x,y),
        config={'displayModeBar': False}),
    # first slider division (mean)
    html.Div(id = "slider-1-container", children = ['Belief',
            dcc.Slider(id='slider-updatemode-1',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
          )], style={'width':800}),
          html.Div(id = "slider-13-value"),
    # sec slider division (var)
    html.Div(id = "slider-2-container", children = ['Confidence',
            dcc.Slider(id='slider-updatemode-2',
    min=0,
    max=100,
    step = 1,
    value=50,
    updatemode = 'drag',
    included=True
    )
            ], style={'width':800}),
    html.Div(id = "slider-14-value")
             ]# end of list of layout
            )# parentheses for layout
call_backs_dashapp_main_7()



# 
if __name__ == '__main__':
    manager.run()
#


#######################################################################################################
# alternative way of plotting that includes colors below the plot, 
#could e.g., be used if one wishes to compare confidence interpretations (such as integral vs. spread)
#######################################################################################################

# dashapp4 = dash.Dash(__name__,
#                       reactVar = "react-entry-point3",
#                       dash_file = 'dash_renderer3.min.js',
#                       rendererID ='_dash-renderer3',
#                       dash_config = '_dash-config3',
#                       dash_scripts_src = '.*dash[-_]renderer3.*',
#                       external_stylesheets=external_stylesheets, server=app, url_base_pathname='/dashplot3/' )

# dashapp4.layout = html.Div(children=[
#     html.H1(children='Belief and confidence'),

#     html.Div(children='''
#         Dash: A web a.
#     '''),
#     # the graph
#     dcc.Graph(
#         id='example-graph', style = {'width': 400},
#         figure={
#             'data': [
#                 {'x': x[:50], 'y': y[:50], 'type': 'scatter', 'name': 'SF', 'fill' : 'tozeroy', 'mode':'lines', 'line':{'color':'purple'}},
#                 {'x': x[50:], 'y': y[50:], 'type': 'scatter', 'name': 'SF', 'fill' : 'tozeroy', 'mode':'lines', 'line':{'color':'orange'}}
#             ],
#             'layout': {
#                     'shapes':[{'type' : 'line', 'x0':0.5, 'x1':0.5, 'y0':0, 'y1':y[49],
#                                'line' : {'color':'black', 'width' : 3}
#                                }],
    
#                 'title': 'Dash Data Visualization',
#                 'yaxis':{'showgrid':False, 'showaxis':False, 'showticks':False, 'zeroline':False, 'showticklabels':False},
#                 'xaxis' : {'showgrid': False, 'zeroline':False, 'tickvals' : [.2, 0, .8], 'ticktext':['A', 'neutral', 'B']}
#             }
#         }

#     ),
#     # first slider division (mean)
#     html.Div(id = "slider-1-container", children = ['Opinion',
#             dcc.Slider(id='slider-updatemode-1',
#     min=0.01,
#     max=1,
#     step = 0.01,
#     value=0.5,
#     updatemode = 'drag',
#     included=True
#     )
#             ], style={'width':200}),
#     html.Div(id = "slider-5-value"),
            
            
#     # second slider division (var)
#     html.Div(id="slider-2-container", children = ['Confidence',
#             dcc.Slider(id='slider-updatemode-2',
#     min=0.001,
#     max=0.1,
#     step = 0.001,
#     value=0.05,
#     updatemode = 'drag',
#     included=True
#     )
#             ], style={'margin-top': 60, 'width':200}),
#              html.Div(id = "slider-6-value")])



# @dashapp4.callback(Output('example-graph', 'figure'),
#               [Input('slider-updatemode-1', 'value'),
#               Input('slider-updatemode-2', 'value')])


# def display_value(mu, var):
#     return transform_data(mu, var)
   

# @dashapp4.callback([Output("slider-5-value", 'children'),
#                Output("slider-6-value", 'children')],
#               [Input('slider-updatemode-1', 'value'),
#                Input('slider-updatemode-2', 'value')])

# def display_value_of_sliders(slid_1_v, slid_2_v):
#     return ("{}".format(slid_1_v), "{}".format(slid_2_v) )
#############################################################