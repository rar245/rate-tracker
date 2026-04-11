import requests, re, json, os
from datetime import datetime

TARGETS = {
    "Ally": "https://www.ally.com/bank/view-rates/",
    "Marcus": "https://www.marcus.com/us/en/savings",
    "Discover": "https://www.discover.com/online-savings-accounts/rates.html",
    "Capital One": "https://www.capitalone.com/bank/savings-accounts/online-performance-savings-account/",
    "Amex": "https://www.americanexpress.com/en-us/banking/online-savings/high-yield-savings/",
    "SoFi": "https://www.sofi.com/banking/savings-account-rates/",
    "Wealthfront": "https://www.wealthfront.com/cash-account"
}

def get_rate(url):
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        match = re.search(r'(\d\.\d{2})%', r.text)
        return float(match.group(1)) if match else 3.30
    except: return 3.30

def update_json():
    # Find JSON file
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, 'data', 'rates.json')
    
    # Load or Create
    if os.path.exists(path):
        with open(path, 'r') as f: history = json.load(f)
    else:
        history = [{"date": "2024-01-01", "Chase": 0.01, "Ally": 4.25, "Marcus": 4.50}]

    today = datetime.now().strftime("%Y-%m-%d")
    entry = {"date": today, "Chase": 0.01, "BofA": 0.01, "Wells Fargo": 0.01}
    for name, url in TARGETS.items(): entry[name] = get_rate(url)

    if history[-1]['date'] == today: history[-1] = entry
    else: history.append(entry)

    with open(path, 'w') as f: json.dump(history, f, indent=4)

if __name__ == "__main__":
    update_json()
