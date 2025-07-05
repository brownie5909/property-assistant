
import requests
from bs4 import BeautifulSoup

def scrape_bing_for_listings(address):
    query = address.replace(" ", "+") + "+site:realestate.com.au+OR+site:domain.com.au"
    search_url = f"https://www.bing.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    print("🔍 Searching Bing:", search_url)

    try:
        resp = requests.get(search_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print("❌ Bing search failed with status:", resp.status_code)
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "realestate.com.au" in href or "domain.com.au" in href:
                if href.startswith("http") and href not in links:
                    links.append(href)
        if not links:
            print("⚠️ No relevant Bing links found.")
        return links[:2]

    except Exception as e:
        print("❌ Exception in Bing scrape:", e)
        return None

def fetch_and_summarize_pages(urls):
    summaries = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in urls:
        try:
            print("📄 Fetching page:", url)
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                print("⚠️ Skipped page (status code):", resp.status_code)
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(separator="\n")
            print("🧾 Text length:", len(text.strip()))
            if len(text.strip()) > 1000:
                summaries.append({ "url": url, "text": text[:4000] })
        except Exception as e:
            print("❌ Error fetching page:", e)
            continue
        if len(summaries) >= 2:
            break

    if not summaries:
        print("⚠️ No valid listing content found.")
        return None

    merged = "\n\n---\n\n".join(f"Source: {s['url']}\n{s['text']}" for s in summaries)
    return {
        "summary_text": merged,
        "image_url": None,
        "source_urls": [s["url"] for s in summaries]
    }

def search_and_scrape_pages(address):
    links = scrape_bing_for_listings(address)
    if not links:
        print("❌ No Bing links to scrape.")
        return None
    return fetch_and_summarize_pages(links)
