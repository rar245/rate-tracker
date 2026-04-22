import json, os, re
from datetime import datetime
from playwright.sync_api import sync_playwright

# The "Rate Beat" April 2026 Targeted List
TARGETS = {
    "Marcus": "https://www.marcus.com/us/en/savings/high-yield-savings",
    "Discover": "https://www.discover.com/online-savings-accounts/",
    "Capital One": "https://www.capitalone.com/bank/savings-accounts/online-performance-savings-account/",
    "Amex": "https://www.americanexpress.com/en-us/banking/online-savings/high-yield-savings/",
    "Ally": "https://www.ally.com/bank/view-rates/",
    "SoFi": "https://www.sofi.com/banking/savings-account-interest-rates-apy/",
    "Wealthfront": "https://www.wealthfront.com/cash-account",
    "Axos Bank": "https://www.axosbank.com/personal/bank/axos-one",
    "LendingClub": "https://www.lendingclub.com/personal-banking/high-yield-savings",
    "CIT Bank": "https://www.cit.com/cit-bank/bank/savings/platinum-savings-account",
    "EverBank": "https://www.everbank.com/personal/savings/performance-savings",
    "Newtek": "https://newtekbank.com/personal-banking/personal-high-yield-savings/",
    "BrioDirect": "https://www.briodirectbanking.com/high-yield-savings-account/",
    "Bread Savings": "https://www.breadfinancial.com/en/bread-savings/high-yield-savings-account.html"
}

def get_live_rate(page, url, name):
    try:
        # Increase timeout slightly to ensure page loads completely
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000) 
        content = page.content()
        
        # Looking for numbers like 3.50, 4.21, etc. followed by %
        match = re.search(r'([0-5]\.\d{2})%', content)
        
        if match:
            rate = float(match.group(1))
            print(f"✓ {name}: {rate}%")
            return rate
        else:
            print(f"? {name}: Rate not found on page. Recording as null.")
            return None # NO FALLBACK
    except Exception as e:
        print(f"! {name}: Connection error. Recording as null.")
        return None # NO FALLBACK

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base, 'data', 'rates.json')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})

        today = datetime.now().strftime("%Y-%m-%d")
        
        # Fixed Anchors (These rarely change, so we keep them as baseline)
        entry = {
            "date": today,
            "Chase": 0.01,
            "BofA": 0.01,
            "Wells Fargo": 0.01,
            "National Avg": 0.39 
        }

        print(f"--- Running Strict Update for {today} ---")
        for name, url in TARGETS.items():
            entry[name] = get_live_rate(page, url, name)

        browser.close()

    if os.path.exists(data_path):
        with open(data_path, 'r') as f: history = json.load(f)
    else: history = []

    # Update or Append
    if history and history[-1]['date'] == today:
        history[-1] = entry
    else:
        history.append(entry)

    with open(data_path, 'w') as f:
        json.dump(history, f, indent=4)
    print(f"--- Update Complete. Processed {len(entry)-1} banks. ---")

if __name__ == "__main__":
    main()
