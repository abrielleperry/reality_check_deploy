from flask import Flask
import dash
from dash import html

# Create a Flask server instance
server = Flask(__name__)

# Define a route for a simple Flask page


@server.route('/hello')
def hello():
    return 'Hello from Flask!'


# Create a Dash application, using the Flask server as backend
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1('Hello from Dash!'),
    html.P('This is a Dash app running on a Flask server.')
])

if __name__ == '__main__':
    # Run the server
    server.run(debug=True)
