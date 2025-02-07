from flask import Flask
from fire_dashboard.fire_app2 import create_dash_app1
from dashboardsalescall import create_dash_app2  # Assuming another Dash app exists

# Initialize Flask app
flask_app = Flask(__name__)

# Attach Dash apps to Flask
app1 = create_dash_app1(flask_app)
app2 = create_dash_app2(flask_app)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000)
