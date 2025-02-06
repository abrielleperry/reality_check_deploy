import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

url = "https://www.cityoftulsa.org/apps/opendata/tfd_dispatch.jsn"
data = pd.read_json(url)

incidents = pd.json_normalize(data["Incidents"][0])


incident_counts = incidents["Problem"].value_counts().reset_index()
incident_counts.columns = ["Problem", "count"]

fig = px.pie(incident_counts, values="count", names="Problem", title="")

app = Dash(__name__)

app.layout = html.Div([dcc.Graph(figure=fig)])

if __name__ == "__main__":
    app.run_server(debug=True)
