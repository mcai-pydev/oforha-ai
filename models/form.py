from datetime import datetime
from bson import ObjectId
from .db import get_collections

class Form:
    def __init__(self, form_type, data, user_id=None, submitted_at=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.form_type = form_type  # contact, feedback, etc.
        self.data = data  # The form data
        self.user_id = user_id  # Optional: ID of logged-in user
        self.submitted_at = submitted_at if submitted_at else datetime.utcnow()
    
    def to_dict(self):
        return {
            '_id': self._id,
            'form_type': self.form_type,
            'data': self.data,
            'user_id': self.user_id,
            'submitted_at': self.submitted_at
        }
    
    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return cls(
            form_type=data.get('form_type'),
            data=data.get('data'),
            user_id=data.get('user_id'),
            submitted_at=data.get('submitted_at'),
            _id=data.get('_id')
        )
    
    def save(self):
        collections = get_collections()
        form_dict = self.to_dict()
        
        if '_id' in form_dict and not form_dict['_id']:
            del form_dict['_id']
            
        result = collections['forms'].update_one(
            {'_id': self._id},
            {'$set': form_dict},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    
    @classmethod
    def get_by_type(cls, form_type, page=1, per_page=10):
        collections = get_collections()
        skip = (page - 1) * per_page
        
        forms = collections['forms'].find(
            {'form_type': form_type}
        ).sort('submitted_at', -1).skip(skip).limit(per_page)
        
        return [cls.from_dict(form) for form in forms]
    
    @classmethod
    def get_by_user(cls, user_id, page=1, per_page=10):
        collections = get_collections()
        skip = (page - 1) * per_page
        
        forms = collections['forms'].find(
            {'user_id': user_id}
        ).sort('submitted_at', -1).skip(skip).limit(per_page)
        
        return [cls.from_dict(form) for form in forms]
    
    @classmethod
    def get_count(cls, form_type=None):
        collections = get_collections()
        query = {'form_type': form_type} if form_type else {}
        return collections['forms'].count_documents(query) 