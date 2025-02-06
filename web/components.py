# components.py

import dash_bootstrap_components as dbc
from dash import Dash, html, dcc


def create_small_card(gross_revenue, fig):
    small_card = dbc.Card(
        [
            dbc.CardBody(
                [                   
                    html.H4("Gross Revenue", className="card-title"),
                    html.H5(f"${gross_revenue:,.2f}", className="card-text"),
                    dcc.Graph(figure=fig)
                ]
            ),
        ],
        style={"width": "100%"}
    )
    return small_card

def create_small_barcard(discountdollars, fig):
    small_card = dbc.Card(
        [
            dbc.CardBody(
                [                   
                    html.H4("Discount ($)", className="card-title"),
                    html.H5(f"${discountdollars:,.2f}", className="card-text"),
                    dcc.Graph(figure=fig)
                ]
            ),
        ],
        style={"width": "100%"}
    )
    return small_card

def create_revenue_card(net_revenue, fig):
    small_card = dbc.Card(
        [
            dbc.CardBody(
                [                   
                    html.H4("Net Revenue", className="card-title"),
                    html.H5(f"${net_revenue:,.2f}", className="card-text"),
                    dcc.Graph(figure=fig)
                ]
            ),
        ],
        style={"width": "100%"}
    )
    return small_card

def create_map_card(net_revenue, fig):
    small_card = dbc.Card(
        [
            dbc.CardBody(
                [                   
                    html.H4("Net Sales Location Map", className="card-title"),
                    html.H5(f"${net_revenue:,.2f}", className="card-text"),
                    dcc.Graph(figure=fig)
                ]
            ),
        ],
        style={"width": "100%"}
    )
    return small_card
