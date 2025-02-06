import dash
from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
import pickle
import dash_bootstrap_components as dbc

# Initialize Dash application with Bootstrap
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Interactive Incident Report and Prediction",
)


def initialize_data():
    static_df = pd.read_csv("../data/fire.csv")
    static_df.dropna(subset=["incident"], inplace=True)
    static_df["incident"] = static_df["incident"].astype(str)
    static_df["date"] = pd.to_datetime(static_df["date"])
    monthly_incidents = (
        static_df.groupby([static_df["date"].dt.strftime("%Y-%m"), "incident"])
        .size()
        .reset_index(name="count")
    )
    monthly_incidents.columns = ["month", "incident", "count"]

    url = "https://www.cityoftulsa.org/apps/opendata/tfd_dispatch.jsn"
    live_df = pd.read_json(url)
    incidents = pd.json_normalize(live_df["Incidents"]["Incident"])
    incidents["Latitude"] = pd.to_numeric(
        incidents["Latitude"], errors="coerce")
    incidents["Longitude"] = pd.to_numeric(
        incidents["Longitude"], errors="coerce")
    incidents["ResponseDate"] = pd.to_datetime(
        incidents["ResponseDate"], format="%m/%d/%Y %I:%M:%S %p"
    )

    problems = incidents["Problem"].unique()

    # Prepare data for the heatmap
    static_df["time"] = pd.to_datetime(
        static_df["time"], format="%H:%M:%S").dt.hour
    pivot_table = static_df.pivot_table(
        index="time", columns="incident", aggfunc="size", fill_value=0
    )

    return static_df, monthly_incidents, problems, incidents, pivot_table


static_df, monthly_incidents, problems, incidents, pivot_table = initialize_data()

# Load machine learning model and features
with open("pickle/model.pkl", "rb") as f:
    model = pickle.load(f)
with open("pickle/feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)

# Define application layout
app.layout = dbc.Container(
    [
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(
                    label="Interactive Incident Report",
                    value="tab-report"),
                dcc.Tab(
                    label="Predictive Analysis",
                    value="tab-predict"),
            ],
        ),
        html.Div(
            id="tabs-content"),
    ])


@app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "tab-report":
        return html.Div([dbc.Row([dbc.Col([html.Label("Select Incident Type:"),
                                           dcc.Dropdown(id="incident-type-dropdown",
                                                        options=[{"label": i,
                                                                  "value": i} for i in static_df["incident"].dropna().unique()],
                                                        value=static_df["incident"].dropna().unique()[0],
                                                        multi=True,
                                                        ),
                                           dcc.Graph(id="action-taken-bar-chart"),
                                           ],
                                          md=4,
                                          ),
                                  dbc.Col([html.Label("Select Problems:"),
                                           dbc.Checklist(id="problem-filter",
                                                         options=[{"label": "Unselect All",
                                                                   "value": "None"},
                                                                  {"label": "Select All",
                                                                   "value": "All"},
                                                                  ] + [{"label": problem,
                                                                        "value": problem} for problem in problems],
                                                         value=["All"],
                                                         inline=False,
                                                         ),
                                           dcc.Graph(id="incident-map",
                                                     style={"width": "100%",
                                                            "height": "600px"},
                                                     ),
                                           ],
                                          md=8,
                                          ),
                                  ]),
                         html.Div([html.H1("Live Incident Pie Chart"),
                                   dcc.Graph(id="live-incident-pie-chart"),
                                   ]),
                         html.Div([html.H1("Incident Reports Over Months"),
                                   dcc.Dropdown(id="incident-dropdown",
                                   options=[{"label": i,
                                             "value": i} for i in static_df["incident"].unique() if i is not None],
                                   value=static_df["incident"].unique()[0],
                                   ),
                                   dcc.Graph(id="incident-over-months-chart"),
                                   ]),
                         html.Div([html.H1("Time and Incident Correlation"),
                                   dcc.RangeSlider(id="time-range-slider",
                                                   min=0,
                                                   max=23,
                                                   step=1,
                                                   marks={i: f"{i:02d}:00" for i in range(24)},
                                                   value=[0,
                                                          23],
                                                   ),
                                   dcc.Graph(id="heatmap-graph"),
                                   ]),
                         ])
    elif tab == "tab-predict":
        return html.Div(
            [
                html.H1("Incident Prediction"),
                dcc.DatePickerSingle(
                    id="input-date",
                    min_date_allowed=pd.to_datetime("2024-05-01"),
                    max_date_allowed=pd.to_datetime("2025-05-01"),
                    initial_visible_month=pd.to_datetime("2024-05-01"),
                    date=str(pd.to_datetime("2024-05-01")),
                ),
                html.Button("Predict", id="predict-button", n_clicks=0),
                html.Div(id="prediction-output", style={"margin": "20px"}),
                dcc.Graph(id="feature-importance-plot"),
            ]
        )


@app.callback(
    Output("prediction-output", "children"),
    Input("predict-button", "n_clicks"),
    State("input-date", "date"),
)
def update_output(n_clicks, date):
    if n_clicks > 0:
        features_df = pd.DataFrame(
            np.random.rand(1, len(feature_names)), columns=feature_names
        )
        prediction = model.predict(features_df)[0]
        return f"Predicted number of incidents on {date}: {prediction:.0f}"


@app.callback(Output("feature-importance-plot", "figure"),
              Input("predict-button", "n_clicks"))
def update_graph(n_clicks):
    if n_clicks > 0:
        importances = model.feature_importances_
        df = pd.DataFrame(
            {"Feature": feature_names, "Importance": importances})
        fig = px.bar(
            df,
            x="Feature",
            y="Importance",
            title="Feature Importances")
        return fig
    return dash.no_update


# Additional callbacks for other charts, graphs, and functionalities


# Fetch live incident data for pie chart
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


# ACTION TAKEN
@app.callback(Output("action-taken-bar-chart", "figure"),
              Input("incident-type-dropdown", "value"))
def update_action_taken_chart(selected_incidents):
    if not isinstance(selected_incidents, list):
        selected_incidents = [selected_incidents]
    if not selected_incidents:
        return px.bar()
    filtered_df = static_df[static_df["incident"].isin(selected_incidents)]
    count_df = filtered_df.groupby(
        "action_taken").size().reset_index(name="counts")
    return px.bar(
        count_df,
        x="action_taken",
        y="counts",
        title="Count of Actions Taken for Selected Incident Types",
        labels={"counts": "Count of Actions Taken"},
        height=500,
    )


#################


# INCIDENTS OVER MONTHS
@app.callback(Output("incident-over-months-chart", "figure"),
              Input("incident-dropdown", "value"))
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


#################


# INCIDENT MAP
@app.callback(
    Output("incident-map", "figure"),
    [Input("problem-filter", "value")],
)
def update_map(selected_problems):
    if "All" in selected_problems:
        selected_problems = problems.tolist()
    filtered_data = incidents[(incidents["Problem"].isin(selected_problems))]
    return px.scatter_mapbox(
        filtered_data,
        lat="Latitude",
        lon="Longitude",
        hover_name="Problem",
        hover_data=["ResponseDate", "IncidentNumber"],
        color_discrete_sequence=["fuchsia"],
        zoom=10,
        center={"lat": 36.1540, "lon": -95.9928},
        title="Incident Locations",
        mapbox_style="open-street-map",
    )


#################


# LIVE PIE CHART
@app.callback(Output("live-incident-pie-chart", "figure"),
              [Input("problem-filter", "value")])
def update_live_incident_pie_chart(_):
    return fetch_live_data()


#################


# SELECT ALL
@app.callback(
    Output("problem-filter", "value"),
    [Input("problem-filter", "value")],
    [State("problem-filter", "options")],
)
def select_all_problems(selected_problems, options):
    if "All" in selected_problems and "None" not in selected_problems:
        return [option["value"]
                for option in options if option["value"] != "None"]
    elif "None" in selected_problems:
        return []
    return selected_problems


#################


# TIME AND INCIDENT
@app.callback(Output("heatmap-graph", "figure"),
              Input("time-range-slider", "value"))
def update_heatmap(time_range):
    filtered_data = static_df[(static_df["time"] >= time_range[0]) & (
        static_df["time"] <= time_range[1])]
    filtered_pivot = filtered_data.pivot_table(
        index="time", columns="incident", aggfunc="size", fill_value=0
    )
    fig = px.imshow(
        filtered_pivot,
        labels=dict(
            x="Incident Type",
            y="Hour of Day",
            color="Number of Incidents"),
        x=filtered_pivot.columns,
        y=filtered_pivot.index,
        aspect="auto",
    )
    fig.update_layout(
        title="Correlation between Time of Day and Incident Types",
        xaxis_nticks=36)
    return fig


#################


if __name__ == "__main__":
    app.run_server(debug=True)
