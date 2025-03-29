# Oforha AI API

A Flask-based API for handling contact forms and newsletter subscriptions.

## Features

- Contact form submission
- Newsletter subscription
- Rate limiting
- MongoDB integration
- CORS support
- Health check endpoint

## Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Git

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd oforha-ai
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `oforha_db` directory with the following variables:
```
MONGODB_URI=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret
PORT=4000
```

5. Run the application:
```bash
python wsgi.py
```

The API will be available at `http://localhost:4000`

## API Endpoints

- `GET /` - Serve the contact form page
- `GET /health` - Health check endpoint
- `POST /api/forms/submit` - Submit a contact form
- `POST /api/subscribers/subscribe` - Subscribe to newsletter
- `POST /api/subscribers/unsubscribe` - Unsubscribe from newsletter

## Development

Run tests:
```bash
python -m pytest
```

## Deployment

1. Push your code to GitHub
2. Set up environment variables in your deployment platform
3. Deploy using your preferred hosting service (e.g., Heroku, DigitalOcean, etc.)

## Security

- All sensitive information is stored in environment variables
- Rate limiting is implemented to prevent abuse
- CORS is configured for secure cross-origin requests
- Input validation is performed on all endpoints

## License

MIT