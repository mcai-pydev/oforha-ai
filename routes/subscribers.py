from flask import Blueprint, request, jsonify
from models import Subscriber
from routes.auth import token_required
import re

subscribers = Blueprint('subscribers', __name__)

def is_valid_email(email):
    """Validate email format using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@subscribers.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    
    # Validate required fields
    if not data or 'email' not in data:
        return jsonify({'message': 'Email is required'}), 400
    
    # Validate email format
    if not is_valid_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 400
    
    # Check if already subscribed
    existing_subscriber = Subscriber.find_by_email(data['email'])
    if existing_subscriber:
        if existing_subscriber.status == 'active':
            return jsonify({'message': 'Already subscribed'}), 400
        else:
            # Reactivate unsubscribed user
            existing_subscriber.status = 'active'
            existing_subscriber.save()
            return jsonify({'message': 'Resubscribed successfully'})
    
    # Create new subscriber
    subscriber = Subscriber(
        email=data['email'],
        name=data.get('name')
    )
    
    if subscriber.save():
        return jsonify({
            'message': 'Subscribed successfully',
            'subscriber': {
                'email': subscriber.email,
                'name': subscriber.name,
                'subscribed_at': subscriber.subscribed_at
            }
        }), 201
    else:
        return jsonify({'message': 'Error creating subscription'}), 500

@subscribers.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({'message': 'Email is required'}), 400
    
    # Validate email format
    if not is_valid_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 400
    
    subscriber = Subscriber.find_by_email(data['email'])
    if not subscriber:
        return jsonify({'message': 'Subscriber not found'}), 404
    
    if subscriber.unsubscribe():
        return jsonify({'message': 'Unsubscribed successfully'})
    else:
        return jsonify({'message': 'Error unsubscribing'}), 500

@subscribers.route('/subscribers', methods=['GET'])
@token_required
def get_subscribers():
    # Get query parameters
    status = request.args.get('status', 'active')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Get subscribers
    subscribers = Subscriber.get_active_subscribers()
    
    # Paginate results
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_subscribers = subscribers[start_idx:end_idx]
    
    return jsonify({
        'subscribers': [
            {
                'email': sub.email,
                'name': sub.name,
                'subscribed_at': sub.subscribed_at,
                'status': sub.status
            }
            for sub in paginated_subscribers
        ],
        'total': len(subscribers),
        'page': page,
        'per_page': per_page
    })

@subscribers.route('/bulk-subscribe', methods=['POST'])
@token_required
def bulk_subscribe():
    data = request.get_json()
    
    if not data or 'emails' not in data:
        return jsonify({'message': 'List of emails is required'}), 400
    
    emails = data['emails']
    if not isinstance(emails, list):
        return jsonify({'message': 'Emails must be a list'}), 400
    
    # Validate all emails
    invalid_emails = [email for email in emails if not is_valid_email(email)]
    if invalid_emails:
        return jsonify({
            'message': 'Invalid email format(s)',
            'invalid_emails': invalid_emails
        }), 400
    
    count = Subscriber.bulk_subscribe(emails)
    return jsonify({
        'message': f'Successfully subscribed {count} users',
        'count': count
    }) 