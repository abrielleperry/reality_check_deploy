import pandas as pd
import requests
from xml.etree import ElementTree as ET
from urllib.parse import urljoin

def get_merged_df():
    # Assuming 'order_details_df' is already fetched somewhere in your code
    order_details_df = fetch_order_details()
    sales_order_df = fetch_sales_order()
    # print(sales_order_df.columns)
    # print(order_details_df.columns)
    # Ensure that 'OrderID' is of the same type in both DataFrames
    sales_order_df['OrderID'] = sales_order_df['OrderID'].astype(str)
    order_details_df['OrderID'] = order_details_df['OrderID'].astype(str)
    gross_revenue = calculate_gross_revenue(order_details_df)
    # Merge the two DataFrames on 'OrderID'
    merged_df = pd.merge(sales_order_df, order_details_df, on='OrderID')

    # Check columns after merge
    #print(merged_df.columns)

    # If 'Gross_Revenue' column is not found, raise an error
    if 'LineTotal' not in merged_df.columns:
        raise KeyError("Column 'LineTotal' not found after merging dataframes.")
    
    return merged_df

def fetch_sales_order():
    base_url = "https://services.odata.org/V3/northwind/Northwind.svc/"
    response = requests.get(base_url)
    collections_xml = response.text

    root = ET.fromstring(collections_xml)
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'app': 'http://www.w3.org/2007/app'}
    sales_order_url = None

    for collection in root.findall('.//app:collection', ns):
        if 'Orders' in collection.get('href'):
            sales_order_url = urljoin(base_url, collection.get('href'))
            break

    if sales_order_url:
        response = requests.get(sales_order_url, headers={'Accept': 'application/json'})
        sales_order_data = response.json()
        sales_order_list = sales_order_data.get('value', [])
        return pd.DataFrame(sales_order_list)    
    
    return pd.DataFrame()
    #an empty DataFrame if the URL was not found

def fetch_order_details():
    base_url = "https://services.odata.org/V3/northwind/Northwind.svc/"
    response = requests.get(base_url)
    collections_xml = response.text

    root = ET.fromstring(collections_xml)
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'app': 'http://www.w3.org/2007/app'}
    order_details_url = None

    for collection in root.findall('.//app:collection', ns):
        if 'Order_Details' in collection.get('href'):
            order_details_url = urljoin(base_url, collection.get('href'))
            break

    if order_details_url:
        response = requests.get(order_details_url, headers={'Accept': 'application/json'})
        order_details_data = response.json()
        order_details_list = order_details_data.get('value', [])
        return pd.DataFrame(order_details_list)
    
    return pd.DataFrame()
    #an empty DataFrame if the URL was not found

def calculate_gross_revenue(df):
    if not df.empty:
        #Sprint(df.columns)
        # Convert columns to numeric types, use errors='coerce' to handle any conversion issues
        df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df['DiscountPerc'] = pd.to_numeric(df['Discount'], errors='coerce')        # Calculate the gross revenue for each line
        df['LineTotal'] = df['UnitPrice'] * df['Quantity']
        df['DiscountDollars'] = df['LineTotal'] * df['DiscountPerc']
        df['NetRevenue'] = df['LineTotal'] - df['DiscountDollars']
        # Sum up to get the total gross revenue
        return df['LineTotal'].sum(), df['NetRevenue'].sum(), df['DiscountDollars'].sum()
    return 0

def compute_daily_revenue(merged_df):
    # Assuming 'Order_Date' is a column in 'sales_order_df'
    # Ensure the 'OrderDate' column is converted to datetime objects
    merged_df['OrderDate'] = pd.to_datetime(merged_df['OrderDate'], errors='coerce')

    # Calculate daily gross revenue
    daily_revenue = merged_df.groupby(merged_df['OrderDate'].dt.date)['LineTotal'].sum()
    return daily_revenue.reset_index(name='LineTotal')

def compute_location_netrevenue(merged_df):
    # Assuming 'Order_Date' is a column in 'sales_order_df'
    # Ensure the 'OrderDate' column is converted to datetime objects
    merged_df['OrderDate'] = pd.to_datetime(merged_df['OrderDate'], errors='coerce')
    # Calculate daily gross revenue
    location_revenue = merged_df.groupby(merged_df['ShipCity'])['NetRevenue'].sum()
    return location_revenue.reset_index(name='NetRevenue')

def compute_location_grossrevenue(merged_df):
    # Assuming 'Order_Date' is a column in 'sales_order_df'
    # Ensure the 'OrderDate' column is converted to datetime objects
    merged_df['OrderDate'] = pd.to_datetime(merged_df['OrderDate'], errors='coerce')
    # Calculate daily gross revenue
    location_revenue = merged_df.groupby(merged_df['ShipCity'])['LineTotal'].sum()
    return location_revenue.reset_index(name='LineTotal')

def compute_location_discount(merged_df):
    # Assuming 'Order_Date' is a column in 'sales_order_df'
    # Ensure the 'OrderDate' column is converted to datetime objects
    merged_df['OrderDate'] = pd.to_datetime(merged_df['OrderDate'], errors='coerce')
    # Calculate daily gross revenue
    location_revenue = merged_df.groupby(merged_df['ShipCity'])['DiscountDollars'].sum()
    return location_revenue.reset_index(name='DiscountDollars')

def getcity(merged_df):
    # Assuming 'Order_Date' is a column in 'sales_order_df'
    # Ensure the 'OrderDate' column is converted to datetime objects
    merged_df['OrderDate'] = pd.to_datetime(merged_df['OrderDate'], errors='coerce')
    # Calculate daily gross revenue
    location_city = merged_df.groupby(merged_df['ShipCity'])['ShipCity'].sum()
    return location_city.reset_index(name='ShipCity')
