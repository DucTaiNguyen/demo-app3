import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


#########--------------- Integrate Flask and Dash-------------------############

import flask 
from flask_pymongo import PyMongo 
from pymongo import MongoClient
from flask import Flask, render_template

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
'''
I use 2 layout="" to see what happen when I add Dash to flask. but they are not really compatible.

The long layout can insert Dash, but not the flask.nav

'''


# layout = """
# <!DOCTYPE html>
# <html lang="en">
# <title>{%title%}</title>
# {%favicon%}
# {%metas%}
# <meta charset="UTF-8">
# <meta name="viewport" content="width=device-width, initial-scale=1">
# <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
# <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
# <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
# <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
# {%css%}
# <style>
# body,h1,h2,h3,h4,h5,h6 {font-family: "Lato", sans-serif}
# .w3-bar,h1,button {font-family: "Montserrat", sans-serif}
# .fa-anchor,.fa-coffee {font-size:200px}
# </style>
# <body>
# <!-- Navbar -->
# <div class="w3-top">
#   <div class="w3-bar w3-red w3-card w3-left-align w3-large">
#     <a class="w3-bar-item w3-button w3-hide-medium w3-hide-large w3-right w3-padding-large w3-hover-white w3-large w3-red" href="javascript:void(0);" onclick="myFunction()" title="Toggle Navigation Menu"><i class="fa fa-bars"></i></a>
#     <a href="#" class="w3-bar-item w3-button w3-padding-large w3-white">Home</a>
#     <a href="#" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Link 1</a>
#     <a href="#" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Link 2</a>
#     <a href="#" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Link 3</a>
#     <a href="#" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Link 4</a>
#   </div>

#   <!-- Navbar on small screens -->
#   <div id="navDemo" class="w3-bar-block w3-white w3-hide w3-hide-large w3-hide-medium w3-large">
#     <a href="#" class="w3-bar-item w3-button w3-padding-large">Link 1</a>
#     <a href="#" class="w3-bar-item w3-button w3-padding-large">Link 2</a>
#     <a href="#" class="w3-bar-item w3-button w3-padding-large">Link 3</a>
#     <a href="#" class="w3-bar-item w3-button w3-padding-large">Link 4</a>
#   </div>
# </div>

# <!-- Header -->
# <header class="w3-container w3-red w3-center" style="padding:128px 16px">
#   <h1 class="w3-margin w3-jumbo">START PAGE</h1>
#   <p class="w3-xlarge">Template by w3.css</p>
#   <button class="w3-button w3-black w3-padding-large w3-large w3-margin-top">Get Started</button>
# </header>

# <!-- First Grid -->
# <div class="w3-row-padding w3-padding-64 w3-container">
#   <div class="w3-content">
#     <div class="w3-twothird">
#       <h1>Bar Chart</h1>

#         <h2>Insert bar chart here</h2>
#         {%app_entry%}
#   </div>
# </div>
#   {%config%}
#   {%scripts%}
#   {%renderer%}
# </body>
# </html>
# """



layout='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index</title>
</head>
<body>
    {% nav.my_navbar.render() THis the problem the nav appear here????  %}
    <div class="w3-row-padding w3-padding-64 w3-container">
        <div class="w3-content">
          <div class="w3-twothird">
            <h1>Bar Chart</h1>
      
              <h2>Insert bar chart here</h2>
                {%app_entry%}
        </div>
  {%config%}
  {%scripts%}
  {%renderer%}
</body>
</html>
'''
# #mongo = PyMongo(server)
## flask server is main . There are 2 branches use main server ,these are app and app2
server = flask.Flask(__name__,)
app = dash.Dash(__name__, server = server,external_stylesheets=[] ,url_base_pathname='/dashboard/',)
app2 = dash.Dash(__name__, server = server,external_stylesheets=external_stylesheets ,index_string=layout) # index_string=layout url_base_pathname='/dashboard2/'
app3 = dash.Dash(__name__, server = server,external_stylesheets=[] ,url_base_pathname='/dashboard3/')



# #------------------- Nav-------------------######
from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator
nav = Nav(server)

nav.register_element('my_navbar',Navbar(
    'thenav',
    View('CropParameters','render_dashboard'),
    View('CropParameters_All','render_dashboard2'),
    View('CropParameters 3','render_dashboard3'),
    View('Item One', 'item',item=1),
    Link('Google','https://www.google.com'),

    ))





@server.route('/index')
def index():
    return render_template('index.html')

# @server.route('/item')
# def item():
#     return render_template('layout.html')

#######------------------ Make some routes demo------------------------######


@server.route('/dashboard')
def render_dashboard():
    return flask.redirect('/dashboard/')

@server.route('/plotly_dashboard')
def render_dashboard2():
    return flask.redirect('/dashboard2/')

@server.route('/plotly_dashboard3')
def render_dashboard3():
    return flask.redirect('/dashboard3/')


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





#####------ For testing ----------#########
fig2 = px.bar(df, x=df.xtime, y=df.columns[4:9])
fig2.update_layout(
    
    title="CropParameters",
    yaxis_title="value",
    xaxis_title="Time",
    legend_title="variable",
    
   )
# fig3 = px.bar(df, x=df.xtime, y=df.columns[4:9])
# fig3.update_layout(
    
#     title="CropParameters Div 2",
#     yaxis_title="value",
#     xaxis_title="Time",
#     legend_title="variable",
#    )
#####################################################
##########--------------app3------------#############
'''
stem_elong,stem_thick,cum_trusses,stem_dens,plant_dens
'''
app3.layout = html.Div(children=[
    html.Div([
        html.H1(["Crop Parameters of stem_elong".upper()], style={'text-align': 'center'}),
        dcc.Graph(id='my_app3_Graph_1', figure=go.Figure(data("stem_elong")))
    ]),

        html.Div([
        html.H1(["Crop Parameters of stem_thick".upper()], style={'text-align': 'center'}),
        dcc.Graph(id='my_app3_Graph_2', figure=go.Figure(data("stem_thick")))
    ]),
        html.Div([
        html.H1(["Crop Parameters of cum_trusses".upper()], style={'text-align': 'center'}),
        dcc.Graph(id='my_app3_Graph_3', figure=go.Figure(data("cum_trusses")))
    ]),
        html.Div([
        html.H1(["Crop Parameters of stem_dens".upper()], style={'text-align': 'center'}),
        dcc.Graph(id='my_app3_Graph_4', figure=go.Figure(data("stem_dens")))
    ]),
        html.Div([
        html.H1(["Crop Parameters of plant_dens".upper()], style={'text-align': 'center'}),
        dcc.Graph(id='my_app3_Graph_5', figure=go.Figure(data("plant_dens")))
    ]),


])

#####----------------- App2----------############
app2.layout = html.Div([html.H1('CroParameters for All'.upper()),
                     html.Div(dcc.Input(id='input-on-submit', type='text')),
                    html.A('Google',href='#'),
                    dcc.Location(id='url', refresh=False),
                    html.Br(),
                      dcc.Link('Navigate to "/"', href='/'),
    html.Br(),

                    dcc.Graph(id='my-Graph-2', figure=fig2),
                    
])

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
    app3.run_server()

