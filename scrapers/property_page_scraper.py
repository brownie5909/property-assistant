
import os
import requests
from bs4 import BeautifulSoup

def scrape_property_page(address):
    query = address.replace(' ', '+') + '+site:realestate.com.au'
    search_url = f"https://www.google.com/search?q={query}"

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        link = None
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "realestate.com.au" in href:
                match = href.split("q=")[-1].split("&")[0]
                if match.startswith("http"):
                    link = match
                    break

        if not link:
            return None

        page_resp = requests.get(link, headers=headers, timeout=10)
        if page_resp.status_code != 200:
            return None

        soup = BeautifulSoup(page_resp.text, "html.parser")
        text = soup.get_text(separator="\n")

        data = {
            "source_url": link,
            "summary_text": text[:4000],
            "image_url": None
        }

        img = soup.find("img")
        if img and img.get("src", "").startswith("http"):
            data["image_url"] = img["src"]

        return data

    except Exception as e:
        return {"error": str(e)}
