from datetime import datetime
from bson import ObjectId
from .db import get_collections

class Subscriber:
    def __init__(self, email, name=None, subscribed_at=None, status='active', _id=None):
        self._id = _id if _id else ObjectId()
        self.email = email
        self.name = name
        self.subscribed_at = subscribed_at if subscribed_at else datetime.utcnow()
        self.status = status  # active, unsubscribed, bounced
    
    def to_dict(self):
        return {
            '_id': self._id,
            'email': self.email,
            'name': self.name,
            'subscribed_at': self.subscribed_at,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return cls(
            email=data.get('email'),
            name=data.get('name'),
            subscribed_at=data.get('subscribed_at'),
            status=data.get('status', 'active'),
            _id=data.get('_id')
        )
    
    @classmethod
    def find_by_email(cls, email):
        collections = get_collections()
        subscriber_data = collections['subscribers'].find_one({'email': email})
        return cls.from_dict(subscriber_data)
    
    @classmethod
    def get_active_subscribers(cls):
        collections = get_collections()
        subscribers_data = collections['subscribers'].find({'status': 'active'})
        return [cls.from_dict(data) for data in subscribers_data]
    
    def save(self):
        collections = get_collections()
        subscriber_dict = self.to_dict()
        
        if '_id' in subscriber_dict and not subscriber_dict['_id']:
            del subscriber_dict['_id']
            
        result = collections['subscribers'].update_one(
            {'_id': self._id},
            {'$set': subscriber_dict},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    
    def unsubscribe(self):
        self.status = 'unsubscribed'
        return self.save()
    
    @classmethod
    def bulk_subscribe(cls, emails):
        collections = get_collections()
        now = datetime.utcnow()
        subscribers = [
            {
                'email': email,
                'subscribed_at': now,
                'status': 'active'
            }
            for email in emails
        ]
        if subscribers:
            result = collections['subscribers'].insert_many(subscribers)
            return len(result.inserted_ids)
        return 0 