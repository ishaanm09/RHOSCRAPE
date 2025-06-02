from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import csv
from io import StringIO
from vc_scraper import extract_companies

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
CORS(app, resources={r"/scrape": {"origins": os.getenv("ALLOWED_ORIGINS", "*")}})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data.get('url')
        
        logger.info(f"Received scrape request for URL: {url}")
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Directly call the scraping function
        companies = extract_companies(url)
        
        if not companies:
            logger.error("No companies were found")
            return jsonify({'error': 'No data was scraped'}), 500

        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Company", "URL"])  # Header
        writer.writerows(companies)
        
        # Get the CSV data and reset the pointer
        csv_data = output.getvalue()
        output.close()
        
        logger.info(f"Successfully scraped {len(companies)} companies")
        return csv_data, 200, {'Content-Type': 'text/csv'}

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 