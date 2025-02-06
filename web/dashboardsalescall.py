import dash
from dash import html, dcc 
from flask import Flask
import data_processing as dp
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from components import create_small_card  # Import the function from the components module
from components import create_map_card
from components import create_revenue_card
from components import create_small_barcard
from plot_grids import create_daily_revenue_bar_chart
from plot_grids import create_daily_revenue_line_chart
from plot_grids import create_sales_map
from plot_grids import create_revenue_chart
import pandas as pd


def create_dash_app2(flask_app):
    dash_app2 = dash.Dash(__name__, server=flask_app, routes_pathname_prefix='/app2/',
                          external_stylesheets=[dbc.themes.BOOTSTRAP])
       
    # Fetch and calculate the gross revenue
    #order_details_df = dp.fetch_order_details()
    df = dp.get_merged_df()
    gross_revenue, net_revenue, discount_dollars = dp.calculate_gross_revenue(df)
    print("hey")
    print(df.columns)
    # Create the bar chart figure using the imported function
    figline = create_daily_revenue_line_chart()
    figbar = create_daily_revenue_bar_chart()
    figmap = create_sales_map()
    figbarlocation = create_revenue_chart()


    # Create the small card component by calling the function
    small_linecard = create_small_card(gross_revenue, figline)
    small_barcard = create_small_barcard(discount_dollars, figbar)
    small_figmap = create_map_card(net_revenue, figmap)
    revenue_chart = create_revenue_card(net_revenue, figbarlocation)

    #========================
    # Extract 'YearMonth' from 'ShippedDate'

    # df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    # df['YearMonth'] = df['OrderDate'].dt.strftime('%Y-%m')
    # df['CountryCity'] = df['ShipCountry'] + ' - ' + df['ShipCity']
    # df['YearMonthInt'] = df['OrderDate'].dt.strftime('%Y%m').astype(int)

    df['CountryCity'] = df['ShipCountry'] + ' - ' + df['ShipCity']
    # Creating options for the dropdown
    options = [{'label': i, 'value': i} for i in df['CountryCity'].unique()]

    dash_app2.layout = html.Div([
        html.H1("Net Revenue by Country/City"),
        dcc.Dropdown(
            id='country-city-dropdown',
            options=options,
            value=options[0]['value'],  # Default value
            multi=False  # Single selection
        ),
        dcc.Graph(id='revenue-chart')
    ])

    @dash_app2.callback(
        Output('revenue-chart', 'figure'),
        [Input('country-city-dropdown', 'value')]
    )
    def update_chart(selected_country_city):
        filtered_df = df[df['CountryCity'] == selected_country_city]
        fig = px.bar(filtered_df, x='CountryCity', y='NetRevenue', title='Net Revenue')
        return fig

    #========================


    # Set up the app layout with the small card
    dash_app2.layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(small_linecard, width=12, lg=6, md=6),
                    dbc.Col(small_barcard, width=12, lg=6, md=6)
                ],
                className="mb-4"  # Margin bottom for spacing between rows
            ),
            dbc.Row(
                [
                    dbc.Col(revenue_chart, width=12, lg=12, md=12),
                ],
                className="mb-4"
            ),
            dbc.Row(
                [
                    #dbc.Col(small_figmap, width=12, lg=8, md=8),
                    dbc.Col(small_figmap, width=12, lg=12, md=8),

                ],
                className="mb-4"
            )
        ],
        fluid=True,
    )

    return dash_app2
# Run the app
# Run the Flask server
if __name__ == '__main__':
    flask_app.run(debug=True)
