from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def dashboard():
    try:
        leaderboard_data = requests.get('https://flipburn-backend-deploy.fly.dev/api/leaderboard').json()
    except Exception as e:
        leaderboard_data = [{"wallet": "ERROR", "amount": "N/A", "timestamp": str(e)}]

    try:
        total_bought = requests.get('https://flipburn-backend-deploy.fly.dev/api/total-bought').json().get("total", "N/A")
    except:
        total_bought = "N/A"

    try:
        total_burned = requests.get('https://flipburn-backend-deploy.fly.dev/api/total-burned').json().get("total", "N/A")
    except:
        total_burned = "N/A"

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>$FLIP Burn Dashboard</title>
        <style>
            body { background-color: black; color: #00ff00; font-family: monospace; padding: 30px; }
            .entry { margin-bottom: 15px; border-bottom: 1px solid #00ff00; padding-bottom: 5px; }
            h1, h2 { color: #00ffff; }
            .stat { font-size: 20px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>🔥 $FLIP Auto-Burn Dashboard</h1>

        <div class="stat">💰 <strong>Total FLIP Bought:</strong> {{ total_bought }}</div>
        <div class="stat">🔥 <strong>Total FLIP Burned:</strong> {{ total_burned }}</div>

        <h2>📜 Recent Burn Events</h2>
        {% for entry in leaderboard %}
        <div class="entry">
            <strong>{{ entry.wallet }}</strong> burned <strong>{{ entry.amount }}</strong> FLIP<br>
            <small>{{ entry.timestamp }}</small>
        </div>
        {% endfor %}
    </body>
    </html>
    """

    return render_template_string(html_template,
                                  leaderboard=leaderboard_data,
                                  total_bought=total_bought,
                                  total_burned=total_burned)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
