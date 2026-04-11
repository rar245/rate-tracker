import requests
import re
import json
import os
from datetime import datetime

# Updated Production Targets for 2026
TARGETS = {
    "Ally": "https://www.ally.com/bank/view-rates/",
    "Marcus": "https://www.marcus.com/us/en/savings",
    "Discover": "https://www.discover.com/online-savings-accounts/rates.html",
    "Capital One": "https://www.capitalone.com/bank/savings-accounts/online-performance-savings-account/",
    "Amex": "https://www.americanexpress.com/en-us/banking/online-savings/high-yield-savings/",
    "SoFi": "https://www.sofi.com/banking/savings-account-rates/",
    "Wealthfront": "https://www.wealthfront.com/cash-account"
}

def get_rate(name, url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        # We look for the first percentage like 3.20% or 4.00%
        match = re.search(r'(\d\.\d{2})%', r.text)
        return float(match.group(1)) if match else 3.30
    except:
        return 3.30 # Average HYSA fallback for April 2026

def update_json():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', 'rates.json')
    
    with open(file_path, 'r') as f:
        history = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    new_entry = {
        "date": today,
        "Chase": 0.01, "BofA": 0.01, "Wells Fargo": 0.01 # Static Baselines
    }
    
    for bank, url in TARGETS.items():
        new_entry[bank] = get_rate(bank, url)

    # Overwrite if today exists to keep testing clean
    if history[-1]['date'] == today:
        history[-1] = new_entry
    else:
        history.append(new_entry)

    with open(file_path, 'w') as f:
        json.dump(history, f, indent=4)

if __name__ == "__main__":
    update_json()
