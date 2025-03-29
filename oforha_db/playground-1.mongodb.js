// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// Select the database to use.
use('oforha-ai');

// Create a new collection
db.createCollection('users');

// Insert a few documents into the users collection.
db.users.insertMany([
  {
    'username': 'test_user1',
    'email': 'user1@example.com',
    'role': 'user',
    'created_at': new Date()
  },
  {
    'username': 'test_user2',
    'email': 'user2@example.com',
    'role': 'admin',
    'created_at': new Date()
  }
]);

// Find all documents in the users collection
db.users.find();

// Find documents with role = "admin"
db.users.find({ 'role': 'admin' });

// Update a document
db.users.updateOne(
  { 'username': 'test_user1' },
  {
    $set: {
      'role': 'premium_user'
    }
  }
);

// Create an index
db.users.createIndex({ 'email': 1 }, { unique: true });

// Count documents
db.users.countDocuments({});

// Aggregate example - group users by role
db.users.aggregate([
  {
    $group: {
      _id: '$role',
      count: { $sum: 1 },
      users: { $push: '$username' }
    }
  }
]); 