
import os
import re
from serpapi import GoogleSearch

def scrape_comparables(address, type="sold"):
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        raise Exception("Missing SERPAPI_API_KEY")

    if type == "sold":
        query = f"{address} recent sold unit site:domain.com.au"
    else:
        query = f"{address} for sale unit site:realestate.com.au"

    params = {
        "engine": "google",
        "q": query,
        "location": "Australia",
        "google_domain": "google.com.au",
        "gl": "au",
        "hl": "en",
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    comps = []

    for r in results.get("organic_results", [])[:5]:
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        link = r.get("link", "")

        price_match = re.search(r"\$[\d,]+", snippet)
        bed_match = re.search(r"(\d+)\s*bed", snippet, re.IGNORECASE)
        bath_match = re.search(r"(\d+)\s*bath", snippet, re.IGNORECASE)
        year_match = re.search(r"(\d{4})", snippet)

        comps.append({
            "title": title,
            "link": link,
            "snippet": snippet,
            "price": price_match.group() if price_match else "",
            "bedrooms": bed_match.group(1) if bed_match else "",
            "bathrooms": bath_match.group(1) if bath_match else "",
            "year": year_match.group(1) if year_match else ""
        })

    return comps
