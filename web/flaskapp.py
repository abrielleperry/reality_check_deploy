from flask import Flask
import dash
from dash import html, dcc 
from dashboardsalescall import create_dash_app2 as create_dash_app2
from fire_dashboard.fire_app2 import create_dash_app1 as create_dash_app1


# Initialize Flask app
flask_app = Flask(__name__)

# Define a route for a simple Flask page
app1 = create_dash_app1(flask_app)
app2 = create_dash_app2(flask_app)
# Run the Flask server
if __name__ == '__main__':
    flask_app.run(debug=True)
