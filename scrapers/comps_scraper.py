
import os
from serpapi import GoogleSearch

def scrape_comparables(address, type="sold"):
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        raise Exception("Missing SERPAPI_API_KEY")

    if type == "sold":
        query = f"{address} recent sold property site:domain.com.au"
    else:
        query = f"{address} for sale site:realestate.com.au"

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

    top_results = results.get("organic_results", [])[:5]
    comps = []

    for r in top_results:
        comps.append({
            "title": r.get("title", ""),
            "link": r.get("link", ""),
            "snippet": r.get("snippet", "")
        })

    return comps
