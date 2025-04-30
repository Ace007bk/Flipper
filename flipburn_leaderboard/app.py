from flask import Flask, render_template, jsonify

app = Flask(__name__)

leaderboard_data = [
    {"wallet": "4eTWY...3q2N", "burned": 125.5, "last_burn": "2025-04-23 16:05"},
    {"wallet": "sCdjV...oAkm", "burned": 93.7, "last_burn": "2025-04-23 15:58"},
    {"wallet": "86MyF...AM69", "burned": 88.1, "last_burn": "2025-04-23 15:51"}
]

@app.route("/")
def home():
    return "Flip Auto Burn Engine is Live"

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html", leaderboard=leaderboard_data)

@app.route("/api/leaderboard")
def api_leaderboard():
    return jsonify(leaderboard_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
