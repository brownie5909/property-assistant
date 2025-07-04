import os
from serpapi.google_search import GoogleSearch

def scrape_property_info(address):
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        raise Exception("Missing SERPAPI_API_KEY")

    query = f"{address} site:realestate.com.au"

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

    top_results = results.get("organic_results", [])[:3]
    simplified = []

    for result in top_results:
        simplified.append({
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet")
        })

    return simplified
