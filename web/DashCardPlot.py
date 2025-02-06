from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import data_processing as dp
import plotly.express as px
import pandas as pd

# Assuming 'order_details_df' is already fetched somewhere in your code
order_details_df = dp.fetch_order_details()
sales_order_df = dp.fetch_sales_order()
print(sales_order_df.columns)
print(order_details_df.columns)
# Ensure that 'OrderID' is of the same type in both DataFrames
sales_order_df['OrderID'] = sales_order_df['OrderID'].astype(str)
order_details_df['OrderID'] = order_details_df['OrderID'].astype(str)
gross_revenue = dp.calculate_gross_revenue(order_details_df)
# Merge the two DataFrames on 'OrderID'
merged_df = pd.merge(sales_order_df, order_details_df, on='OrderID')

# Check columns after merge
print(merged_df.columns)

# If 'Gross_Revenue' column is not found, raise an error
if 'LineTotal' not in merged_df.columns:
    raise KeyError("Column 'LineTotal' not found after merging dataframes.")
# Calculate daily revenue
#daily_revenue = dp.compute_daily_revenue(order_details_df)

# Calculate daily revenue from the merged DataFrame
daily_revenue = dp.compute_daily_revenue(merged_df)


# Create a line chart
fig = px.line(daily_revenue, x='OrderDate', y='LineTotal',
              labels={'OrderDate': 'Order Date', 'LineTotal': 'Gross Revenue'},
              title='Daily Gross Revenue')
fig.update_layout(xaxis_title='Order Date', yaxis_title='Gross Revenue ($)')


# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set up the app layout
app.layout = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Gross Revenue Over Time", className="card-title"),
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
