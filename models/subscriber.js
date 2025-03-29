const mongoose = require('mongoose');

const subscriberSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true
  },
  name: {
    type: String,
    trim: true
  },
  status: {
    type: String,
    enum: ['active', 'unsubscribed', 'bounced'],
    default: 'active'
  },
  preferences: {
    categories: [String],
    frequency: {
      type: String,
      enum: ['daily', 'weekly', 'monthly'],
      default: 'weekly'
    }
  },
  metadata: {
    source: String,
    ipAddress: String,
    userAgent: String,
    location: String
  },
  subscribedAt: {
    type: Date,
    default: Date.now
  },
  lastEmailSent: Date,
  unsubscribeDate: Date
});

// Indexes for faster queries
subscriberSchema.index({ email: 1 });
subscriberSchema.index({ status: 1 });
subscriberSchema.index({ subscribedAt: -1 });

module.exports = mongoose.model('Subscriber', subscriberSchema); 