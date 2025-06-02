from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import tempfile
from werkzeug.middleware.proxy_fix import ProxyFix

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
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Create a temporary directory for the CSV file
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = os.path.join(temp_dir, 'portfolio_companies.csv')
            
            # Run the scraper script
            result = subprocess.run(
                ['python', 'vc_scraper.py', url], 
                capture_output=True, 
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            if result.returncode != 0:
                app.logger.error(f"Scraper error: {result.stderr}")
                return jsonify({'error': result.stderr}), 500

            # Read and return the CSV file
            if os.path.exists('portfolio_companies.csv'):
                with open('portfolio_companies.csv', 'r') as f:
                    csv_data = f.read()
                return csv_data, 200, {'Content-Type': 'text/csv'}
            else:
                return jsonify({'error': 'No data was scraped'}), 500

    except Exception as e:
        app.logger.error(f"Server error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 