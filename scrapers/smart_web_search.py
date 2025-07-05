
import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

def ask_gpt_for_listing_urls(address):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"""You're an Australian real estate search assistant.

Your task is to suggest the top 2-3 live property listing URLs for this address:
"{address}"

Only return URLs, one per line. Prioritize:
- realestate.com.au
- domain.com.au
- property.com.au
- Ray White, LJ Hooker, or agency sites

Do not explain. Just list URLs.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a real estate link researcher."},
            {"role": "user", "content": prompt}
        ]
    )
    urls = response.choices[0].message.content.strip().splitlines()
    return [url.strip() for url in urls if url.startswith("http")]

def fetch_and_clean_page(url):
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return {
            "url": url,
            "text": text[:4000]
        }
    except:
        return None

def smart_search_and_scrape(address):
    urls = ask_gpt_for_listing_urls(address)
    summaries = []
    for url in urls:
        page = fetch_and_clean_page(url)
        if page:
            summaries.append(page)
        if len(summaries) >= 2:
            break
    if not summaries:
        return None
    merged_text = "\n\n---\n\n".join(f"Source: {s['url']}\n{s['text']}" for s in summaries)
    return {
        "summary_text": merged_text,
        "image_url": None,
        "source_urls": [s['url'] for s in summaries]
    }
