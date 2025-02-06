from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import data_processing as dp
import plotly.express as px
import pandas as pd
import plot_grids as plot

 #get dataset merging two collections orders and order details
df = dp.get_merged_df()
print(df.head())
print(df.columns)
# Calculate daily revenue from the merged DataFrame
#location_netrevenue_df = dp.compute_location_netrevenue(df)
# Set display options to expand DataFrame output
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)     # Show all rows
pd.set_option('display.width', 1000)        # Set display width to avoid line wrapping

# print(df.columns)
#  Now print the DataFrame
location_netrevenue_df = dp.compute_location_netrevenue(df)
print(location_netrevenue_df)

location_grossrevenue_df = dp.compute_location_grossrevenue(df)
print(location_grossrevenue_df)

location_discount_df = dp.compute_location_discount(df)
print(location_discount_df)

unique_cities = df['ShipCity'].unique()
unique_cities_countries = df[['ShipCity', 'ShipCountry']].drop_duplicates()

print(unique_cities)
print(unique_cities_countries)



# Merge the dataframes on 'City'
merged_df = pd.merge(location_netrevenue_df, location_grossrevenue_df, on='ShipCity', how='outer')
merged_df = pd.merge(merged_df, location_discount_df, on='ShipCity', how='outer')
#print(merged_df)



# # Apply get_lat_lon function to each city and create a DataFrame
# city_coords = {city: plot.get_lat_lon(city) for city in unique_cities}
# coords_df = pd.DataFrame(city_coords.items(), columns=['City', 'Coordinates'])

# # Split the 'Coordinates' tuple into two separate columns
# coords_df[['Latitude', 'Longitude']] = pd.DataFrame(coords_df['Coordinates'].tolist(), index=coords_df.index)
# coords_df.drop(columns=['Coordinates'], inplace=True)  # Optional: remove the combined column

# print(coords_df)

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
    
# Create DataFrame with specified column names
df_cities = pd.DataFrame(city_data, columns=['ShipCity', 'Latitude', 'Longitude'])
merged_df = pd.merge(merged_df, df_cities, on='ShipCity', how='outer')
print(merged_df)
print(merged_df.columns)