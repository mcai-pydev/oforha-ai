from datetime import datetime
from bson import ObjectId
import bcrypt
import jwt
import os
from .db import get_collections

class User:
    def __init__(self, username, email, password=None, _id=None, created_at=None):
        self._id = _id if _id else ObjectId()
        self.username = username
        self.email = email
        self.password_hash = self._hash_password(password) if password else None
        self.created_at = created_at if created_at else datetime.utcnow()
    
    @staticmethod
    def _hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, password):
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
    
    def generate_token(self):
        payload = {
            'user_id': str(self._id),
            'username': self.username,
            'email': self.email,
            'exp': datetime.utcnow().timestamp() + 24 * 60 * 60  # 24 hours expiry
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data.get('username'),
            email=data.get('email'),
            _id=data.get('_id'),
            created_at=data.get('created_at')
        )
    
    @classmethod
    def find_by_email(cls, email):
        collections = get_collections()
        user_data = collections['users'].find_one({'email': email})
        return cls.from_dict(user_data) if user_data else None
    
    @classmethod
    def find_by_username(cls, username):
        collections = get_collections()
        user_data = collections['users'].find_one({'username': username})
        return cls.from_dict(user_data) if user_data else None
    
    def save(self):
        collections = get_collections()
        user_dict = self.to_dict()
        if self.password_hash:
            user_dict['password_hash'] = self.password_hash
        
        if '_id' in user_dict and not user_dict['_id']:
            del user_dict['_id']
            
        result = collections['users'].update_one(
            {'_id': self._id},
            {'$set': user_dict},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None 