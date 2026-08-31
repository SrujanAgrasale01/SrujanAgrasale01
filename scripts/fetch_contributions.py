import json
import os
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

username = os.environ.get("GITHUB_USERNAME", "SrujanAgrasale01")
url = f"https://github.com/users/{username}/contributions"
html = requests.get(url, timeout=30, headers={"User-Agent": "github-profile-readme-generator"}).text
soup = BeautifulSoup(html, "html.parser")

items = []
for rect in soup.select("rect.ContributionCalendar-day"):
    date = rect.get("data-date")
    level = rect.get("data-level")
    if date:
        items.append({"date": date, "level": int(level or 0)})

if not items:
    # Fallback parser for markup variations.
    for cell in soup.select("[data-date][data-level]"):
        date = cell.get("data-date")
        level = cell.get("data-level")
        if date:
            items.append({"date": date, "level": int(level or 0)})

Path("data").mkdir(exist_ok=True)
Path("data/contributions.json").write_text(
    json.dumps({"username": username, "updated_at": datetime.utcnow().isoformat(), "days": items}, indent=2),
    encoding="utf-8",
)
print(f"Fetched {len(items)} contribution days for {username}")
