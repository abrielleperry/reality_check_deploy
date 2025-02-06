from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import data_processing as dp
import plotly.express as px
import DashCardPlot as fig

# Fetch and calculate the data
order_details_df = dp.fetch_order_details()
sales_order_df = dp.fetch_sales_order()
gross_revenue = dp.calculate_gross_revenue(order_details_df)

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set up the app layout
app.layout = dbc.Container(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Gross Revenue", className="card-title"),
                    html.P(f"${gross_revenue:,.2f}", className="card-text"),
                    dcc.Graph(figure=fig)
                ]
            ),
        ],
        className="mt-5",
    ),
    fluid=True,
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
