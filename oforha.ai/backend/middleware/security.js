const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const xss = require('xss-clean');
const mongoSanitize = require('express-mongo-sanitize');

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});

// Security middleware
const securityMiddleware = [
    // Set security HTTP headers
    helmet(),
    
    // Rate limiting
    limiter,
    
    // Data sanitization against XSS
    xss(),
    
    // Data sanitization against NoSQL query injection
    mongoSanitize()
];

module.exports = securityMiddleware; 