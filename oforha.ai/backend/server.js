const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const nodemailer = require('nodemailer');
const config = require('./config/config');
const Message = require('./models/message.model');
const securityMiddleware = require('./middleware/security');

const app = express();

// Security Middleware
app.use(securityMiddleware);

// Basic Middleware
app.use(cors(config.cors));
app.use(express.json({ limit: '10kb' })); // Limit body size

// Configure Email Transporter
const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: process.env.SMTP_PORT,
    secure: true, // Use SSL
    auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
    },
    debug: true, // Enable debug logging
    logger: true  // Log to console
});

// Verify email configuration
transporter.verify(function(error, success) {
    if (error) {
        console.error('Email configuration error:', error);
        console.error('SMTP Settings:', {
            host: process.env.SMTP_HOST,
            port: process.env.SMTP_PORT,
            user: process.env.SMTP_USER,
            secure: true,
            fromEmail: process.env.FROM_EMAIL,
            toEmail: process.env.TO_EMAIL
        });
    } else {
        console.log('Email server is ready to send messages');
    }
});

// MongoDB Connection with retry logic
const connectDB = async () => {
    try {
        await mongoose.connect(config.mongoUri, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
            serverSelectionTimeoutMS: 5000
        });
        console.log('Connected to MongoDB');
    } catch (err) {
        console.error('MongoDB connection error:', err);
        setTimeout(connectDB, 5000);
    }
};

connectDB();

// Email template function
const getEmailTemplate = (name, email, message, trackingId) => `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #7600bc; color: white; padding: 20px; border-radius: 5px 5px 0 0; }
        .content { padding: 20px; border: 1px solid #ddd; border-radius: 0 0 5px 5px; }
        .footer { margin-top: 20px; font-size: 12px; color: #666; }
        .tracking { background: #f5f5f5; padding: 10px; border-radius: 4px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>New Contact Form Submission</h2>
        </div>
        <div class="content">
            <p><strong>Name:</strong> ${name}</p>
            <p><strong>Email:</strong> ${email}</p>
            <p><strong>Message:</strong></p>
            <p style="white-space: pre-wrap;">${message}</p>
            <div class="tracking">
                <p><strong>Tracking ID:</strong> ${trackingId}</p>
            </div>
        </div>
        <div class="footer">
            <p>This message was sent from the Oforha.ai contact form.</p>
        </div>
    </div>
</body>
</html>
`;

// Contact Form Endpoint with improved error handling
app.post('/api/contact', async (req, res) => {
    try {
        const { name, email, message } = req.body;

        // Validate input
        if (!name || !email || !message) {
            return res.status(400).json({ 
                error: 'Please provide all required fields' 
            });
        }

        // Save to MongoDB
        const newMessage = new Message({
            name,
            email,
            message
        });
        await newMessage.save();

        // Send email
        const mailOptions = {
            from: {
                name: 'Oforha.ai Contact Form',
                address: process.env.FROM_EMAIL
            },
            to: process.env.TO_EMAIL,
            replyTo: email,
            subject: `New Contact Form Submission from ${name}`,
            html: getEmailTemplate(name, email, message, newMessage.trackingId)
        };

        // Send email with better error handling
        try {
            const info = await transporter.sendMail(mailOptions);
            console.log('Email sent:', info.messageId);
            
            // Update message status
            newMessage.status = 'sent';
            newMessage.emailSentAt = new Date();
            await newMessage.save();

            res.status(200).json({ 
                message: 'Message sent successfully',
                trackingId: newMessage.trackingId,
                emailId: info.messageId
            });
        } catch (emailError) {
            console.error('Email sending failed:', emailError);
            
            // Update message status to failed
            newMessage.status = 'failed';
            await newMessage.save();
            
            throw new Error('Failed to send email notification');
        }
    } catch (error) {
        console.error('Error:', error);
        
        // Handle different types of errors
        if (error.name === 'ValidationError') {
            return res.status(400).json({ 
                error: Object.values(error.errors).map(err => err.message).join(', ')
            });
        }
        
        if (error.code === 11000) {
            return res.status(400).json({ 
                error: 'A message with this information already exists' 
            });
        }

        res.status(500).json({ 
            error: error.message || 'Failed to send message. Please try again later.' 
        });
    }
});

// Message tracking endpoint
app.get('/api/messages/:trackingId', async (req, res) => {
    try {
        const message = await Message.findOne({ 
            trackingId: req.params.trackingId 
        }).select('-__v');

        if (!message) {
            return res.status(404).json({ 
                error: 'Message not found' 
            });
        }

        res.json(message);
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ 
            error: 'Failed to retrieve message' 
        });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.status(200).json({ 
        status: 'ok',
        mongodb: mongoose.connection.readyState === 1,
        environment: config.env,
        emailConfigured: !!transporter
    });
});

// Test email endpoint (remove in production)
app.post('/api/test-email', async (req, res) => {
    try {
        const testMailOptions = {
            from: {
                name: 'Oforha.ai Test',
                address: process.env.FROM_EMAIL
            },
            to: process.env.TO_EMAIL,
            subject: 'Test Email from Oforha.ai',
            html: `
                <h2>Test Email</h2>
                <p>This is a test email to verify the email configuration.</p>
                <p>Time sent: ${new Date().toISOString()}</p>
            `
        };

        const info = await transporter.sendMail(testMailOptions);
        console.log('Test email sent:', info.messageId);
        
        res.status(200).json({ 
            message: 'Test email sent successfully',
            messageId: info.messageId,
            previewURL: nodemailer.getTestMessageUrl(info)
        });
    } catch (error) {
        console.error('Test email failed:', error);
        res.status(500).json({ 
            error: 'Failed to send test email',
            details: error.message
        });
    }
});

const PORT = config.port;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT} in ${config.env} mode`);
}); 