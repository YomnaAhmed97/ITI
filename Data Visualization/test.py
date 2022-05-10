# -*- coding: utf-8 -*-
"""
Created on Sun  00:38:53 2022

@author: Yomna
"""
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html , State
import plotly.express as px
import plotly.graph_objects as go
PLOTLY_LOGO = "https://iconape.com/wp-content/files/fa/64777/png/google-play-store.png"
img="https://i.pinimg.com/originals/09/6e/44/096e44c23114f1ac29d0cf034cc3a7a9.jpg"
img1="https://i.pinimg.com/564x/32/12/bb/3212bb00d282bef6831e755c5824fcb1.jpg"
df=pd.read_csv("googleplaystoreedit (1).csv")
#print(df.head(5))
#--------------------------------------

#-----------------------------------------
app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])
#----------------------------------
num_apps_in_category = df['Category'].value_counts()

# Sort num_apps_in_category in descending order based on the count of apps in each category
sorted_num_apps_in_category = num_apps_in_category.sort_values(ascending = False)

#fig1 = px.bar(df,
        # index = category name
 #       x = num_apps_in_category.values,
        # value = count
  #      y = num_apps_in_category.index,
   #     orientation="h",
        #color_continuous_scale='Bluered_r',
    #    template="seaborn",
     #   title="Exploring app categories",
      #  height=500,
       # width=600,
        
#)
"""
fig1 = px.scatter(df, x=num_apps_in_category.index, y= num_apps_in_category.values,
	         
          size_max=60)
"""
#fig1.update_yaxes(type='category')
fig1=px.pie(df, values=num_apps_in_category.values,names=num_apps_in_category.index,title="Exploring app categories",template=  'gridon',height=500,width=600)

#--------------------------------
avg_app_rating = df['Rating'].mean()
#print('Average app rating = ', avg_app_rating)

# Distribution of apps according to their ratings

fig2 = px.histogram(df,
        x = df['Rating'], color_discrete_sequence=['#DD2C00'], template="simple_white"
)

# Vertical dashed line to indicate the average app rating
fig2.update_layout(
    {'shapes': [{
               
              'type' :'line',
              'x0': avg_app_rating,
              'y0': 0,
              'x1': avg_app_rating,
              'y1': 1000,
              'line': { 'dash': 'dashdot'}
          }]
          })
#-------------------------------
trace0 = go.Box(
    # Data for paid apps
    y=df[df['Type'] == 'Paid']['Installs'],
    name = 'Paid'
)

trace1 = go.Box(
    # Data for free apps
    y=df[df['Type'] == 'Free']['Installs'],
    name = 'Free'
)

layout = go.Layout(
    title = "Number of downloads of paid apps vs. free apps",
    yaxis = dict(
        type = 'log',
        autorange = True
    )
)
data = [trace0,trace1]
fig3 = go.Figure(data=data,layout=layout)


# Add trace0 and trace1 to a list for plotting
data = [trace0,trace1]
#-----------------------------------------------------
labels =df['Type'].value_counts(sort = True).index
sizes = df['Type'].value_counts(sort = True)


#colors = ["palegreen","orangered"]
#explode = (0.1,0)  # explode 1st slice
 
#rcParams['figure.figsize'] = 8,8
# Plot
fig4 = go.Figure(data=[go.Pie(labels=labels, values=sizes, pull=[0.1,0])])

#--------------------------------------------------
paid_apps = df[df.Type == 'Paid']
data = [{
    'x' : paid_apps['Rating'],
    'type':'scatter',
    'y' : paid_apps['Size'],
    'mode' : 'markers',
    'text' : df['Size'],
    
    } for t in set(paid_apps.Type)]


layout = {'title':"Rating vs Size for Paid Apps", 
          'xaxis': {'title' : 'Rating'},
          'yaxis' : {'title' : 'Size (in MB)'},
}
fig5 = go.Figure(data=data,layout=layout)

#----------------------------------------------
popular_app_cats = df[df.Category.isin(['GAME', 'FAMILY', 'PHOTOGRAPHY',
                                            'MEDICAL', 'TOOLS', 'FINANCE',
                                            'LIFESTYLE','BUSINESS'])]

# Examine the price trend by plotting Price vs Category
fig6 =px.histogram(x = popular_app_cats['Price'], y = popular_app_cats['Category'], 
                   title="Relation between app category and app price",template="plotly_white",
                   color_discrete_sequence=['#FF6363'])

#--------------------------------------------------------
fig7 = px.histogram(df.sort_values('Installs', ascending=False),x = df['Genres'], y= df['Installs'],title="Apps Gernes Installs",template='gridon',height=500,width=600)
#----------------------------------------------------------
fig8 = px.histogram(df.sort_values('Rating', ascending=False),x = df['Genres'], y= df['Rating'],title="Apps Gernes Rating",template='gridon',height=500,width=600)
#-------------------------------------------------------------
labels =df['Content Rating'].value_counts(sort = True).index
sizes = df['Content Rating'].value_counts(sort = True)

fig9 = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
#--------------------------------------------------------------

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        #html.H2("Google Play Store", className="display-4", style={"width": "5rem"}),
        html.Img(src=PLOTLY_LOGO, style={"width": "3rem"}),
        html.H2("Google Play Store", style={"width": "5rem"}),
        html.Hr(),
        html.P(
            "A simple dashboard for analysing google play store apps", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

#Bans
#------------------------------------------------------

card_content1 = [
    dbc.CardHeader(
        [
          html.P("Display The Distrbution of Rating",
                 style={'text-align': 'center','fontSize':'140%','fontFamily':'Arial','fontWeight': 'bold',
                        'vertical-align':'middle'}),
          html.P("App ratings (on a scale of 1 to 5): "+str((df['Rating'].mean())),style={'text-align': 'center','fontSize':'140%','fontFamily':'Arial','fontWeight': 'bold','vertical-align':'middle'})],),

        ]

card_content2 = [
    dbc.CardHeader(
        [
                        html.P("Popularity of paid apps vs free apps",style={'text-align': 'center','vertical-align':'middle','fontSize':'140%','fontFamily':'Arial','fontWeight': 'bold'}),
                      ],),
        ]


card_content3 = [
    dbc.CardHeader(
        [
                        html.P("Percent of Free Apps",
                               style={'text-align': 'center','vertical-align':'middle','fontSize':'140%','fontFamily':'Arial','fontWeight': 'bold'}),
                        
        ]
    )]

card_content4 = [
    dbc.CardHeader(
        [
                        html.P("How do the sizes of paid apps and free apps vary?",
                               style={'text-align': 'center','vertical-align':'middle','fontSize':'140%','fontFamily':'Arial','fontWeight': 'bold'}),
                        
        ]
    )]

card_content5 = [
    dbc.CardHeader(
        [
                        html.P("App category and App price",
                               style={'text-align': 'center','vertical-align':'middle','fontSize':'140%','fontFamily':'Arial','fontWeight': 'bold'}),
                        
        ]
    )]

card_content6 = [
    dbc.CardHeader(
        [
                        html.P("Apps Gernes Installs",
                               style={'text-align': 'center','vertical-align':'middle','fontSize':'140%','fontFamily':'Arial','fontWeight': 'bold'}),
                        
        ]
    )]

card_content7 = [
    dbc.CardHeader(
        [
                        html.P("Apps Gernes Rating",
                               style={'text-align': 'center','vertical-align':'middle','fontSize':'140%','fontFamily':'Arial','fontWeight': 'bold'}),
                        
        ]
    )]

card_content8 = [
    dbc.CardHeader(
        [
                        html.P("Content Rating percentage",
                               style={'text-align': 'center','vertical-align':'middle','fontSize':'140%','fontFamily':'Arial','fontWeight': 'bold'}),
                        
        ]
    )]

#------------------------------------


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        #return html.P("This is the content of the home page!")
        return [
          # title and description
          html.H2('Play Store Description', style={"padding": "2rem 1rem"},),
         html.Div(
[
 dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        html.H4("Overview", className="card-title"),
                        html.P(
                               "The Play Store apps data has enormous potential to drive app-making businesses to success. Actionable insights can be drawn for developers to work on and capture the Android market! ",
                               
                               className="card-text",
                           ),
                        html.H5('The features are  :', className="card-title"),
                        html.P(" [App, Category, Rating, Reviews, Size, Installs, Type, Price, Content Rating, Genres, Last Updated, Current Ver, Android Ver]",className="card-text",),
                    ],
                    body=True,
                    ),
                ),
            
],
        ),
 ],
className="mb-3",
style={"maxWidth": "w-100"},
  ),
   html.Div(dbc.Row([
       dbc.Col([ 
           #html.Imp(src=img, style={ 'margin':'auto','background-color ':'black'}),
           
           dbc.Button(
           "Conclusion",
           id="fade-button", className="mb-3", n_clicks=0),
           dbc.Fade(
            dbc.Card( 
                dbc.CardBody(
                    
                    html.P(
                        "We will see that there are 33 unique app categories present in our dataset. Family and Game apps have the highest market prevalence. Interestingly, Tools, Business and Medical apps are also at the top.",
                        style={"color":"#6495ED", "font-weight": "italic"},#,"background-color": "lightblue"},
                        className="card-text"
                    )
                    
                  
                )

                
                      # dbc.Card(card_content, color="secondary", inverse=True)

                #color="dark",
               
            ),
            #id="fade-transition",
            id="fade",
            is_in=False,
            appear=False,
        ),
           dbc.Card(
               
        
                       
           [
            dcc.Graph(
                      id = 'example-graph-2',
                      figure = fig1
                     )
        ]
           
    ),
          # dcc.Graph(
          #           id = 'example-graph-2',
           #          figure = fig1
           #dbc.Row([dbc.Col(html.Img(src=img, style={ 'margin':'auto','background-color ':'black'}),),]),
           #dbc.Row([dbc.Col(html.Img1(src=img, style={ 'margin':'auto','background-color ':'black'}),),]),
                 
                 ] ),
           
       
       ]),
       className="g-0 d-flex align-items-left",style={"margin-left": "35.2rem"}#,"padding": "1rem 26rem"},
       ), 
   
   
       #className="col-md-7",style={'margin': 'auto 6%'},
       #className="mb-3",style={"padding": "1rem 26rem"},
       
     
]
    
  
    elif pathname == "/page-1":
        return [
            html.H2('Play Store Description', style={"padding": "2rem 1rem"},),
            html.Br(),
                    dbc.Row([
                        
                      dbc.Col([dbc.Card(card_content1, color='#FF5722', inverse=True),
                      #dbc.Col([dbc.Card(card_content2, color='#7a7d80', inverse=True)]),        
                               
                                      ],
                               ),
                              dcc.Graph(id='graph2',figure=fig2, 
                              style={ 'margin':'auto','background-color ':'black'}),
                              #dbc.Row(html.Div(dcc.Graph(id='graph3',figure=fig3), 
                                   # style={ 'margin':'auto','background-color ':'black'}))
                              ],),
                    
                    dbc.Row(
                    [
                       dbc.Col(
                           [ 
                            dbc.Col([dbc.Card(card_content2, color='#7a7d80', inverse=True)]),
                             dbc.Row(html.Div(dcc.Graph(id='graph3',figure=fig3), style={ 'margin':'auto','background-color ':'black'}))
                           ],width=6),
        
                       dbc.Col([
                           dbc.Col([dbc.Card(card_content3, color='#5c9a52', inverse=True)]),
                           dbc.Row(html.Div(dcc.Graph(id='graph4',figure=fig4), 
                                            style={ 'margin':'auto','background-color ':'black'})),
                         ],width=6)
            ],), 
                  
                    
                    ]
    elif pathname == "/page-2":
        return [
             html.H2('Play Store Description', style={"padding": "2rem 1rem"},),
             html.Br(),
                    dbc.Row(
                    [
                       dbc.Col(
                           [ 
                            dbc.Col([dbc.Card(card_content4, color='#345B63', inverse=True)]),
                             dbc.Row(html.Div(dcc.Graph(id='graph5',figure=fig5), style={ 'margin':'auto','background-color ':'black'}))
                           ],width=6),
        
                       dbc.Col([
                           dbc.Col([dbc.Card(card_content8, color='#F66B0E', inverse=True)]),
                           dbc.Row(html.Div(dcc.Graph(id='graph9',figure=fig9), 
                                            style={ 'margin':'auto','background-color ':'black'})),
                         ],width=6)
            ],),
                   
                    html.Br(),
                    dbc.Row(
                    [
                       dbc.Col(
                           [ 
                            dbc.Col([dbc.Card(card_content6, color='#EB5353', inverse=True)]),
                             dbc.Row(html.Div(dcc.Graph(id='graph7',figure=fig7), style={ 'margin':'auto','background-color ':'black'}))
                           ],width=6),
        
                       dbc.Col([
                           dbc.Col([dbc.Card(card_content7, color='#066163', inverse=True)]),
                           dbc.Row(html.Div(dcc.Graph(id='graph8',figure=fig8), 
                                            style={ 'margin':'auto','background-color ':'black'})),
                         ],width=6)
            ],),
                    html.Br(),
                    html.Br(),
                            dbc.Row([
                                
                              dbc.Col([dbc.Card(card_content5,color='#BD4B4B', inverse=True),
                              #dbc.Col([dbc.Card(card_content2, color='#7a7d80', inverse=True)]),        
                                       
                                              ],
                                       ),
                                      dcc.Graph(id='graph6',figure=fig6, 
                                      style={ 'margin':'auto','background-color ':'black'}),
                                      #dbc.Row(html.Div(dcc.Graph(id='graph3',figure=fig3), 
                                           # style={ 'margin':'auto','background-color ':'black'}))
                                      ],),
                    
                    ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output("fade", "is_in"),
    [Input("fade-button", "n_clicks")],
    [State("fade", "is_in")],
)
def Conclusion(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in



if __name__ == "__main__":
    app.run_server(port=8888)