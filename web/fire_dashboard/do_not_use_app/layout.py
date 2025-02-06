# Define application layout
app.layout = dbc.Container(
    [
        # Header of the application
        html.H1(
            "Interactive Incident Report",
            style={"textAlign": "center", "marginTop": 20},
        ),
        # Row for incident type selection and associated actions
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select Incident Type:"),
                        dcc.Dropdown(
                            id="incident-type-dropdown",
                            options=[
                                {"label": i, "value": i}
                                for i in static_df["incident"].dropna().unique()
                            ],
                            value=static_df["incident"].dropna().unique()[0],
                            multi=True,
                            clearable=True,
                            searchable=True,
                        ),
                        dcc.Graph(id="action-taken-bar-chart"),
                    ],
                    md=4,
                    style={"padding": 10},
                ),
                dbc.Col(
                    [
                        html.Label("Select Problems:"),
                        dbc.Checklist(
                            id="problem-filter",
                            options=[
                                {"label": "Unselect All", "value": "None"},
                                {"label": "Select All", "value": "All"},
                            ]
                            + [
                                {"label": problem, "value": problem}
                                for problem in problems
                            ],
                            value=["All"],
                            inline=False,
                        ),
                        dcc.Graph(
                            id="incident-map",
                            style={"width": "100%", "height": "600px"},
                        ),
                    ],
                    md=8,
                    style={"padding": 10},
                ),
            ],
            style={"marginTop": 10},
        ),
        # Live Incident Pie Chart Section
        html.Div(
            [
                html.H2("Live Incident Pie Chart"),
                dcc.Graph(id="live-incident-pie-chart"),
            ],
            style={"marginTop": 20},
        ),
        # Incidents Reports Over Months Section
        html.Div(
            [
                html.H2("Incident Reports Over Months"),
                dcc.Dropdown(
                    id="incident-dropdown",
                    options=[
                        {"label": i, "value": i}
                        for i in static_df["incident"].unique()
                        if i is not None
                    ],
                    value=static_df["incident"].unique()[0],
                ),
                dcc.Graph(id="incident-over-months-chart"),
            ],
            style={"marginTop": 20},
        ),
        # Time and Incident Correlation Section
        html.Div(
            [
                html.H2("Time and Incident Correlation"),
                dcc.RangeSlider(
                    id="time-range-slider",
                    min=0,
                    max=23,
                    step=1,
                    marks={i: f"{i:02d}:00" for i in range(24)},
                    value=[0, 23],
                ),
                dcc.Graph(id="heatmap-graph"),
            ],
            style={"marginTop": 20},
        ),
        # Location Distribution Section
        html.Div(
            [
                html.H2("Location Distribution"),
                dcc.Graph(
                    id="location_name-chart",
                    style={"height": "500px"},
                ),
            ],
            style={"marginTop": 20, "marginBottom": 20},
        ),
    ],
    fluid=True,
)
