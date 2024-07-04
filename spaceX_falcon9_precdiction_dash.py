# Import necessary libraries and modules
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load your SpaceX launch data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Determine the range for payload mass slider
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define unique launch sites for dropdown options
uniquelaunchsites = spacex_df['Launch Site'].unique().tolist()
lsites = [{'label': 'All Sites', 'value': 'All Sites'}]
for site in uniquelaunchsites:
    lsites.append({'label': site, 'value': site})

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    dcc.Dropdown(id='site_dropdown',
                 options=lsites,
                 value='All Sites',
                 placeholder='Select a Launch Site here',
                 searchable=True),
    
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
    id='payload_slider',
    min=0,
    max=10000,
    step=1000,
    marks={
        0: '0 kg', 1000: '1000 kg', 2000: '2000 kg',
        3000: '3000 kg', 4000: '4000 kg', 5000: '5000 kg',
        6000: '6000 kg', 7000: '7000 kg', 8000: '8000 kg',
        9000: '9000 kg', 10000: '10000 kg'
    },
    value=[min_payload, max_payload]
)


    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Define callback to update success-pie-chart based on site_dropdown value
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value')]
)
def update_pie_chart(site_dropdown):
    if site_dropdown == 'All Sites':
        # Filter data for successful launches
        df_success = spacex_df[spacex_df['class'] == 1]
        # Create pie chart
        fig = px.pie(df_success, names='Launch Site', title='Total Success Launches By all sites')
    else:
        # Filter data for successful launches at the selected site
        df_success = spacex_df[(spacex_df['class'] == 1) & (spacex_df['Launch Site'] == site_dropdown)]
        # Create pie chart
        fig = px.pie(df_success, names='class', title=f'Total Success Launches for site {site_dropdown}')
    
    return fig

# Define callback to update success-payload-scatter-chart based on site_dropdown and payload_slider values
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value'),
     Input(component_id='payload_slider', component_property='value')]
)
def update_scatter_chart(site_dropdown, payload_slider):
    # Filter data based on payload range and selected site
    low, high = payload_slider
    if site_dropdown == 'All Sites':
        df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
        title = 'Payload and Outcome for all Sites'
    else:
        df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high) & (spacex_df['Launch Site'] == site_dropdown)]
        title = f'Payload and Outcome for {site_dropdown}'
    
    # Create scatter plot
    fig = px.scatter(df_filtered, x='Payload Mass (kg)', y='class', color='Booster Version',
                     size='Payload Mass (kg)', hover_data=['Payload Mass (kg)', 'Booster Version'])
    
    # Update layout attributes
    fig.update_layout(title=title, xaxis_title='Payload Mass (kg)', yaxis_title='Outcome Class')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
