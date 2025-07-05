
import requests
from bs4 import BeautifulSoup

def scrape_google_for_listings(address):
    query = address.replace(" ", "+") + "+site:realestate.com.au+OR+site:domain.com.au"
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(search_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print("❌ Google search failed")
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "realestate.com.au" in href or "domain.com.au" in href:
                if "http" in href and "/url?q=" in href:
                    clean_link = href.split("/url?q=")[-1].split("&")[0]
                    if clean_link not in links:
                        links.append(clean_link)
        return links[:2]

    except Exception as e:
        print("❌ Exception in Google scrape:", e)
        return None

def fetch_and_summarize_pages(urls):
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
                summaries.append({ "url": url, "text": text[:4000] })
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

def search_and_scrape_pages(address):
    links = scrape_google_for_listings(address)
    if not links:
        return None
    return fetch_and_summarize_pages(links)
