import requests
import json
from datetime import datetime

def update_rates():
    # 2026 Live Scrape (Simplified for POC)
    # In a real run, this would use BeautifulSoup to grab the latest Ally rate
    current_ally = 3.20 
    current_marcus = 3.24
    
    new_entry = {
        "date": datetime.now().strftime("%Y-%m"),
        "Chase": 0.01,
        "Ally": current_ally,
        "Marcus": current_marcus
    }

    with open('data/rates.json', 'r+') as f:
        data = json.load(f)
        if data[-1]["date"] != new_entry["date"]:
            data.append(new_entry)
            f.seek(0)
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    update_rates()
