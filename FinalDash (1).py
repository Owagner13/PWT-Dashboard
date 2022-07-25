# Good modules to have
import numpy as np, pandas as pd
import random, json, time, os

# Required Modules
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Add basic CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']




# This is the main application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Do not bother us with exceptions
app.config.suppress_callback_exceptions = True

data = pd.read_csv("pwtupdate1.csv") # Bringing in our dataset

# Use this list of variables for our dropdown menus throughout the code
varname=['Real GDP (Expenditure Side)',	'Real GDP (Output Side)','Population','Employment','Average Annual Hours Worked','Human Capital Index',	'Real Consumption','Real Domestic Absorbtion','Current GDP (Expenditure Side)','Current GDP (Output Side)','Capital Stock',	'Capital Services',	'TFP Level','TWP Level (Welfare Relevant)',	'Real GDP (2017 National Price)','Real Consumption (2017 National Price)',	'Real Domestic Absorbtion (2017 National Price)','Capital Stock (2017 National Price)',	'Capital Services (2017 National Price)',	'TFP (2017 National Price)','TWP (Welfare Relevant, 2017 National Price)','Share of labour compensation in GDP at current national prices','Share of Household Consumption','Share of Gross Capital Formation','Share of Government Consumption','Share of Merchandise Exports','Share of Merchandise Imports','Share of Residual Trade and GDP']
    




app.layout = html.Div([

    
    html.H1(children='Penn World Table Dashboard', style={'color':'midnightblue'}),
    html.H6('Penn World Tables is a set of national-accounts data that has been developed and maintained by individuals at the University of California, Davis and Groningen Growth Development Centre.', style={'color':'dimgrey'}),
    html.H6('This dashboard allows users to explore data from 183 countries relating to capital, productivity, employment, and population.', style={'color':'dimgrey'}),
    html.A("Link to Penn World Tables Documentation", href='https://www.rug.nl/ggdc/productivity/pwt/pwt-documentation', target="_blank"),
    
    
    html.Br(),
    html.Hr(),
    ############# For Plot 3 #############

    html.Div([ #### Makes a row of a page ##### 
                html.Div([   ### Makes a spcae for Left Graph #####
                    html.H3('Scatter Plot', style={'color':'slateblue'}),
                    html.H6('Use the drop down menus to select 2 variables', style={'color':'dimgrey'}),
                    html.Div([
                              # First dropdown for scatter
                              dcc.Dropdown(varname, value='Real GDP (Expenditure Side)',  id='dropdownscat1'),
                              ],
                              # Allows it to be side by side
                              style={'width': '49%', 'display': 'inline-block'}),
                    
                    html.Div([
                              # second dropdown for scatter
                              dcc.Dropdown(varname, value='Capital Stock',  id='dropdownscat2'),
                              ],
                              # Allows it to be side by side
                              style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                    # calls for the figure
                    dcc.Graph(id='figure2'),
                    # below is the slider for the graph to choose the year
                    html.Div([ 
                                dcc.Slider(
                                data['Year'].min(),
                                data['Year'].max(),
                                step=None,
                                value=2000,
                                marks={
                                    1950: '1950',
                                    1960: '1960',
                                    1970: '1970',
                                    1980: '1980',
                                    1990: '1990',
                                    2000: '2000',
                                    2010: '2010',
                                    2019: '2020'
                                },
                                id='year-slider'
                                )
                                ]),
                    
                     html.H6('Adjust the time slider to view data for different years', style={'color':'dimgrey'}),
                ], className="six columns"), # Determines how much of the row this graph gets must not exceed 12 between the two of them
        
        
                html.Div([   ### Right Graph #####
                    html.H3('Time Series', style={'color':'slateblue'}),
                    html.H6('Select a variable and countries to see over time', style={'color':'dimgrey'}),
                    html.Div([
                              dcc.Dropdown(varname, value='Real GDP (Expenditure Side)',  id='dropdown'), # Dropdown of all variable names
                              ],
                              style={'width': '49%', 'display': 'inline-block'}), # So dropdowns can be side by side
                    
                    html.Div([
                              # Dropdown to pick ounties and you can pick multiple
                              dcc.Dropdown(data.Country.unique(), value=['France'],  id='dropdown8', multi=True),
                              ],
                              style={'width': '49%', 'float': 'right', 'display': 'inline-block'}), #So it can be side by side
                    dcc.Graph(id='figure1'), # Calls for the time series grpah
                ], className="six columns"), # Six cols assigned which is half the page
    ], className="row"),
    
    html.Br(), # Space things out
    html.Hr(),
    
    html.Div([ #### Page Split ##### 
                html.Div([   ### Left Graph #####
                    html.H3('Sunburst Plot', style={'color':'slateblue'}),
                    html.H6('Use the drop down menu to select a variable', style={'color':'dimgrey'}),
                    html.Div([
                              # dropdown to change variable
                              dcc.Dropdown(varname, value='Real GDP (Expenditure Side)',  id='dropdown3'),
                              ],
                              style={'width': '49%', 'display': 'inline-block'}),
                    
                    
                    dcc.Graph(id='figure3'), # calls for the sunburst plot
                    html.H6('Navigate the figure by clicking continent of choice', style={'color':'dimgrey'}), 
                ], className="five columns"), #gets less page space because it is not wide

                html.Div([   ### Right Graph #####
                    html.H3('Map', style={'color':'slateblue'}),
                    html.H6('Use the drop down menu to select a variable', style={'color':'dimgrey'}),
                    html.Div([ # again a variable selector
                              dcc.Dropdown(varname, value='Real GDP (Expenditure Side)',  id='dropdown2'),
                              ],
                              style={'width': '49%', 'display': 'inline-block'}),
                    
                    
                    dcc.Graph(id='figure5'), # calls for the map
                    html.H6('                Navigate the map by hovering, clicking, and dragging', style={'color':'dimgrey'}),
                ], className="seven columns"), # gets more page space
    ], className="row")
                

])


    

#####################
#  Plot 1           #
#####################    

@app.callback(
    Output('figure2', 'figure'),
    Input('year-slider', 'value'),
    Input('dropdownscat1', 'value'),
    Input('dropdownscat2', 'value'))   
def make_plot(year,var1,var2):
    
    sub = data[(data['Year']==year)] # subsetting the data of year chosen from slider
            
    fig = px.scatter(sub,  x = var1, y=var2, color='Country', hover_name="Country",
                    template='seaborn')  # Graph the scatter of chosen variables for subset
    
    fig.update_layout(showlegend=False) # got rid of legend as it was large and unhelpful when hover gives all info needed
    return fig   

#####################
#  Plot 2           #
#####################
    
@app.callback(
    Output('figure1', 'figure'),
    Input('dropdown8', 'value'),
    Input('dropdown', 'value'))   
def make_plot(count,var):
    
    ################# Trial and error code for subsetting #################
    #sub = data[(data['Country'] in count)]    
    #   fig = go.Figure()
    #  fig.add_trace(go.Scatter(sub,  x = 'year', y='rgdpe', mode='lines',
    #    labels={"year":"Year","rgdpe":"Real GDP"}, title='Real GDP over time'))
    #df = px.data.gapminder().query("country == count")
    #for i in count:
    #    df=data[(data['Country'] == i)]
    #######################################################################
    
    
    sub=data[(data['Country'].isin(count))] # how we subset the data using counties passed in
    
    fig = px.line(sub,  x = 'Year', y=var, color='Country', template='seaborn') # graphing the subset of data for respective variable
    
    
    return fig    



#####################
#  Plot 3           #
#####################


@app.callback(
    Output('figure3', 'figure'),
    Input('dropdown3', 'value'))   
def make_plot(thing):
    # Divide countries into high and low for chosen variable
    data['HighLow']=(data[thing]>data[thing].mean())
    data.loc[data.HighLow == False,'HighLow'] = 'Low'
    data.loc[data.HighLow == True,'HighLow'] = 'High'

    # Below is the graph that resulted which is an interactive pie chart that divides it by continent, then into top 50% or lower 50% then country
    fig = px.sunburst(data[data.Year==2019], path=['Continent','HighLow', 'Country'], values=thing,
                      color='HighLow', color_discrete_map={'(?)':'lightsalmon', 'High':'bisque', 'Low':'lightcoral'},
                     template='ggplot2' )
    
 
    fig.update_traces(hovertemplate=None, hoverinfo='skip') #We wanted to get rid of the hoverbar because it was larger than the graph
    
    #We could not decide if we liked sunburst or tree mapp as they do very simmilar things
    #fig= px.treemap(data[data.Year==2019], path=['Continent', 'HighLow', 'Country'], values=thing)
    
    return fig   
    
    
#####################
#  Plot 4           #
##################### 

@app.callback(
    Output('figure5', 'figure'),
    Input('dropdown2', 'value'))   
def make_plot(var):
    
    fig = px.choropleth(data[data.Year==2019], locations="Country Code", 
                    color=var, # lifeExp is a column of gapminder
                    hover_name="Country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Sunset, # The colorbar we choose from
                    template='ggplot2' ) # We chose to use this theme
    
    
    
    return fig    
    


    
# -------------------------- MAIN ---------------------------- #


# This is the code that gets run when we call this file from the terminal
# The port number can be changed to fit your particular needs
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)