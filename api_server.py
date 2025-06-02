from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import tempfile
from werkzeug.middleware.proxy_fix import ProxyFix
import logging

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

        # Create a temporary directory for the CSV file
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = os.path.join(temp_dir, 'portfolio_companies.csv')
            
            # Log the current working directory and script location
            cwd = os.path.dirname(os.path.abspath(__file__))
            logger.info(f"Current working directory: {cwd}")
            logger.info(f"Running scraper script for URL: {url}")
            
            # Run the scraper script
            result = subprocess.run(
                ['python', 'vc_scraper.py', url], 
                capture_output=True, 
                text=True,
                cwd=cwd
            )
            
            logger.info(f"Scraper stdout: {result.stdout}")
            if result.stderr:
                logger.error(f"Scraper stderr: {result.stderr}")
            
            if result.returncode != 0:
                error_msg = f"Scraper failed with return code {result.returncode}: {result.stderr}"
                logger.error(error_msg)
                return jsonify({'error': error_msg}), 500

            # Check if CSV file exists and read it
            csv_file_path = os.path.join(cwd, 'portfolio_companies.csv')
            logger.info(f"Looking for CSV file at: {csv_file_path}")
            
            if os.path.exists(csv_file_path):
                with open(csv_file_path, 'r') as f:
                    csv_data = f.read()
                logger.info("Successfully read CSV file")
                return csv_data, 200, {'Content-Type': 'text/csv'}
            else:
                error_msg = f"CSV file not found at {csv_file_path}"
                logger.error(error_msg)
                return jsonify({'error': error_msg}), 500

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 