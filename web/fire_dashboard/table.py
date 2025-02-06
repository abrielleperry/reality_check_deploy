from dash import Dash, dcc, html, Input, Output, State, MATCH
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv('../data/fire.csv')

# Define default columns
default_column_x = 'date'
default_column_y = 'incident'
options = [{'label': str(col), 'value': col} for col in df.columns]
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    dbc.Row(
        dbc.Col(
            [
                html.H3("Fire Incident Data Visualization"),
                dbc.InputGroup(
                    [
                        dcc.Dropdown(
                            options=[
                                {
                                    'label': incident,
                                    'value': incident} for incident in df['incident'].unique() if pd.notna(incident)],
                            value=df['incident'].iloc[0] if pd.notna(
                                df['incident'].iloc[0]) else None,
                            id="pattern-match-country",
                            clearable=False,
                            style={
                                "width": "300px"},
                        ),
                        dbc.Button(
                            "Add Chart",
                            id="pattern-match-add-chart",
                            n_clicks=0),
                    ],
                    className="mb-3",
                ),
                html.Div(
                    id="pattern-match-container",
                    children=[],
                    className="mt-4"),
            ])),
    fluid=True,
)

def create_figure(column_x, column_y, incident):
    filtered_df = df[df['incident'] == incident]
    return go.Figure(data=[go.Table(
        header=dict(values=list(filtered_df.columns)),
        cells=dict(values=[filtered_df[col] for col in filtered_df.columns])
    )])

def make_card(n_clicks, incident):
    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    f"Figure {n_clicks + 1}",
                    dbc.Button(
                        "X",
                        id={"type": "dynamic-delete", "index": n_clicks},
                        n_clicks=0,
                        color="secondary",
                    ),
                ],
                className="text-end",
            ),
            dcc.Graph(
                id={"type": "dynamic-output", "index": n_clicks},
                style={"height": "800px", "width": "1000px"},
                figure=create_figure(default_column_x, default_column_y, incident),
            ),
            dcc.Dropdown(
                id={"type": "dynamic-dropdown-x", "index": n_clicks},
                options=options,
                value=default_column_x,
                clearable=False,
            ),
            dcc.Dropdown(
                id={"type": "dynamic-dropdown-y", "index": n_clicks},
                options=options,
                value=default_column_y,
                clearable=False,
            ),
        ],
        style={
            "width": "1000px",
            "height": "800px",
            "display": "inline-block"
        },
        className="m-1",
        id={"type": "dynamic-card", "index": n_clicks},
    )

@app.callback(
    Output("pattern-match-container", "children"),
    Input("pattern-match-add-chart", "n_clicks"),
    State("pattern-match-container", "children"),
    State("pattern-match-country", "value"),
)
def add_card(n_clicks, cards, incident):
    new_card = make_card(n_clicks, incident)
    cards.append(new_card)
    return cards

@app.callback(
    Output({"type": "dynamic-card", "index": MATCH}, "style"),
    Input({"type": "dynamic-delete", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def remove_card(_):
    return {"display": "none"}

@app.callback(
    Output({"type": "dynamic-output", "index": MATCH}, "figure"),
    Input({"type": "dynamic-dropdown-x", "index": MATCH}, "value"),
    Input({"type": "dynamic-dropdown-y", "index": MATCH}, "value"),
    Input("pattern-match-country", "value"),
)
def update_figure(column_x, column_y, incident):
    return create_figure(column_x, column_y, incident)

if __name__ == "__main__":
    app.run_server(debug=True)
