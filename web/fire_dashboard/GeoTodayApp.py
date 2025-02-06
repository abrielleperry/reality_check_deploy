from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


def geoTodayApp():

    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Load JSON data from URL
    url = "https://www.cityoftulsa.org/apps/opendata/tfd_dispatch.jsn"
    df = pd.read_json(url)

    # Normalize nested JSON data
    incidents = pd.json_normalize(df['Incidents']['Incident'])

    # Ensure that latitude and longitude are in the correct format
    incidents['Latitude'] = pd.to_numeric(
        incidents['Latitude'], errors='coerce')
    incidents['Longitude'] = pd.to_numeric(
        incidents['Longitude'], errors='coerce')

    # Convert 'ResponseDate' to datetime
    incidents['ResponseDate'] = pd.to_datetime(
        incidents['ResponseDate'],
        format='%m/%d/%Y %I:%M:%S %p')

    # Extract month and year for filtering
    incidents['Year'] = incidents['ResponseDate'].dt.year
    incidents['Month'] = incidents['ResponseDate'].dt.month

    # Create unique lists for the dropdown and checkboxes
    years = incidents['Year'].unique()
    months = incidents['Month'].unique()
    problems = incidents['Problem'].unique()

    # Layout for filters
    filters_layout = html.Div([
        dbc.Label("Select Year:"),
        dcc.Dropdown(
            id='year-filter',
            options=[{'label': year, 'value': year}
                     for year in sorted(incidents['Year'].unique())],
            value=sorted(incidents['Year'].unique())[0],  # Default value
            multi=False
        ),
        dbc.Label("Select Month:"),
        dcc.Dropdown(
            id='month-filter',
            options=[{'label': month, 'value': month}
                     for month in sorted(incidents['Month'].unique())],
            value=sorted(incidents['Month'].unique())[0],  # Default value
            multi=False
        ),
        dbc.Label("Select Problems:"),
        dbc.Checklist(
            id='problem-filter',
            options=[{'label': 'Unselect All', 'value': 'None'}, {'label': 'Select All', 'value': 'All'}] + \
            [{'label': problem, 'value': problem} for problem in problems],
            value=['All'],  # Default value
            inline=False
        )
    ])

    # Define the application layout
    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(filters_layout, md=4),
            dbc.Col([
                dcc.Graph(id='incident-map',
                          style={'width': '100%', 'height': '600px'})
            ], width=8)
        ])
    ])

    # Callback to update the map based on filters

    @app.callback(
        Output('incident-map', 'figure'),
        [Input('year-filter', 'value'),
         Input('month-filter', 'value'),
         Input('problem-filter', 'value')])
    def update_map(selected_year, selected_month, selected_problems):
        if 'All' in selected_problems:
            selected_problems = problems.tolist()

        filtered_data = incidents[
            (incidents['Year'] == selected_year) &
            (incidents['Month'] == selected_month) &
            (incidents['Problem'].isin(selected_problems))
        ]

        fig = px.scatter_mapbox(
            filtered_data,
            lat='Latitude',
            lon='Longitude',
            hover_name='Problem',
            hover_data=[
                'ResponseDate',
                'IncidentNumber'],
            color_discrete_sequence=["fuchsia"],
            zoom=10,
            center={
                "lat": 36.1540,
                "lon": -95.9928},
            title='Incident Locations',
            mapbox_style="open-street-map")
        return fig

    # Callback to handle the select all functionality

    @app.callback(
        Output('problem-filter', 'value'),
        [Input('problem-filter', 'value')],
        [State('problem-filter', 'options')])
    def select_all_problems(selected_problems, options):
        if 'All' in selected_problems and 'None' not in selected_problems:
            # If 'All' is selected and 'None' is not, select everything except
            # 'None'
            return [option['value']
                    for option in options if option['value'] != 'None']
        elif 'None' in selected_problems:
            # If 'None' is selected, unselect everything
            return []
        return selected_problems

    if __name__ == '__main__':
        app.run_server(debug=True)
