from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import xml.etree.ElementTree as ET
import requests
import data_processing as dp


# Assuming `xml_data` is the XML string you've got from the URL
app = Dash(__name__)

# Load xml data from URL
url = "https://services.odata.org/V3/Northwind/Northwind.svc/"
# Read the XML from the URL, specifying the XPath to the collection elements
# You need to define the namespaces used in the XML file
namespaces = {
    'atom': 'http://www.w3.org/2005/Atom',
    'app': 'http://www.w3.org/2007/app'
}

# Use XPath to specify the path to the collection elements
df = pd.read_xml(url, xpath='//app:collection', namespaces=namespaces)

# If you print df, it should display a DataFrame with the 'href' attribute of each 'collection'
#print(df)
#print(df.columns)


for index, row in df.iterrows():
    collection_url = row['href']
    # Here you would do something with each collection URL, such as fetching and processing the data
    print(collection_url)

sales_order_df = dp.fetch_sales_order()
print(sales_order_df.columns)

order_details_df = dp.fetch_order_details()
print(order_details_df.columns)

# # Normalize nested JSON data
# incidents = pd.json_normalize(df['Incidents']['Incident'])

# # Ensure that latitude and longitude are in the correct format
# incidents['Latitude'] = pd.to_numeric(incidents['Latitude'], errors='coerce')
# incidents['Longitude'] = pd.to_numeric(incidents['Longitude'], errors='coerce')

# # Create a geographical scatter plot

# # Create a Mapbox scatter plot using a default style
# fig = px.scatter_mapbox(incidents, lat='Latitude', lon='Longitude',
#                         hover_name='Problem', hover_data=['ResponseDate', 'IncidentNumber'],
#                         color_discrete_sequence=["fuchsia"], zoom=10,
#                         center={"lat": 36.1540, "lon": -95.9928},
#                         title='Incident Locations', mapbox_style="open-street-map")

# # Dash layout
# app.layout = html.Div([
#     html.H1("Incident Locations"),
#     dcc.Graph(
#         figure=fig,
#         style={'height': '90vh', 'width': '80vh'}  
#         # Adjust height and width to create a more square aspect ratio
#     )
# ])

if __name__ == '__main__':
    app.run_server(debug=True)
