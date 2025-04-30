# =======================================
# FlipBurn Auto-Burn Backend (Fly.io Ready)
# =======================================

import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === CONFIG ===
API_KEY = "94680a64-c947-4b12-92d5-ddba014f6121"  # Fresh API key
TREASURY_PRIVATE_KEY = [103,94,78,173,218,133,32,224,165,177,5,147,42,165,192,75,92,186,143,158,210,56,224,53,147,135,208,117,173,201,191,103,241,122,210,42,111,163,193,59,245,94,5,85,78,64,31,215,76,214,60,35,104,54,127,214,161,136,13,24,198,55,153,133]
BURN_ADDRESS = "1nc1nerator11111111111111111111111111111111"
MINT_ADDRESS = "H6s6CWBxWuNhzpRb3bWCbZtxqzPZ3G9ZdfUFZPqcpump"
THRESHOLD = 1_000_000  # 1 million FLIP triggers 1 burn
CACHE_TTL = 60

batch_burn_queue = []

cache = {
    "burned_timestamp": 0,
    "burned_data": None,
    "bought_timestamp": 0,
    "bought_data": None,
}

# === HELPERS ===
def shorten_address(address: str) -> str:
    return f"{address[:4]}...{address[-4:]}" if len(address) >= 8 else address

def fetch_transactions():
    try:
        url = f"https://api.helius.xyz/v0/addresses/{MINT_ADDRESS}/transactions?api-key={API_KEY}&limit=100"
        resp = requests.get(url)
        return resp.json() if resp.ok else []
    except Exception as e:
        app.logger.error(f"Error fetching transactions: {str(e)}")
        return []

def calculate_total_bought(txns):
    total = 0
    for tx in txns:
        if tx.get("type") != "SWAP":
            continue
        for transfer in tx.get("tokenTransfers", []):
            if (
                transfer.get("mint") == MINT_ADDRESS and
                transfer.get("toUserAccount") and
                transfer.get("tokenAmount", 0) >= THRESHOLD
            ):
                total += int(transfer["tokenAmount"])
    return total

def calculate_total_burned(txns):
    burned = 0
    for tx in txns:
        if tx.get("type") != "BURN":
            continue
        for transfer in tx.get("tokenTransfers", []):
            if transfer.get("mint") == MINT_ADDRESS:
                burned += int(transfer.get("tokenAmount", 0))
    return burned

def send_burn_transaction(count):
    try:
        # 🔥 Here you would send a real transaction
        app.logger.info(f"Sending {count} FLIP to burn address {BURN_ADDRESS}")
        print(f"🔥 Burned {count} FLIP tokens to {BURN_ADDRESS}")
    except Exception as e:
        app.logger.error(f"Error sending burn: {str(e)}")

# === ROUTES ===
@app.route("/")
def home():
    return jsonify({"status": "🟢 Flip Burn Bot is LIVE"})

@app.route("/bought", methods=["GET"])
def total_bought():
    now = time.time()
    if cache["bought_data"] and now - cache["bought_timestamp"] < CACHE_TTL:
        return jsonify(cache["bought_data"])

    txns = fetch_transactions()
    total = calculate_total_bought(txns)
    data = {"total_bought": total}
    cache["bought_data"] = data
    cache["bought_timestamp"] = now
    return jsonify(data)

@app.route("/burn", methods=["GET"])
def total_burned():
    now = time.time()
    if cache["burned_data"] and now - cache["burned_timestamp"] < CACHE_TTL:
        return jsonify(cache["burned_data"])

    txns = fetch_transactions()
    total = calculate_total_burned(txns)
    data = {"total_burned": total}
    cache["burned_data"] = data
    cache["burned_timestamp"] = now
    return jsonify(data)

@app.route("/trigger", methods=["POST"])
def trigger_burn():
    try:
        body = request.json

        for event in body.get("events", []):
            if event.get("type") != "SWAP":
                continue
            for transfer in event.get("tokenTransfers", []):
                if (
                    transfer.get("mint") == MINT_ADDRESS and
                    transfer.get("toUserAccount") and
                    transfer.get("tokenAmount", 0) >= THRESHOLD
                ):
                    batch_burn_queue.append(1)
                    app.logger.info("Added 1 to batch burn queue.")

        if len(batch_burn_queue) >= 10:
            burn_count = sum(batch_burn_queue)
            send_burn_transaction(burn_count)
            batch_burn_queue.clear()

        return jsonify({"message": "Trigger received."})
    except Exception as e:
        app.logger.exception(f"Error in trigger_burn: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
