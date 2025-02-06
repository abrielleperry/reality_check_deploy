import pandas as pd
import requests
from xml.etree import ElementTree as ET

# Base URL for the Northwind OData service
base_url = "https://services.odata.org/V3/northwind/Northwind.svc/"

# Make a GET request to get the service document which lists all available collections
response = requests.get(base_url)
collections_xml = response.text

# Parse the XML to find the URL for the Order_Details collection
root = ET.fromstring(collections_xml)
ns = {'atom': 'http://www.w3.org/2005/Atom', 'app': 'http://www.w3.org/2007/app'}
order_details_url = None
for collection in root.findall('.//app:collection', ns):
    if 'Order_Details' in collection.get('href'):
        order_details_url = base_url + collection.get('href')
        break

# Check if the Order_Details URL was found
if order_details_url:
    # Since it's an OData service, we can request the data in JSON format which pandas can handle easily
    response = requests.get(order_details_url, headers={'Accept': 'application/json'})
    order_details_data = response.json()

    # Extracting the value which contains the actual data
    order_details_list = order_details_data['value']

    # Convert this into a DataFrame
    order_details_df = pd.DataFrame(order_details_list)

    # Display the DataFrame
    print(order_details_df)
else:
    print("Order_Details collection was not found in the service document.")
