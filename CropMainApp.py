import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#########--------------- Integrate Flask and Dash-------------------############

import flask 
from flask_pymongo import PyMongo
from pymongo import MongoClient


# #mongo = PyMongo(server)
## flask server is main . There are 2 branches use main server ,these are app and app2
server = flask.Flask(__name__)
app = dash.Dash(__name__, server = server, url_base_pathname='/dashboard/')
app2 = dash.Dash(__name__, server = server, url_base_pathname='/dashboard2/')



# #------------------- Nav-------------------######
from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator
nav = Nav(server)

nav.register_element('my_navbar',Navbar(
    'thenav',
    View('CropParameters','render_dashboard'),
    View('CropParameters_All','render_dashboard2'),
    View('Item One', 'item',item=1),
    Link('Google','https://www.google.com'),

    ))


@server.route('/')
def index():
    return render_template('index.html')

@server.route('/items/<item>')
def item(item):
    return '<h1> The item Page!!! the item is: {}.'.format(item)

#######------------------ Make some routes demo------------------------######


@server.route('/dashboard')
def render_dashboard():
    return flask.redirect('/dashboard/')

@server.route('/plotly_dashboard')
def render_dashboard2():
    return flask.redirect('/dashboard2/')


#Loading data

cluster = MongoClient('mongodb+srv://tai:12345@cluster0.l0bot.mongodb.net/farm?retryWrites=true&w=majority')
db = cluster['farm']
collection=db["CropParameters"]

data_from_db = collection.find({})
df=pd.DataFrame.from_dict(data_from_db)

###2. from csv
#df = pd.read_csv('CropParameters.csv')

######################################

# Find the list of farm name:
for col in df.columns:
    if col == "farm_name":
        farm_name = sorted(df.farm_name.unique())
        
## Clear data to fit with graph object. This is specific case for our requirement
## to filter 6 farms individualy as variable and then perfrom them in 1 plotly.
def data(product: str):
    data = []
    for col in df.columns:
        if col == "farm_name":
            for _farm_name in df.farm_name.unique():  # array(['Reference', 'AICU', 'Digilog', 'IUACAAS', 'Automatoes','TheAutomators'], dtype=object)
                farm = df.loc[df['farm_name'] == _farm_name]  # 6 farms here
                data = data + [go.Bar(name=_farm_name, x=farm.xtime, y=farm[product])]
    return data




# # ----------------------Fig2 and App2 layout------------------------#

fig2 = px.bar(df, x=df.xtime, y=df.columns[4:9])
fig2.update_layout(
    
    title="CropParameters",
    yaxis_title="value",
    xaxis_title="Time",
    legend_title="variable",
   )


app2.layout = html.Div([html.H1('CroParameters for All'.upper()),


                    dcc.Graph(id='my-Graph-2', figure=fig2)
])



# #
# # ----------------------App layout------------------------#


app.layout = html.Div([
    html.H1(["Crop Parameters".upper()], style={'text-align': 'center'}),
    dcc.Dropdown(id='product_choice',
                 options=[{'value': product, 'label': product}
                          for product in df.iloc[:0, [4, 5, 6, 7, 8]]],
                 # == [stem_elong,stem_thick,cum_trusses,stem_dens,plant_dens]
                 value='stem_elong'),  # For general:I am looking for the loop for df.iloc[x for ???]

    dcc.Graph(id='my-Graph', figure={}),
])


# ##-------------- Call Back-------------------##
@app.callback(
    Output(component_id='my-Graph', component_property='figure'),
    Input(component_id='product_choice', component_property='value')

)
def interactive_graphing(value_product):
    print(value_product)
    fig = go.Figure(data(value_product))
    fig.update_layout(
        barmode='group',
        title=("Your choice:  " + value_product).upper(),
        yaxis_title="unit",
        xaxis_title="Time",
        legend_title="Farm Name",
    )
    return fig


if __name__ == '__main__':
    server.run()        ### This is Flask server
    app.run_server()
    app2.run_server()

