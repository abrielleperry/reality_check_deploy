from geopy.geocoders import Nominatim
import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Initialize geocoder
geolocator = Nominatim(user_agent="geomapnorthwind")

# Example data with cities and revenue
data = {
    'City': ['New York', 'Toronto', 'San Francisco', 'London'],
    'Country': ['USA', 'Canada', 'USA', 'UK'],
    'Net Revenue': [1000, 1500, 1200, 1800]
}

df = pd.DataFrame(data)

# Function to get latitude and longitude
def get_lat_lon(city):
    location = geolocator.geocode(city)
    return location.latitude, location.longitude

# Apply function to DataFrame
df[['Latitude', 'Longitude']] = df['City'].apply(lambda x: pd.Series(get_lat_lon(x)))

mean_lat = df['Latitude'].mean()
mean_lon = df['Longitude'].mean()


map_center = {"lat": mean_lat, "lon": mean_lon}

# Create a map using Plotly Express
fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Net Revenue",
                        hover_name='City', hover_data={
                            "Country": True,        # Show city
                            "Net Revenue": True, # Show net revenue
                            "Latitude": False,   # Do NOT show latitude
                            "Longitude": False   # Do NOT show longitude
                        },
                        size='Net Revenue', color_discrete_sequence=["fuchsia"],
                        size_max=15, zoom=1.5, center=map_center,
                        mapbox_style="open-street-map")

# Initialize the Dash app
app = dash.Dash(__name__)

# Setup app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(lg=4, md=6),  # Empty column for spacing
        dbc.Col(dcc.Graph(figure=fig), lg=4, md=6,
                style={'width': '50%', 'height': '100%'}),  # Column for the map
        dbc.Col(lg=4, md=6)  # Empty column for spacing
    ])
], fluid=True)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
