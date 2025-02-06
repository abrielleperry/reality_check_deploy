from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import data_processing as dp
import plotly.express as px
import pandas as pd
from geopy.geocoders import Nominatim


def create_daily_revenue_line_chart():

    #get dataset merging two collections orders and order details
    merged_df = dp.get_merged_df()
    # Calculate daily revenue
    #daily_revenue = dp.compute_daily_revenue(order_details_df)
    
    # Calculate daily revenue from the merged DataFrame
    daily_revenue = dp.compute_daily_revenue(merged_df)


    # Create a line chart
    fig = px.line(daily_revenue, x='OrderDate', y='LineTotal',
                labels={'OrderDate': 'Order Date', 'LineTotal': 'Gross Revenue'},
                title='Daily Gross Revenue')
    fig.update_layout(xaxis_title='Order Date', yaxis_title='Gross Revenue ($)')
    
    return fig

def create_daily_revenue_bar_chart():
    #get dataset merging two collections orders and order details
    merged_df = dp.get_merged_df()
    
    # Ensure the Order_Date column is in datetime format
    merged_df['OrderDate'] = pd.to_datetime(merged_df['OrderDate'])

    # Calculate daily revenue from the merged DataFrame
    #daily_revenue_df = dp.compute_daily_revenue(merged_df)
    gross_revenue, net_revenue, DiscountDollars = dp.calculate_gross_revenue(merged_df)
    
    # Create a bar chart
    fig = px.bar(merged_df, x='OrderDate', y='DiscountDollars',
                 labels={'OrderDate': 'Order Date', 'DiscountDollars': 'Discount ($)'},
                 title='Daily Discount Applied')
    fig.update_layout(xaxis_title='Order Date', yaxis_title='Discount ($)', bargap=0.2)

    return fig

# Function to get latitude and longitude
def get_lat_lon(city):
    # Initialize geocoder
    geolocator = Nominatim(user_agent="geomapnorthwind")
    location = geolocator.geocode(city)
    if location is not None:
        location = geolocator.geocode(city)
        return location.latitude, location.longitude
    else:
        print("Location not found")
    

def create_sales_map():
    #get dataset merging two collections orders and order details
    df = dp.get_merged_df()
    unique_cities = df['ShipCity'].unique()

    gross_revenue, net_revenue, discount_dollars = dp.calculate_gross_revenue(df)
    print(df.columns)
    #hard code because takes too long to fetch and there is a limit
    city_data = [
    ['Reims', 49.257789, 4.031926],
    ['Münster', 51.962510, 7.625188],
    ['Rio de Janeiro', -22.911014, -43.209373],
    ['Lyon', 45.757814, 4.832011],
    ['Charleroi', 50.411623, 4.444528],
    ['Bern', 46.948474, 7.452175],
    ['Genève', 46.204717, 6.142311],
    ['Resende', -22.441870, -44.420485],
    ['San Cristóbal', 18.520090, -70.207677],
    ['Graz', 47.070868, 15.438279],
    ['México D.F.', 19.432630, -99.133178],
    ['Köln', 50.938361, 6.959974],
    ['Albuquerque', 35.084103, -106.650985],
    ['Bräcke', 62.783333, 15.666667],
    ['Strasbourg', 48.584614, 7.750713],
    ['Oulu', 65.011873, 25.471681],
    ['München', 48.137108, 11.575382],
    ['Caracas', 10.506093, -66.914601],
    ['Seattle', 47.603832, -122.330062],
    ['Lander', 39.905988, -116.984337],
    ['Cunewalde', 51.098481, 14.514475],
    ['Bergamo', 45.756656, 9.754219],
    ['Leipzig', 51.340632, 12.374733],
    ['Luleå', 65.583119, 22.145954],
    ['Frankfurt a.M.', 50.110644, 8.682092],
    ['Madrid', 40.416705, -3.703582],
    ['Barquisimeto', 10.077437, -69.322229],
    ['Reggio Emilia', 44.608667, 10.594067],
    ['London', 51.489334, -0.144055],
    ['Sao Paulo', -23.550651, -46.633382],
    ['Cork', 51.897077, -8.465467],
    ['Stuttgart', 48.778449, 9.180013],
    ['Sevilla', 37.388630, -5.995340],
    ['Anchorage', 61.216313, -149.894852],
    ['Portland', 45.520247, -122.674194],
    ['Nantes', 47.218637, -1.554136],
    ['Cowes', 50.763318, -1.298519],
    ['Brandenburg', 52.845549, 13.246130],
    ['Boise', 43.616616, -116.200886],
    ['Lisboa', 38.707751, -9.136592],
    ['Marseille', 43.296174, 5.369953],
    ['Montréal', 45.503182, -73.569806],
    ['København', 55.686724, 12.570072],
    ['Toulouse', 43.604462, 1.444247],
    ['Salzburg', 47.798135, 13.046481],
    ['Colchester', 51.889690, 0.899465],
    ['Aachen', 50.776351, 6.083862],
    ['Barcelona', 41.382894, 2.177432],
    ['Århus', 56.149628, 10.213405],
    ['Warszawa', 52.233717, 21.071432],
    ['Elgin', 42.037260, -88.281099],
    ['Stavern', 52.797273, 7.434552],
    ['Tsawassen', 123.05, 49.01],
    ['I. de Margarita', 11.020560, -63.907398],
    ['Lille', 50.636565, 3.063528],
    ['Buenos Aires', -34.603718, -58.381530],
    ['Torino', 45.067755,  7.682489],
    ['Campinas',  -22.905639,   -47.059564]]
    
    # Create DataFrame with specified column names and merge
    df_cities = pd.DataFrame(city_data, columns=['ShipCity', 'Latitude', 'Longitude'])
    df = pd.merge(df, df_cities, on='ShipCity', how='outer')
    
    unique_cities_countries = df[['ShipCity', 'ShipCountry']].drop_duplicates()
    df_cities = pd.merge(df_cities, unique_cities_countries, on='ShipCity', how='outer')
    #print(df_cities)
    
    
    #this code will get it dynamically but if too many have to pay
    # Apply get_lat_lon function to each city and create a DataFrame
    # city_coords = {city: plot.get_lat_lon(city) for city in unique_cities}
    # coords_df = pd.DataFrame(city_coords.items(), columns=['City', 'Coordinates'])

    # # Split the 'Coordinates' tuple into two separate columns
    # coords_df[['Latitude', 'Longitude']] = pd.DataFrame(coords_df['Coordinates'].tolist(), index=coords_df.index)
    # coords_df.drop(columns=['Coordinates'], inplace=True)  # Optional: remove the combined column

    #print(coords_df)

    mean_lat = df_cities['Latitude'].mean()
    mean_lon = df_cities['Longitude'].mean()

    # Calculate daily revenue from the merged DataFrame
    location_netrevenue = dp.compute_location_netrevenue(df)
    # add lat and lon
    location_netrevenue = pd.merge(location_netrevenue, df_cities, on='ShipCity', how='outer')
    #location_netrevenue = pd.merge(location_netrevenue, df, on='ShipCity', how='outer')
    #add shipCountry to location_netrevenue df
    #location_netrevenue = pd.merge(location_netrevenue, df[['ShipCity','ShipCountry']], on='ShipCity', how='outer')
    
    # df1 = location_netrevenue
    # df2 = df
    # df1 = pd.merge(df1, df2[['ShipCity', 'ShipCountry']],
    #            on='ShipCity', how='left', suffixes=('_x', '_drop'))

    # # Drop the _drop columns
    # df1 = df1[df1.columns.drop(list(df1.filter(regex='_drop')))]
    # location_netrevenue = df1
    
    #print(location_netrevenue)
    map_center = {"lat": mean_lat, "lon": mean_lon}
    
    # Assuming 'location_netrevenue' is your DataFrame
    location_netrevenue['Latitude'] = pd.to_numeric(location_netrevenue['Latitude'], errors='coerce')
    location_netrevenue['Longitude'] = pd.to_numeric(location_netrevenue['Longitude'], errors='coerce')

    # Check for any NaN values that were introduced
    #print(location_netrevenue[['Latitude', 'Longitude']].isna().sum())
    
    # Convert 'NetRevenue' to numeric, coercing errors to NaN
    location_netrevenue['NetRevenue'] = pd.to_numeric(location_netrevenue['NetRevenue'], errors='coerce')

    # Check for NaN values in 'NetRevenue'
    nan_count_netrevenue = location_netrevenue['NetRevenue'].isna().sum()
    print(f"NaN values in NetRevenue: {nan_count_netrevenue}")

    print(location_netrevenue.dtypes)
    print(location_netrevenue.head())

    # Create a map using Plotly Express
    fig = px.scatter_mapbox(location_netrevenue,
                            lat='Latitude', 
                            lon='Longitude', 
                            color='NetRevenue',
                            hover_name='ShipCity',                         
                            hover_data={
                            "ShipCountry": True,  # Confirm column name is exactly "ShipCountry"
                            "NetRevenue": ":.2f"  # Assuming NetRevenue should be formatted as a float
                            },
                            size='NetRevenue',  # This will scale the size of the points based on the NetRevenue column
                            color_discrete_sequence=["fuchsia"],  # This sets the color scheme
                            size_max=15, 
                            zoom=1.5,  # Initial zoom level
                            center=map_center,  # Centers the map based on average lat and lon
                            title='Sales Locations', mapbox_style="open-street-map")  # The style of the map
    return fig

def create_revenue_chart():
    #get dataset merging two collections orders and order details
    
    merged_df = dp.get_merged_df()
    # unique_cities_countries = merged_df[['ShipCity', 'ShipCountry']].drop_duplicates()
    print("hello")
    #print(unique_cities_countries.columns)
    #gross_revenue, net_revenue, discount_dollars = dp.calculate_gross_revenue(merged_df)
    # Extract 'YearMonth' from 'ShippedDate'
    #unique_cities_countries['YearMonth'] = unique_cities_countries['OrderDate'].dt.strftime('%Y-%m')
    #merged_df['YearMonth'] = merged_df['OrderDate'].dt.strftime('%Y-%m')
    # Ensure the Order_Date column is in datetime format
    #merged_df['OrderDate'] = pd.to_datetime(merged_df['OrderDate'])


    #merged_df = pd.merge(merged_df, unique_cities_countries, on='ShipCity', how='outer')
    # Calculate daily revenue from the merged DataFrame
    #df = dp.compute_daily_revenue(merged_df)
    
    #Sdf['CountryCity'] = unique_cities_countries['ShipCountry'] + ' - ' + unique_cities_countries['ShipCity']
    print(merged_df.columns)
    # merged_df = merged_df.drop('ShipCountry_y', axis=1)
    # merged_df.rename(columns={'ShipCountry_x': 'ShipCountry'}, inplace=True)
    # print(merged_df.columns)
    # print("hello again 3")
    # print(unique_cities_countries.columns)
    
    # print(df.columns)
    #merged_df = pd.merge(merged_df, unique_cities_countries, on='OrderDate', how='outer')
    # print(merged_df.columns)
    # print(df.columns)
    # # Convert 'OrderDate' to datetime
    # df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    # # Create 'YearMonth' by formatting 'OrderDate'
    # df['YearMonth'] = df['OrderDate'].dt.strftime('%Y-%m')
    # print(df.columns)
    # print(merged_df.columns)
    # print("hello again 3")
    # print(df.columns)
    # merged_df = pd.merge(merged_df, df, on='OrderDate', how='outer')
    # print(merged_df.columns)
    
    # Reshaping the DataFrame using melt to make it suitable for a grouped bar chart
    df_melted = merged_df.melt(id_vars=['ShipCity', 'ShipCountry'], value_vars=['NetRevenue', 'Discount', 'LineTotal'],
                        var_name='Type', value_name='Amount')
   # print(df_melted.columns)
    #print(df_melted.head())


    fig = px.bar(merged_df, 
                x='ShipCity', 
                y='NetRevenue', 
                color='ShipCountry',  # Use country as color differentiation if still needed
                labels={'NetRevenue': 'Net Revenue ($)', 'ShipCity': 'City'},
                title='Net Revenue by City and Country')

    # Enhance layout
    fig.update_layout(
        xaxis={'categoryorder':'total descending'},  # Optionally sort bars by total descending order
        yaxis_title='Net Revenue ($)',
        legend_title='Country'
    )



    return fig