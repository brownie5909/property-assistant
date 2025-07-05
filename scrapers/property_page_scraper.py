import os
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch   # ✅ Correct for version 0.1.5

def scrape_property_page(address):
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        raise Exception("Missing SERPAPI_API_KEY")

    search = GoogleSearch({
        "q": f"{address} site:realestate.com.au OR site:domain.com.au",
        "location": "Australia",
        "hl": "en",
        "gl": "au",
        "engine": "google",
        "api_key": api_key
    })

    results = search.get_dict()
    url = None
    for r in results.get("organic_results", []):
        link = r.get("link", "")
        if "realestate.com.au" in link or "domain.com.au" in link:
            url = link
            break

    if not url:
        return None

    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")

        data = {
            "source_url": url,
            "summary_text": text[:4000],
            "image_url": None
        }

        # Attempt to get image from known REA patterns
        img = soup.find("img")
        if img and img.get("src", "").startswith("http"):
            data["image_url"] = img["src"]

        return data

    except Exception as e:
        return {"error": str(e)}
