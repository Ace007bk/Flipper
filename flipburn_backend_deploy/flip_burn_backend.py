from fastapi import FastAPI, Request
import httpx

app = FastAPI()

HELIUS_API_KEY = "4828b59b-50cd-43bb-8571-6add477186c1"
MINT_ADDRESS = "H6s6CWBxWuNhzpRb3bWCbZtxqzPZ3G9ZdfUFZPqcpump"
BURN_ADDRESS = "1nc1nerator11111111111111111111111111111111"
BURN_RATIO = 1 / 1_000_000
total_bought = 175000000
total_burned = total_bought * BURN_RATIO

@app.get("/")
def home():
    return {
        "status": "🟢 Flip Auto Burn Bot is LIVE",
        "burn_address": BURN_ADDRESS,
        "burn_ratio": "1 per 1,000,000 FLIP",
        "network": "Solana Mainnet"
    }

@app.get("/status")
def status():
    return {
        "total_bought": total_bought,
        "total_burned": round(total_burned, 2),
        "burn_address": BURN_ADDRESS,
        "burn_ratio": "1 per 1,000,000 FLIP"
    }

@app.post("/burn/{amount}")
def burn(amount: int):
    burned = amount * BURN_RATIO
    global total_bought, total_burned
    total_bought += amount
    total_burned += burned
    return {
        "burned": round(burned, 2),
        "new_total_bought": total_bought,
        "new_total_burned": round(total_burned, 2),
        "message": f"🔥 Burned {round(burned, 2)} FLIP!"
    }

@app.post("/webhook")
async def helius_webhook(request: Request):
    data = await request.json()
    bought = 0

    for txn in data.get("transactions", []):
        for event in txn.get("events", {}).get("splToken", []):
            if event.get("mint") == MINT_ADDRESS and event.get("tokenAmount", {}).get("amount", 0) > 0:
                bought += int(event["tokenAmount"]["amount"])

    if bought > 0:
        async with httpx.AsyncClient() as client:
            await client.post(f"https://flipburn.fly.dev/burn/{bought}")

    return {"processed_bought": bought}

