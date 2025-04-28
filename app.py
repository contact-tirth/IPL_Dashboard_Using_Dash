# from http.cookiejar import debug
import pandas as pd
import numpy as np
import dash
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output

deliveries = pd.read_csv('D:\Learning\DSMP 2.0\IPL_Analysis_Dashboard_Dash\Datasets\deliveries.csv')
matches = pd.read_csv('D:\Learning\DSMP 2.0\IPL_Analysis_Dashboard_Dash\Datasets\matches.csv')
ipl_df = matches.merge(deliveries,left_on='id',right_on='match_id')

#To Get Total Run in Season
ipl_2024 = ipl_df[ipl_df['season']=='2024']
total_runs = ipl_2024['total_runs'].sum()
# print(total_runs)

#To Print Total Wickets in Season
total_wickets = ipl_2024['is_wicket'].sum()
# print(total_wickets)

#Orange Cap
orange_cap = ipl_2024.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(1).index[0]
orange_runs = ipl_2024.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(1).values[0]
#Purple Cap
purple_cap = ipl_2024.groupby('bowler')['is_wicket'].sum().sort_values(ascending=False).head(1).index[0]
purple_wicket = ipl_2024.groupby('bowler')['is_wicket'].sum().sort_values(ascending=False).head(1).values[0]

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

options = [
    # {'label':'All','value':'All'},
    {'label':'2007/08','value':'2007/08'},
    {'label':'2009','value':'2009'},
    {'label':'2009/10','value':'2009/10'},
    {'label':'2011','value':'2011'},
    {'label':'2012','value':'2012'},
    {'label':'2013','value':'2013'},
    {'label':'2014','value':'2014'},
    {'label':'2015','value':'2015'},
    {'label':'2016','value':'2016'},
    {'label':'2017','value':'2017'},
    {'label':'2018','value':'2018'},
    {'label':'2019','value':'2019'},
    {'label':'2020/21','value':'2020/21'},
    {'label':'2021','value':'2021'},
    {'label':'2022','value':'2022'},
    {'label':'2023','value':'2023'},
    {'label':'2024','value':'2024'}
]

app=dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout=html.Div(
    [
                html.H1('IPL Analysis Dashboard',style={'color':'#FFFFFF',
                                                                'text-align':'center',
                                                                'font-weight': 'bold',
                                                                'margin-top': '30px'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H3('Total Runs',style={'text-align':'center',
                                                                    'font-weight': 'bold',
                                                                    'color':'#FFFFFF',
                                                                    'text-decoration': 'underline'
                                                     }),
                                html.H4(total_runs,style={'text-align':'center',
                                                             'font-weight': 'bold',
                                                            'color':'#FFFFFF'
                                                     })
                            ],className='card-body')
                        ],className='card bg-danger')
                    ],className='col-md-3'),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H3('Total Wickets', style={'text-align': 'center',
                                                              'font-weight': 'bold',
                                                              'color': '#FFFFFF',
                                                              'text-decoration': 'underline'
                                                              }),
                                html.H4(total_wickets, style={'text-align': 'center',
                                                      'font-weight': 'bold',
                                                      'color': '#FFFFFF'
                                                      })
                            ], className='card-body')
                        ], className='card bg-info')
                    ],className='col-md-3'),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H3('Orange Cap', style={
                                    'text-align': 'center',
                                    'font-weight': 'bold',
                                    'color': '#FFFFFF',
                                    'text-decoration': 'underline'
                                }),
                                html.H4(orange_cap, style={
                                    'text-align': 'center',
                                    'font-weight': 'bold',
                                    'color': '#FFFFFF',
                                    'margin-bottom': '5px'  # small gap between name and runs
                                }),
                                html.H5(f"Runs: {orange_runs}", style={
                                    'text-align': 'center',
                                    'font-weight': 'bold',
                                    'color': '#FFFFFF'
                                })
                            ], className='card-body')
                        ], className='card bg-dark')
                    ],className='col-md-3'),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H3('Purple Cap', style={
                                    'text-align': 'center',
                                    'font-weight': 'bold',
                                    'color': '#FFFFFF',
                                    'text-decoration': 'underline'
                                }),
                                html.H4(purple_cap, style={
                                    'text-align': 'center',
                                    'font-weight': 'bold',
                                    'color': '#FFFFFF',
                                    'margin-bottom': '5px'  # small gap between name and runs
                                }),
                                html.H5(f"Wickets: {purple_wicket}", style={
                                    'text-align': 'center',
                                    'font-weight': 'bold',
                                    'color': '#FFFFFF'
                                })
                            ], className='card-body')
                        ], className='card bg-success')
                    ],className='col-md-3'),
                ],className='row'),
                html.Div([
                    html.Div([],className='col-md-6'),
                    html.Div([], className='col-md-6')
                ],className='row'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                dcc.Dropdown(id='picker',options=options,value='All'),
                                dcc.Graph(id='bar')
                            ],className='card-body')
                        ],className='card')
                    ],className='col-md-12',style={'margin-top': '30px'})
                ],className='row')
            ],className='container')

@app.callback(Output('bar','figure'),[Input('picker','value')])
def update_graph(selected_value):
    new_df = ipl_df[ipl_df['season']==str(selected_value)]
    top_50 = new_df.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(25).reset_index()
    fig = {
        'data': [go.Bar(x=top_50['batter'], y=top_50['batsman_runs'])],
        'layout': go.Layout(title='Top 50 Batsmen In IPL Season')
    }
    return fig


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
