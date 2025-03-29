const mongoose = require('mongoose');

const connectDB = async () => {
  const maxRetries = 3;
  let retries = 0;

  const tryConnect = async () => {
    try {
      console.log(`Attempting to connect to MongoDB... (Attempt ${retries + 1}/${maxRetries})`);
      console.log('MongoDB URI:', process.env.MONGODB_URI);
      
      const conn = await mongoose.connect(process.env.MONGODB_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        serverSelectionTimeoutMS: 5000,
        socketTimeoutMS: 45000,
        retryWrites: true,
        retryReads: true,
      });
      
      console.log(`MongoDB Connected: ${conn.connection.host}`);
      console.log('Database Name:', conn.connection.name);
      
      // Add connection error handler
      mongoose.connection.on('error', (err) => {
        console.error('MongoDB connection error:', err);
      });
      
      // Add disconnection handler
      mongoose.connection.on('disconnected', () => {
        console.log('MongoDB disconnected');
      });
      
      return true;
      
    } catch (error) {
      console.error('MongoDB connection error:', error);
      console.error('Error details:', {
        name: error.name,
        message: error.message,
        code: error.code
      });
      
      if (retries < maxRetries - 1) {
        retries++;
        console.log(`Retrying connection in 5 seconds...`);
        await new Promise(resolve => setTimeout(resolve, 5000));
        return tryConnect();
      }
      
      return false;
    }
  };

  const success = await tryConnect();
  if (!success) {
    console.error('Failed to connect to MongoDB after multiple attempts');
    console.error('Please check if:');
    console.error('1. MongoDB is installed');
    console.error('2. MongoDB service is running');
    console.error('3. MongoDB is listening on port 27017');
    console.error('4. No firewall is blocking the connection');
    process.exit(1);
  }
};

module.exports = connectDB; 