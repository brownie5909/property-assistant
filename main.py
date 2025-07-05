from flask import Flask, request, jsonify
import os
import re
from drive_upload.upload_to_drive import upload_file_to_drive
from assistant.openai_handler import generate_property_insights
from assistant.structured_comparables import generate_structured_comparables
from pdf.generate_report import create_pdf_report
from scrapers.serp_scraper import scrape_property_info
from scrapers.suburb_scraper import scrape_suburb_insights
from scrapers.comps_scraper import scrape_comparables
from scrapers.deep_scraper import deep_scrape_listing_page

app = Flask(__name__)

@app.route("/upload-test", methods=["GET", "POST"])
def upload_test():
    sample_filename = "sample_report.txt"
    with open(sample_filename, "w") as f:
        f.write("This is a test file uploaded to Google Drive.")
    try:
        file_link = upload_file_to_drive(sample_filename)
        return jsonify({"message": "Upload successful", "link": file_link})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate-report", methods=["POST"])
def generate_report():
    try:
        data = request.get_json()
        address = data.get("address")
        if not address:
            return jsonify({"error": "Missing property address"}), 400

        listing_data = scrape_property_info(address)

        suburb_match = re.search(r",\s*(.*?)\s+QLD", address)
        suburb = suburb_match.group(1).strip() if suburb_match else ""
        suburb_data = scrape_suburb_insights(suburb) if suburb else []

        sold_comps_raw = scrape_comparables(address, type="sold")
        for_sale_comps_raw = scrape_comparables(address, type="forsale")

        # Deep scrape to improve data quality
        sold_comps = []
        for_sale_comps = []
        for item in sold_comps_raw:
            detail = deep_scrape_listing_page(item.get("link"))
            if detail and detail.get("year") == "2025":
                sold_comps.append({**item, **detail})
        for item in for_sale_comps_raw:
            detail = deep_scrape_listing_page(item.get("link"))
            if detail and detail.get("year") == "2025":
                for_sale_comps.append({**item, **detail})

        structured_comps = generate_structured_comparables(address, sold_comps, for_sale_comps)
        insights = generate_property_insights(address, listing_data, suburb_data, sold_comps, for_sale_comps)

        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', address)
        pdf_filename = f"property_report_{safe_name}.pdf"

        image_url = None
        for entry in listing_data:
            if 'link' in entry and 'realestate.com.au' in entry['link']:
                image_url = f"https://img.realestate.com.au/property-assets/{safe_name.lower()}.jpg"
                break

        create_pdf_report(address, insights, pdf_filename, image_url=image_url)

        drive_link = upload_file_to_drive(pdf_filename)
        return jsonify({"summary": insights[:250] + "...", "pdf_link": drive_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/scrape-property", methods=["POST"])
def scrape_property():
    try:
        data = request.get_json()
        address = data.get("address")
        if not address:
            return jsonify({"error": "Missing property address"}), 400

        results = scrape_property_info(address)
        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
