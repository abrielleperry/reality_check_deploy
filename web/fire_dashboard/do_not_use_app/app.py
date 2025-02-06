import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from dash.dependencies import Input, Output



app = Dash(__name__, title="Interactive Incident Report")

# Load the data
df = pd.read_csv("../data/fire.csv")

# Now that df is defined, you can perform operations on it
df = df.dropna(subset=['incident'])
df['incident'] = df['incident'].astype(str)

df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.strftime('%Y-%m')

monthly_incidents = df.groupby(
    ['month', 'incident']).size().reset_index(name='count')

# Define the app layout with structured rows and columns
app.layout = html.Div([
    html.H1("Interactive Incident Report"),
    html.Div([
        html.Div([
            html.Label("Select Incident Type:"),
            dcc.Dropdown(
                id='incident-type-dropdown',
                options=[{'label': i, 'value': i}
                         for i in df['incident'].dropna().unique()],
                value=df['incident'].dropna().unique()[0],
                multi=True
            ),
            dcc.Graph(id='action-taken-bar-chart')
        ], className="six columns"),
        html.Div([
            html.H1("Incident Reports Over Time"),
        dcc.Dropdown(
            id='incident-dropdown',
            options=[{'label': i, 'value': i}
                    for i in df['incident'].unique() if i is not None],
            value=df['incident'].unique()[0]
        ),
        dcc.Graph(id='incident-over-months-chart')
        ], className="six columns"),
    ], className="row")
])




# Callback for Action Taken chart
@app.callback(
    Output('action-taken-bar-chart', 'figure'),
    Input('incident-type-dropdown', 'value')
)
def update_action_taken_chart(selected_incidents):
    # Ensure selected_incidents is always a list even if it's a single value
    if not isinstance(selected_incidents, list):
        selected_incidents = [selected_incidents]
    
    if not selected_incidents:
        return px.bar()
    
    filtered_df = df[df['incident'].isin(selected_incidents)]
    count_df = filtered_df.groupby('action_taken').size().reset_index(name='counts')
    fig = px.bar(
        count_df,
        x='action_taken',
        y='counts',
        title="Count of Actions Taken for Selected Incident Types",
        labels={'counts': 'Count of Actions Taken'},
        height=500
    )
    return fig

# Callback for Incidents Over Months chart
@app.callback(
    Output('incident-over-months-chart', 'figure'),
    Input('incident-dropdown', 'value')
)
def update_incidents_over_months_chart(selected_incident):
    filtered_data = monthly_incidents[monthly_incidents['incident'] == selected_incident]
    
    fig = px.line(filtered_data, x='month', y='count',
                 title=f'Monthly Count of {selected_incident}')
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Number of Incidents')
    
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
