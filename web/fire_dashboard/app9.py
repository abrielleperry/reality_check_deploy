import dash
from dash import html, dcc 
from flask import Flask
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def create_dash_app1(flask_app):# Initialize Dash application with Bootstrap
    dash_app1 = dash.Dash(__name__, server=flask_app, routes_pathname_prefix='/app1/',
                          external_stylesheets=[dbc.themes.BOOTSTRAP],
                          title="Interactive Incident Report")

    navbar = dbc.NavbarSimple(
        #    children=[
        #       dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        #      dbc.DropdownMenu(
        #         nav=True,
        #        in_navbar=True,
        #       label="More",
        #  ),
        # ],
        brand="Reality Check",
        brand_href="#",
        color="info",
        dark=True,
    )


    def initialize_data():
        static_df = pd.read_csv("data/fire.csv").dropna(subset=["incident"])
        df = static_df[~static_df["location_name"].isin(["HSE", "0"])]
        static_df["incident"] = static_df["incident"].astype(str)
        static_df["date"] = pd.to_datetime(static_df["date"])
        static_df["time"] = pd.to_datetime(static_df["time"], format="%H:%M:%S").dt.hour
        monthly_incidents = (
            static_df.groupby([static_df["date"].dt.strftime("%Y-%m"), "incident"])
            .size()
            .reset_index(name="count")
        )
        monthly_incidents.columns = ["month", "incident", "count"]  # Correct column names

        url = "https://www.cityoftulsa.org/apps/opendata/tfd_dispatch.jsn"
        incidents = pd.json_normalize(pd.read_json(url)["Incidents"]["Incident"])
        incidents["Latitude"] = pd.to_numeric(incidents["Latitude"], errors="coerce")
        incidents["Longitude"] = pd.to_numeric(incidents["Longitude"], errors="coerce")
        incidents["ResponseDate"] = pd.to_datetime(
            incidents["ResponseDate"], format="%m/%d/%Y %I:%M:%S %p"
        )

        pivot_table = static_df.pivot_table(
            index="time", columns="incident", aggfunc="size", fill_value=0
        )

        return (
            df,
            static_df,
            monthly_incidents,
            incidents["Problem"].unique(),
            incidents,
            pivot_table,
        )


    df, static_df, monthly_incidents, problems, incidents, pivot_table = initialize_data()

    dash_app1.layout = dbc.Container(
        [
            navbar,
            html.H1(
                "Interactive Incident Report",
                style={"textAlign": "center", "marginTop": 20},
            ),
            dbc.Container(
                [
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
                                md=6,
                                style={"padding": 10},
                            ),
                            dbc.Col(
                                [
                                    dcc.Graph(id="live-incident-pie-chart"),
                                ],
                                md=6,
                                style={"padding": 10},
                            ),
                        ],
                        style={"marginTop": 10},
                    ),
                ]
            ),
            dbc.Placeholder(color="info", className="me-1 mt-1 w-100"),
            dbc.Container(
                [html.H2("Live Incident Map")],
                style={"textAlign": "center", "marginTop": 20},
            ),
            dbc.Row(
                [
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
                        ]
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(
                                id="incident-map",
                                style={"width": "900px", "height": "600px"},
                            ),
                        ]
                    ),
                ],
                style={"marginTop": 20},
            ),
            dbc.Placeholder(color="info", className="me-1 mt-1 w-100"),
            dbc.Container(
                [html.H2("Incident Reports Over Months")],
                style={"textAlign": "center", "marginTop": 20},
            ),
            dbc.Row(
                [
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
            dbc.Placeholder(color="info", className="me-1 mt-1 w-100"),
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
            dbc.Placeholder(color="info", className="me-1 mt-1 w-100"),
            html.Div(
                [
                    html.H2("Location Distribution"),
                    dcc.Graph(id="location_name-chart", style={"height": "500px"}),
                ],
                style={"marginTop": 20, "marginBottom": 20},
            ),
        ],
        fluid=True,
    )


    def fetch_live_data():
        url = "https://www.cityoftulsa.org/apps/opendata/tfd_dispatch.jsn"
        live_data = pd.read_json(url)
        incidents = pd.json_normalize(live_data["Incidents"][0])
        incident_counts = incidents["Problem"].value_counts().reset_index()
        incident_counts.columns = ["Problem", "count"]
        fig = px.pie(
            incident_counts,
            values="count",
            names="Problem",
            title="Live Incident Types over the Last 24 Hours",
        )
        return fig
    return dash_app1

    @dash.app1.callback(
        Output("action-taken-bar-chart", "figure"), Input("incident-type-dropdown", "value")
    )
    def update_action_taken_chart(selected_incidents):
        if not selected_incidents:
            return px.bar()
        filtered_df = static_df[
            static_df["incident"].isin(
                selected_incidents
                if isinstance(selected_incidents, list)
                else [selected_incidents]
            )
        ]
        count_df = filtered_df.groupby("action_taken").size().reset_index(name="counts")
        return px.bar(
            count_df,
            x="action_taken",
            y="counts",
            title="",
            labels={"counts": "Count of Actions Taken"},
            height=500,
        )
    return dash_app1

    # INCIDENTS OVER MONTHS
    @dash_app1.callback(
        Output("incident-over-months-chart", "figure"), Input("incident-dropdown", "value")
    )
    def update_incidents_over_months_chart(selected_incident):
        filtered_data = monthly_incidents[
            monthly_incidents["incident"] == selected_incident
        ]
        return px.line(
            filtered_data,
            x="month",
            y="count",
            title=f"Monthly Count of {selected_incident}",
        )


    # INCIDENT MAP
    @dash_app1.callback(Output("incident-map", "figure"), [Input("problem-filter", "value")])
    def update_map(selected_problems):
        if "All" in selected_problems:
            selected_problems = problems.tolist()
        filtered_data = incidents[incidents["Problem"].isin(selected_problems)]
        return px.scatter_mapbox(
            filtered_data,
            lat="Latitude",
            lon="Longitude",
            hover_name="Problem",
            hover_data=["ResponseDate", "IncidentNumber"],
            color_discrete_sequence=["fuchsia"],
            zoom=10,
            center={"lat": 36.1540, "lon": -95.9928},
            title="",
            mapbox_style="open-street-map",
        )


    @dash_app1.callback(
        Output("live-incident-pie-chart", "figure"), [Input("problem-filter", "value")]
    )
    def update_live_incident_pie_chart(_):
        return fetch_live_data()


    @dash_app1.callback(
        Output("problem-filter", "value"),
        [Input("problem-filter", "value")],
        [State("problem-filter", "options")],
    )
    def select_all_problems(selected_problems, options):
        if "All" in selected_problems and "None" not in selected_problems:
            return [option["value"] for option in options if option["value"] != "None"]
        elif "None" in selected_problems:
            return []
        return selected_problems


    @dash_app1.callback(Output("heatmap-graph", "figure"), Input("time-range-slider", "value"))
    def update_heatmap(time_range):
        filtered_data = static_df[
            (static_df["time"] >= time_range[0]) & (static_df["time"] <= time_range[1])
        ]
        filtered_pivot = filtered_data.pivot_table(
            index="time", columns="incident", aggfunc="size", fill_value=0
        )
        fig = px.imshow(
            filtered_pivot,
            labels=dict(x="Incident Type", y="Hour of Day", color="Number of Incidents"),
            x=filtered_pivot.columns,
            y=filtered_pivot.index,
            aspect="auto",
        )
        fig.update_layout(
            title="Correlation between Time of Day and Incident Types", xaxis_nticks=36
        )
        return fig


    @dash_app1.pp.callback(
        dash.dependencies.Output("location_name-chart", "figure"),
        [dash.dependencies.Input("location_name-chart", "id")],
    )
    def update_area_chart(selected_property):
        location_name_counts = df["location_name"].value_counts().reset_index()
        location_name_counts.columns = ["location_name", "count"]
        filtered_counts = location_name_counts[
            location_name_counts["count"] > 100
        ].sort_values("count", ascending=False)
        if filtered_counts.empty:
            return px.bar(title="No data to display.")
        fig = px.bar(filtered_counts, x="count", y="location_name", title="Locations")
        fig.update_xaxes(range=[0, max(filtered_counts["count"]) + 10])
        return fig


if __name__ == "__main__":
    flask_app.run(debug=True, port=8050)
