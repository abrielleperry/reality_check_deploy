import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Load the CSV data
df = pd.read_csv('data/tulsa-fire.csv')

# Assuming df is loaded here, let's add a print statement to confirm its initial state
print("Initial DataFrame:")
print(df.head())


# Initialize Dash app
#Creating the Dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Using coerce to handle any parsing errors

# Check DataFrame after conversion
print("\nDataFrame after converting 'date' to datetime:")
print(df.head())

# Create a new column for 'year-month' format
df['month_year'] = df['date'].dt.to_period('M')

# Check DataFrame after adding 'month_year'
print("\nDataFrame after adding 'month_year' column:")
print(df.head())

# Group by the new 'month_year' column and count incidents
monthly_incidents = df.groupby('month_year').size().reset_index(name='counts')

# Print the grouped data
print("\nMonthly incidents count:")
print(monthly_incidents)


# Define the layout of the app
app.layout = html.Div([
    html.H1("Incidents Per Month"),
    dcc.Graph(
        id='incident-bar-graph',
        figure={
            'data': [
                {'x': monthly_incidents['month_year'].astype(str), 'y': monthly_incidents['counts'], 'type': 'bar'}
            ],
            'layout': {
                'title': 'Monthly Incident Counts',
                'xaxis': {'title': 'Month-Year'},
                'yaxis': {'title': 'Number of Incidents'},
            }
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# app.layout = html.Div([
#     dcc.Graph(
#         figure={
#             'data': [{'x': monthly_incidents['month_year'], 'y': monthly_incidents['counts'], 'type': 'bar'}],
#             'layout': {
#                 'title': 'Incidents Per Month'
#             }
#         }
#     )
# ])
