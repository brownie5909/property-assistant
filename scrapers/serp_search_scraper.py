
import os
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def search_and_scrape_pages(address):
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    if not serpapi_key:
        raise Exception("Missing SERPAPI_API_KEY environment variable")

    search = GoogleSearch({
        "q": f"{address} site:realestate.com.au OR site:domain.com.au",
        "location": "Australia",
        "hl": "en",
        "gl": "au",
        "engine": "google",
        "api_key": serpapi_key
    })

    results = search.get_dict()
    urls = [r.get("link") for r in results.get("organic_results", []) if "realestate.com.au" in r.get("link", "") or "domain.com.au" in r.get("link", "")]

    summaries = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(separator="\n")
            if len(text.strip()) > 1000:
                summaries.append({"url": url, "text": text[:4000]})
        except:
            continue
        if len(summaries) >= 2:
            break

    if not summaries:
        return None

    merged = "\n\n---\n\n".join(f"Source: {s['url']}\n{s['text']}" for s in summaries)
    return {
        "summary_text": merged,
        "image_url": None,
        "source_urls": [s["url"] for s in summaries]
    }
