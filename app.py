from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from routes.auth import auth
from routes.subscribers import subscribers
from routes.forms import forms
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables from oforha_db/.env
dotenv_path = os.path.join(os.path.dirname(__file__), 'oforha_db', '.env')
load_dotenv(dotenv_path)

def create_app():
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    CORS(app)
    
    # Initialize rate limiter with default storage
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Register blueprints
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(subscribers, url_prefix='/api/subscribers')
    app.register_blueprint(forms, url_prefix='/api/forms')
    
    # Root route - serve the HTML page
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Health check endpoint
    @app.route('/health')
    @limiter.limit("30 per minute")
    def health_check():
        return {'status': 'healthy'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'message': 'Internal server error'}), 500
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            'message': 'Rate limit exceeded',
            'description': str(e.description),
            'retry_after': e.retry_after,
            'limit': e.limit,
            'remaining': e.remaining
        }), 429
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Get port from environment variable, default to 4000 if not set
    port = int(os.environ.get('PORT', '4000'))
    print(f"Starting server on port {port}")
    print(f"Using .env file from: {dotenv_path}")
    print(f"Environment variables loaded: PORT={port}, MONGODB_URI={'*' * 20}")
    app.run(host='0.0.0.0', port=port, debug=True) 