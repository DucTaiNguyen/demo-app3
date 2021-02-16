# import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
##------------------Need to improve ----------------------#
## Unit is not uppdate automaticly yet
## Some CSS

# app = dash.Dash(__name__)

#########--------------- Integrate Flask and Dash-------------------############

import flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = flask.Flask(__name__)


#mongo = PyMongo(server)
server = flask.Flask(__name__)
app = dash.Dash(__name__, server = server, url_base_pathname='/dashboard/')
app2 = dash.Dash(__name__, server = server, url_base_pathname='/dashboard2/')

#######------------------ Make some routes demo------------------------######

@server.route('/')
def index():
    return 'This is index page'


@server.route('/hello')
def hello():
    return 'Hello, World!'


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


#2. from csv
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




# ----------------------App2 layout------------------------#


app2.layout = html.Div([html.H1('Hi there, I am app2 for reports from Dash'.upper())])



#
# ----------------------App layout------------------------#


app.layout = html.Div([
    html.H1(["Crop Parameters".upper()], style={'text-align': 'center'}),
    dcc.Dropdown(id='product_choice',
                 options=[{'value': product, 'label': product}
                          for product in df.iloc[:0, [4, 5, 6, 7, 8]]],
                 # == [stem_elong,stem_thick,cum_trusses,stem_dens,plant_dens]
                 value='stem_elong'),  # For general:I am looking for the loop for df.iloc[x for ???]

    dcc.Graph(id='my-Graph', figure={}),
])


##-------------- Call Back-------------------##
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
    app.run_server()
    app2.run_server()
