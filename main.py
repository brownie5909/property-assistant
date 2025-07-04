from flask import Flask, request, jsonify
import os
import re
from drive_upload.upload_to_drive import upload_file_to_drive
from assistant.openai_handler import generate_property_insights
from pdf.generate_report import create_pdf_report
from scrapers.serp_scraper import scrape_property_info
from scrapers.suburb_scraper import scrape_suburb_insights

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

        # extract suburb from address
        suburb_match = re.search(r",\s*(.*?)\s+QLD", address)
        suburb = suburb_match.group(1).strip() if suburb_match else ""
        suburb_data = scrape_suburb_insights(suburb) if suburb else []

        insights = generate_property_insights(address, listing_data, suburb_data)

        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', address)
        pdf_filename = f"property_report_{safe_name}.pdf"
        create_pdf_report(address, insights, pdf_filename)

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
