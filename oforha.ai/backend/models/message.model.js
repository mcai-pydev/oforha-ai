const mongoose = require('mongoose');
const { v4: uuidv4 } = require('uuid');

const messageSchema = new mongoose.Schema({
    trackingId: {
        type: String,
        default: () => `MSG-${uuidv4()}`,
        unique: true
    },
    name: { 
        type: String, 
        required: [true, 'Name is required'],
        trim: true,
        maxLength: [50, 'Name cannot be more than 50 characters']
    },
    email: { 
        type: String, 
        required: [true, 'Email is required'],
        match: [/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid email'],
        trim: true
    },
    message: { 
        type: String, 
        required: [true, 'Message is required'],
        trim: true,
        maxLength: [1000, 'Message cannot be more than 1000 characters']
    },
    status: {
        type: String,
        enum: ['pending', 'sent', 'failed'],
        default: 'pending'
    },
    createdAt: { 
        type: Date, 
        default: Date.now 
    },
    emailSentAt: {
        type: Date
    }
});

// Add indexes for better query performance
messageSchema.index({ trackingId: 1 });
messageSchema.index({ createdAt: -1 });
messageSchema.index({ status: 1 });

module.exports = mongoose.model('Message', messageSchema); 