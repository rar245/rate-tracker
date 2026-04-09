import requests
from bs4 import BeautifulSoup
import json
import re
import os
from datetime import datetime

def get_rates():
    # April 2026 Live Market Rates
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Simple Fallbacks if scrape fails
    ally = 3.20
    marcus = 3.65
    
    try:
        r = requests.get("https://www.ally.com/bank/view-rates/", headers=headers, timeout=10)
        ally = float(re.search(r'(\d+\.\d+)%', r.text).group(1))
    except: pass
        
    try:
        r = requests.get("https://www.marcus.com/us/en/savings", headers=headers, timeout=10)
        marcus = float(re.search(r'(\d+\.\d+)%', r.text).group(1))
    except: pass
        
    return ally, marcus

def update_json():
    # --- DYNAMIC PATH FINDING ---
    # This searches the whole folder structure for rates.json
    target_file = None
    for root, dirs, files in os.walk("."):
        if "rates.json" in files:
            target_file = os.path.join(root, "rates.json")
            break
    
    if not target_file:
        print("CRITICAL ERROR: Could not find rates.json in any folder!")
        return

    with open(target_file, 'r') as f:
        history = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    
    # If today already exists, we modify it instead of skipping 
    # (This helps during testing/debugging)
    ally, marcus = get_rates()
    new_entry = {"date": today, "Chase": 0.01, "Ally": ally, "Marcus": marcus}
    
    if history[-1]['date'] == today:
        history[-1] = new_entry # Update existing
    else:
        history.append(new_entry) # Add new

    with open(target_file, 'w') as f:
        json.dump(history, f, indent=4)
    print(f"Successfully saved to {target_file}")

if __name__ == "__main__":
    update_json()
