const mongoose = require('mongoose');
require('dotenv').config({ path: require('path').join(__dirname, '.env') });

const testConnection = async () => {
  try {
    console.log('Attempting to connect to MongoDB...');
    console.log('MongoDB URI:', process.env.MONGODB_URI);
    
    const conn = await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    
    console.log('Successfully connected to MongoDB!');
    console.log('Database:', conn.connection.name);
    console.log('Host:', conn.connection.host);
    
    // Test creating a document
    const Test = mongoose.model('Test', { name: String });
    await Test.create({ name: 'test' });
    console.log('Successfully created test document');
    
    // Clean up
    await Test.deleteMany({});
    console.log('Cleaned up test documents');
    
    await mongoose.connection.close();
    console.log('Connection closed successfully');
    
  } catch (error) {
    console.error('Connection error:', error);
    process.exit(1);
  }
};

testConnection(); 