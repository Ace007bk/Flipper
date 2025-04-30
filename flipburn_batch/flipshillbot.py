
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

# ==== Your Shill Messages ====
shill_messages = [
    "$FLIP is flipping the game! Auto burns every milestone. #WeFlip2 #Solana #Crypto 🚀",
    "Bitcoin doesn’t burn. $FLIP does. Welcome to deflationary domination. #WeFlip #BurnToken 💰",
    "They print. We burn. $FLIP is built for the future. #Solana #MemeCoin #FLIPtheMarket 🔥",
    "Asian whales know—burn is king. $FLIP makes scarcity sexy. #WeFlip2 #CryptoChina 🐋",
    "Smart whales accumulate $FLIP before the next burn wave. #Solana #FlipArmy #WeFlip2 🧠",
]

# ==== Launch Browser ====
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=options)

# ==== Go to Twitter Login Page ====
driver.get('https://twitter.com/login')
time.sleep(8)  # Wait for login page to fully load

# ==== IMPORTANT: You manually login here once ====
input("🔑 Log into your Twitter account in the opened browser. Press Enter here after you're logged in...")

# ==== Main Posting Loop ====
while True:
    try:
        tweet_text = random.choice(shill_messages)
        
        driver.get('https://twitter.com/compose/tweet')
        time.sleep(5)

        tweet_box = driver.find_element(By.XPATH, "//div[@data-testid='tweetTextarea_0']")
        tweet_box.send_keys(tweet_text)
        time.sleep(2)

        tweet_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
        tweet_button.click()

        print(f"✅ Posted: {tweet_text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

    print("⏳ Sleeping 15 minutes before next post...")
    time.sleep(15 * 60)
