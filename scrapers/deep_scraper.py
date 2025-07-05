
import requests
from bs4 import BeautifulSoup
import re

def deep_scrape_listing_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")

        price_match = re.search(r"\$[\d,]+", text)
        bed_match = re.search(r"(\d+)\s*bed", text, re.IGNORECASE)
        bath_match = re.search(r"(\d+)\s*bath", text, re.IGNORECASE)
        year_match = re.search(r"(2025)", text)

        return {
            "price": price_match.group(0) if price_match else "",
            "bedrooms": bed_match.group(1) if bed_match else "",
            "bathrooms": bath_match.group(1) if bath_match else "",
            "year": year_match.group(1) if year_match else "",
            "source_text": text[:300]
        }

    except Exception as e:
        return {"error": str(e), "url": url}
