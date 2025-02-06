import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px


df = pd.read_csv('../data/fire.csv')

# Exclude specific location names
df = df[~df['location_name'].isin(['HSE', '0'])]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Location Distribution"),
    dcc.Graph(
        id='location_name-chart',
        style={
            'height': '1000px'})  # Adjust height as needed
])


@app.callback(
    dash.dependencies.Output('location_name-chart', 'figure'),
    [dash.dependencies.Input('location_name-chart', 'id')]
)
def update_area_chart(selected_property):
    # Calculate the value counts of location names
    location_name_counts = df['location_name'].value_counts().reset_index()
    location_name_counts.columns = ['location_name', 'count']

    # Filter to only include locations with more than 10 occurrences
    filtered_counts = location_name_counts[location_name_counts['count'] > 100]

    # Sort values in descending order
    filtered_counts = filtered_counts.sort_values('count', ascending=False)

    # Check if the DataFrame is empty after filtering
    if filtered_counts.empty:
        return px.bar(title="No data to display.")

    # Create the horizontal bar chart
    fig = px.bar(
        filtered_counts,
        x='count',
        y='location_name',
        title='Locations'
    )

    # Adjust x-axis range
    max_count = filtered_counts['count'].max()
    fig.update_xaxes(range=[0, max_count + 10])

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
