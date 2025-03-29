require('dotenv').config();

const config = {
    env: process.env.NODE_ENV || 'development',
    port: process.env.PORT || 5000,
    mongoUri: process.env.MONGODB_URI || 'mongodb://localhost:27017/oforha_contacts',
    sendgrid: {
        apiKey: process.env.SENDGRID_API_KEY,
        fromEmail: process.env.FROM_EMAIL,
        toEmail: process.env.TO_EMAIL
    },
    cors: {
        origin: process.env.NODE_ENV === 'production' 
            ? 'https://mcai-pydev.github.io'
            : 'http://localhost:3000'
    },
    messageTracking: {
        enabled: true,
        prefix: 'MSG-'
    }
};

module.exports = config; 