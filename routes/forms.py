from flask import Blueprint, request, jsonify
from models import Form, User
from routes.auth import token_required
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

forms = Blueprint('forms', __name__)

def validate_form_data(data):
    """Validate form submission data"""
    if not data:
        raise BadRequest('No data provided')
    
    if 'form_type' not in data:
        raise BadRequest('Form type is required')
    
    if 'data' not in data:
        raise BadRequest('Form data is required')
    
    if not isinstance(data['data'], dict):
        raise BadRequest('Form data must be a JSON object')
    
    # Validate required fields based on form type
    required_fields = {
        'contact': ['name', 'email', 'message'],
        'feedback': ['rating', 'comment'],
        'support': ['subject', 'description', 'priority']
    }
    
    if data['form_type'] in required_fields:
        missing_fields = [field for field in required_fields[data['form_type']] 
                         if field not in data['data']]
        if missing_fields:
            raise BadRequest(f"Missing required fields for {data['form_type']} form: {', '.join(missing_fields)}")

@forms.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        validate_form_data(data)
        
        # Get user_id from token if available
        user_id = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            payload = User.verify_token(token)
            if payload:
                user_id = payload['user_id']
        
        # Create form submission
        form = Form(
            form_type=data['form_type'],
            data=data['data'],
            user_id=user_id
        )
        
        if form.save():
            return jsonify({
                'message': 'Form submitted successfully',
                'form_id': str(form._id)
            }), 201
        else:
            return jsonify({'message': 'Error submitting form'}), 500
            
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@forms.route('/forms/<form_type>', methods=['GET'])
@token_required
def get_forms(form_type):
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Validate form type
        valid_types = ['contact', 'feedback', 'support']
        if form_type not in valid_types:
            raise BadRequest(f"Invalid form type. Must be one of: {', '.join(valid_types)}")
        
        # Get forms
        forms = Form.get_by_type(form_type, page, per_page)
        total = Form.get_count(form_type)
        
        return jsonify({
            'forms': [
                {
                    'id': str(form._id),
                    'form_type': form.form_type,
                    'data': form.data,
                    'user_id': form.user_id,
                    'submitted_at': form.submitted_at
                }
                for form in forms
            ],
            'total': total,
            'page': page,
            'per_page': per_page
        })
        
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@forms.route('/my-forms', methods=['GET'])
@token_required
def get_my_forms():
    try:
        # Get user_id from token
        token = request.headers.get('Authorization').split(' ')[1]
        payload = User.verify_token(token)
        if not payload:
            raise Unauthorized('Invalid or expired token')
            
        user_id = payload['user_id']
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Get user's forms
        forms = Form.get_by_user(user_id, page, per_page)
        total = Form.get_count(user_id=user_id)
        
        return jsonify({
            'forms': [
                {
                    'id': str(form._id),
                    'form_type': form.form_type,
                    'data': form.data,
                    'submitted_at': form.submitted_at
                }
                for form in forms
            ],
            'total': total,
            'page': page,
            'per_page': per_page
        })
        
    except Unauthorized as e:
        return jsonify({'message': str(e)}), 401
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500 