from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('../data/fire.csv')

df = df.dropna(subset=['incident'])
df['incident'] = df['incident'].astype(str)


df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.strftime('%Y-%m')

monthly_incidents = df.groupby(
    ['month', 'incident']).size().reset_index(name='count')

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Incident Reports Over Time"),
    dcc.Dropdown(
        id='incident-dropdown',
        options=[{'label': i, 'value': i}
                 for i in df['incident'].unique() if i is not None],
        value=df['incident'].unique()[0]
    ),
    dcc.Graph(id='incident-over-months-chart')
])


@app.callback(
    Output('incident-over-months-chart', 'figure'),
    Input('incident-dropdown', 'value'))
def update_incidents_over_months_chart(selected_incident):
    filtered_data = monthly_incidents[monthly_incidents['incident']
                                      == selected_incident]

    fig = px.line(filtered_data, x='month', y='count',
                  title=f'Monthly Count of {selected_incident}')
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Number of Incidents')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
