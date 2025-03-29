const mongoose = require('mongoose');

const formSchema = new mongoose.Schema({
  formType: {
    type: String,
    required: true,
    enum: ['contact', 'subscription', 'feedback', 'custom']
  },
  fields: [{
    name: String,
    type: {
      type: String,
      enum: ['text', 'email', 'textarea', 'select', 'checkbox', 'radio']
    },
    label: String,
    required: Boolean,
    options: [String] // For select, radio, checkbox
  }],
  submissions: [{
    data: mongoose.Schema.Types.Mixed,
    submittedBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    submittedAt: {
      type: Date,
      default: Date.now
    },
    status: {
      type: String,
      enum: ['new', 'read', 'replied', 'archived'],
      default: 'new'
    }
  }],
  settings: {
    notifications: {
      email: Boolean,
      slack: Boolean
    },
    autoReply: Boolean,
    redirectUrl: String
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

// Index for faster queries
formSchema.index({ formType: 1 });
formSchema.index({ 'submissions.submittedAt': -1 });

module.exports = mongoose.model('Form', formSchema); 