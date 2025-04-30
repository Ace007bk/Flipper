from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

shill_messages = [
    "$FLIP is flipping the game! Auto burns every milestone. #WeFlip2 #Solana #Crypto 🚀",
    "Bitcoin doesn’t burn. $FLIP does. Welcome to deflationary domination. #WeFlip #BurnToken 💰",
    "They print. We burn. $FLIP is built for the future. #Solana #MemeCoin #FLIPtheMarket 🔥",
    "$FLIP is turning up the heat! Buy & burn nonstop. #WeFlip2 💰🔥",
    "Diamond hands flip the market. $FLIP is pure scarcity. #Solana #FLIP 🔥🚀",
]

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=options)
driver.get('https://twitter.com/login')
time.sleep(10)

input("🔑 Login in the opened browser. Hit Enter here when you're fully logged in...")

while True:
    try:
        tweet_text = random.choice(shill_messages)

        driver.get('https://twitter.com/compose/tweet')
        time.sleep(8)

        # Find tweet input box reliably
        boxes = driver.find_elements(By.XPATH, "//div[@role='textbox']")
        for box in boxes:
            try:
                box.send_keys(tweet_text)
                break
            except:
                continue

        time.sleep(2)

        # Find tweet button
        buttons = driver.find_elements(By.XPATH, "//div[@data-testid='tweetButtonInline']")
        for button in buttons:
            try:
                button.click()
                print(f"✅ Posted: {tweet_text}")
                break
            except:
                continue

    except Exception as e:
        print(f"❌ Error: {e}")

    print("⏳ Sleeping 15 minutes...")
    time.sleep(15 * 60)
