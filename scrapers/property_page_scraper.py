
import os
import requests
from bs4 import BeautifulSoup

def scrape_property_page(address):
    query = address.replace(' ', '+') + '+site:realestate.com.au'
    search_url = f"https://www.google.com/search?q={query}"

    print("🟡 Search URL:", search_url)

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
                    print("✅ Found listing link:", link)
                    break

        if not link:
            print("❌ No listing link found in search results.")
            return {"error": "No listing link found."}

        page_resp = requests.get(link, headers=headers, timeout=10)
        if page_resp.status_code != 200:
            print("❌ Listing page request failed:", page_resp.status_code)
            return {"error": "Listing page did not return 200."}

        soup = BeautifulSoup(page_resp.text, "html.parser")
        text = soup.get_text(separator="\n")

        if len(text.strip()) < 1000:
            print("❌ Page content too short.")
            return {"error": "Page content was too short."}

        data = {
            "source_url": link,
            "summary_text": text[:4000],
            "image_url": None
        }

        img = soup.find("img")
        if img and img.get("src", "").startswith("http"):
            data["image_url"] = img["src"]

        print("✅ Scraping complete. Text length:", len(data["summary_text"]))
        return data

    except Exception as e:
        print("❌ Exception during scraping:", str(e))
        return {"error": str(e)}
