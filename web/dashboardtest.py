# app.py

from dash import Dash, html, dcc
import data_processing as dp
import dash_bootstrap_components as dbc
from dash import html
from components import create_small_card  # Import the function from the components module
from plot_grids import create_daily_revenue_bar_chart
from plot_grids import create_daily_revenue_line_chart
from plot_grids import create_sales_map

# Fetch and calculate the gross revenue
order_details_df = dp.fetch_order_details()
gross_revenue = dp.calculate_gross_revenue(order_details_df)

# Create the bar chart figure using the imported function
figline = create_daily_revenue_line_chart()
figbar = create_daily_revenue_bar_chart()
figmap = create_sales_map()
# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the small card component by calling the function
small_linecard = create_small_card(gross_revenue, figline)
small_barcard = create_small_card(gross_revenue, figbar)
small_figmap = create_map_card(figmap)
# Set up the app layout with the small card
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(small_linecard, width=12, lg=4, md=6),
                dbc.Col(small_barcard, width=12, lg=4, md=6),
                dbc.Col(small_linecard, width=12, lg=4, md=6)
            ],
            className="mb-4"  # Margin bottom for spacing between rows
        ),
        dbc.Row(
            [
                dbc.Col(small_figmap, width=12, lg=8, md=8),
                dbc.Col(small_barcard, width=12, lg=4, md=6)
            ],
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(small_linecard, width=12, lg=4, md=6),
                dbc.Col(small_barcard, width=12, lg=4, md=6),
                dbc.Col(small_linecard, width=12, lg=4, md=6)
            ]
        )
    ],
    fluid=True,
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
