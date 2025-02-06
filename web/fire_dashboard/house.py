import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

def House():
    data = pd.read_csv('../data/fire.csv')

    filtered_data = data[data['location_name'].str.lower() == 'hse']

    incident_counts = filtered_data['incident'].value_counts().reset_index()
    incident_counts.columns = ['incident', 'count']

    threshold = 10  
    filtered_incidents = incident_counts[incident_counts['count'] > threshold]

    fig = px.bar(filtered_incidents, x='incident', y='count', title='Frequency of Incidents at Location "HSE"', color='incident',  # This assigns a unique color based on the 'incident' column
                color_continuous_scale=px.colors.qualitative.Plotly)

    fig.update_layout(width=1200, height=800)

    max_count = filtered_incidents['count'].max()
    fig.update_yaxes(range=[0, max_count + 82])

    app = Dash(__name__)

    app.layout = html.Div(children=[
        html.H1(children='Incident Analysis for Houses'),
        dcc.Graph(
            id='incident-graph',
            figure=fig
        )
    ])

    if __name__ == '__main__':
        app.run_server(debug=True)
