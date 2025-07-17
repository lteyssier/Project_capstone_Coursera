# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Dropdown para selección de sitio
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     *[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
                 ],
                 value='ALL',
                 placeholder='Select a Launch Site',
                 searchable=True),
    html.Br(),

    # Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # RangeSlider para Payload
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload,
                    max=max_payload,
                    step=1000,
                    marks={int(min_payload): f'{int(min_payload)} kg',
                           int(max_payload): f'{int(max_payload)} kg'},
                    value=[min_payload, max_payload]),

    # Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback del pie chart
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df[spacex_df['class'] == 1],
                     names='Launch Site',
                     title='Total Successful Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df,
                     names='class',
                     title=f'Total Launch Outcomes for site {selected_site}')
    return fig

# Callback del scatter chart
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title=f'Success vs Payload for {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
