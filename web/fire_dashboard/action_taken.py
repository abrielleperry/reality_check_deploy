import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv("../data/fire.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Incident Report"),
    html.Label("Select Incident Type:"),
    dcc.Dropdown(
        id='incident-type-dropdown',
        options=[{'label': i, 'value': i}
                 for i in df['incident'].dropna().unique()],
        value=[df['incident'].dropna().unique()[0]],
        multi=True
    ),
    dcc.Graph(id='action-taken-bar-chart')
])


@app.callback(
    Output('action-taken-bar-chart', 'figure'),
    [Input('incident-type-dropdown', 'value')]
)
def update_action_taken_chart(selected_incidents):
    if not selected_incidents:
        return px.bar()
    filtered_df = df[df['incident'].isin(selected_incidents)]
    count_df = filtered_df.groupby('action_taken').size(
    ).reset_index(name='counts')
    fig = px.bar(
        count_df,
        x='action_taken',
        y='counts',
        title="Count of Actions Taken for Selected Incident Types",
        labels={'counts': 'Count of Actions Taken'},
        height=500
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
