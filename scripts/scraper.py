import requests
from bs4 import BeautifulSoup
import json
import re
import os
from datetime import datetime

def get_ally_rate():
    try:
        # User-Agent makes the request look like a standard browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        r = requests.get("https://www.ally.com/bank/view-rates/", headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Looks for a pattern like 3.20% or 4.25%
        rate_text = soup.find(string=re.compile(r'\d+\.\d+%'))
        return float(rate_text.replace('%', ''))
    except Exception as e:
        print(f"Ally Scrape Error: {e}")
        return 3.20 # Fallback for April 2026

def get_marcus_rate():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        r = requests.get("https://www.marcus.com/us/en/savings/high-yield-savings", headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Marcus often puts their rate in a specific span or data attribute
        rate_text = soup.find(string=re.compile(r'\d+\.\d+%\s*APY', re.IGNORECASE))
        # Extract just the number
        match = re.search(r'(\d+\.\d+)', rate_text)
        return float(match.group(1))
    except Exception as e:
        print(f"Marcus Scrape Error: {e}")
        return 3.24 # Fallback for April 2026

def update_json():
    # This ensures the script finds the file even when running from /scripts/ folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, '..', 'data', 'rates.json')
    
    with open(file_path, 'r') as f:
        history = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if we already have an entry for today
    if history[-1]['date'] == today:
        print(f"Rates for {today} already exist. Skipping update.")
        return

    new_rates = {
        "date": today,
        "Chase": 0.01, # The Big Bank Baseline
        "Ally": get_ally_rate(),
        "Marcus": get_marcus_rate()
    }
    
    history
