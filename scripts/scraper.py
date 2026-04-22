import json, os, re
from datetime import datetime
from playwright.sync_api import sync_playwright

# ALL BANKS RESTORED WITH CORRECTED URLS
TARGETS = {
    "Marcus": "https://www.marcus.com/us/en/savings/high-yield-savings",
    "Discover": "https://www.discover.com/online-banking/savings-account/",
    "Capital One": "https://www.capitalone.com/bank/savings-accounts/online-performance-savings-account/",
    "Amex": "https://www.americanexpress.com/en-us/banking/online-savings/high-yield-savings/",
    "Barclays": "https://www.banking.barclaysus.com/online-savings.html",
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
        page.goto(url, wait_until="networkidle", timeout=35000)
        page.wait_for_timeout(4000) 
        content = page.content()
        
        # Look for the highest rate (ignores fine print like 0.01% or 1.00% minimums)
        matches = re.findall(r'([1-5]\.\d{2})%', content)
        
        if matches:
            rates = [float(m) for m in matches]
            rate = max(rates)
            print(f"✓ {name}: {rate}%")
            return rate
        else:
            print(f"? {name}: No high-yield rate found.")
            return None
    except Exception as e:
        print(f"! {name}: Connection error.")
        return None

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base, 'data', 'rates.json')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})

        today = datetime.now().strftime("%Y-%m-%d")
        
        entry = {
            "date": today,
            "Chase": 0.01,
            "BofA": 0.01,
            "Wells Fargo": 0.01,
            "National Avg": 0.39 
        }

        print(f"--- Running Update for {today} ---")
        for name, url in TARGETS.items():
            entry[name] = get_live_rate(page, url, name)

        browser.close()

    if os.path.exists(data_path):
        with open(data_path, 'r') as f: history = json.load(f)
    else: history = []

    if history and history[-1]['date'] == today:
        history[-1] = entry
    else:
        history.append(entry)

    with open(data_path, 'w') as f:
        json.dump(history, f, indent=4)
    print(f"--- Update Complete. Processed {len(entry)-1} banks. ---")

if __name__ == "__main__":
    main()
