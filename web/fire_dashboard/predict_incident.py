import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import pickle


with open("pickle/model.pkl", "rb") as f:
    model = pickle.load(f)
with open("pickle/feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)

    app = dash.Dash(
        __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    )

    app.layout = html.Div(
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
        dash.dependencies.State("input-date", "date"),
    )
    def update_output(n_clicks, date):
        if n_clicks > 0:
            features_df = pd.DataFrame(
                np.random.rand(1, len(feature_names)), columns=feature_names
            )
            prediction = model.predict(features_df)[0]
            return f"Predicted number of incidents on {date}: {prediction:.0f}"

    @app.callback(
        Output("feature-importance-plot", "figure"), Input("predict-button", "n_clicks")
    )
    def update_graph(n_clicks):
        if n_clicks > 0:
            importances = model.feature_importances_
            df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
            fig = px.bar(df, x="Feature", y="Importance", title="Feature Importances")
            return fig
        return dash.no_update

    if __name__ == "__main__":
        app.run_server(debug=True)
