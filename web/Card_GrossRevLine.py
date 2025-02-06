from dash import Dash, html, dcc
from plot_grids import create_daily_revenue_line_chart
import dash_bootstrap_components as dbc
import data_processing as dp
import plotly.express as px
import pandas as pd

# Fetch and calculate the gross revenue
order_details_df = dp.fetch_order_details()
gross_revenue = dp.calculate_gross_revenue(order_details_df)

# Create the bar chart figure using the imported function
fig = create_daily_revenue_line_chart()
# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# Set up the app layout
app.layout = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        # html.H4("Gross Revenue Over Time", className="card-title"),
                        # dcc.Graph(figure=fig)
                        
                        html.H4("Gross Revenue", className="card-title"),
                        html.H5(f"${gross_revenue:,.2f}", className="card-text"),
                        dcc.Graph(figure=fig)
                    ]
                ),
            ],
            className="mt-5",
        ),
    ],
    fluid=True,
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)