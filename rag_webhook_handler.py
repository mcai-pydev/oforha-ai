import requests
import json
from typing import Dict, Any
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import sys
from urllib.parse import urljoin

# Load environment variables
load_dotenv()

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class RAGWebhookHandler:
    def __init__(self, n8n_webhook_url: str):
        # Ensure the URL is properly formatted
        self.n8n_webhook_url = n8n_webhook_url.strip()
        logger.info(f"Initialized RAGWebhookHandler with n8n URL: {self.n8n_webhook_url}")
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process the incoming query using RAG
        """
        try:
            # TODO: Implement your RAG logic here
            # This is where you would:
            # 1. Retrieve relevant documents
            # 2. Generate response using your LLM
            # 3. Return the results
            
            response = {
                "status": "success",
                "query": query,
                "response": "Sample RAG response"
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def send_to_n8n(self, data: Dict[str, Any]) -> bool:
        """
        Send processed results back to n8n webhook
        """
        try:
            logger.info(f"Attempting to send data to n8n: {self.n8n_webhook_url}")
            logger.debug(f"Data being sent: {json.dumps(data, indent=2)}")
            
            # Ensure the URL is properly formatted
            webhook_url = self.n8n_webhook_url.strip()
            
            response = requests.post(
                webhook_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10  # Add timeout
            )
            
            # Log the response status and content
            logger.info(f"n8n response status: {response.status_code}")
            logger.debug(f"n8n response content: {response.text}")
            
            response.raise_for_status()
            return True
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error to n8n: {str(e)}")
            logger.error("Please ensure n8n is running and the webhook URL is correct")
            return False
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout while connecting to n8n: {str(e)}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending data to n8n: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response content: {e.response.text}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while sending data to n8n: {str(e)}")
            return False

# Initialize the handler
n8n_url = os.getenv('N8N_WEBHOOK_URL', '').strip()
if not n8n_url:
    logger.error("N8N_WEBHOOK_URL environment variable is not set!")
    sys.exit(1)

handler = RAGWebhookHandler(n8n_url)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return jsonify({
            "status": "success",
            "message": "Webhook is active and ready to receive POST requests",
            "n8n_url": n8n_url
        }), 200
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({
                    "status": "error",
                    "message": "No query provided in request body"
                }), 400
            
            query = data['query']
            logger.info(f"Received query: {query}")
            
            result = handler.process_query(query)
            
            if handler.send_to_n8n(result):
                return jsonify(result), 200
            else:
                return jsonify({
                    "status": "error",
                    "message": "Failed to process request - check logs for details"
                }), 500
                
        except Exception as e:
            logger.error(f"Error processing webhook request: {str(e)}")
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

def test_n8n_connection():
    """
    Test function to directly send a request to n8n webhook
    """
    test_data = {
        "query": "Test connection to n8n",
        "timestamp": "2024-01-20T12:00:00Z"
    }
    
    try:
        # Ensure the URL is properly formatted
        webhook_url = n8n_url.strip()
        logger.info(f"Testing connection to: {webhook_url}")
        
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting webhook server on port {port}")
    logger.info(f"n8n webhook URL: {n8n_url}")
    app.run(host='0.0.0.0', port=port, debug=True) 