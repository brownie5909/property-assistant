from flask import Flask, request, jsonify
import os
from drive_upload.upload_to_drive import upload_file_to_drive

app = Flask(__name__)

@app.route("/upload-test", methods=["GET", "POST"])
def upload_test():
    # Create a sample file to upload
    sample_filename = "sample_report.txt"
    with open(sample_filename, "w") as f:
        f.write("This is a test file uploaded to Google Drive.")

    try:
        file_link = upload_file_to_drive(sample_filename)
        return jsonify({"message": "Upload successful", "link": file_link})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
