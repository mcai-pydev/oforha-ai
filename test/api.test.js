const axios = require('axios');

const API_URL = 'http://localhost:5000/api';

// Test user data
const testUser = {
  email: 'test@example.com',
  password: 'password123',
  name: 'Test User'
};

// Test subscriber data
const testSubscriber = {
  email: 'subscriber@example.com',
  name: 'Test Subscriber',
  preferences: {
    categories: ['AI', 'Technology'],
    frequency: 'weekly'
  }
};

// Test form data
const testForm = {
  formType: 'contact',
  fields: [
    {
      name: 'name',
      type: 'text',
      label: 'Name',
      required: true
    },
    {
      name: 'email',
      type: 'email',
      label: 'Email',
      required: true
    },
    {
      name: 'message',
      type: 'textarea',
      label: 'Message',
      required: true
    }
  ],
  settings: {
    notifications: {
      email: true
    },
    autoReply: true
  }
};

async function testAPI() {
  try {
    console.log('Starting API tests...\n');

    // Test user registration
    console.log('Testing user registration...');
    const registerResponse = await axios.post(`${API_URL}/auth/register`, testUser);
    console.log('Registration successful:', registerResponse.data);
    const token = registerResponse.data.token;

    // Test user login
    console.log('\nTesting user login...');
    const loginResponse = await axios.post(`${API_URL}/auth/login`, {
      email: testUser.email,
      password: testUser.password
    });
    console.log('Login successful:', loginResponse.data);

    // Test subscriber registration
    console.log('\nTesting subscriber registration...');
    const subscriberResponse = await axios.post(`${API_URL}/subscribers/subscribe`, testSubscriber);
    console.log('Subscriber registration successful:', subscriberResponse.data);

    // Test form creation
    console.log('\nTesting form creation...');
    const formResponse = await axios.post(`${API_URL}/forms`, testForm);
    console.log('Form creation successful:', formResponse.data);
    const formId = formResponse.data._id;

    // Test form submission
    console.log('\nTesting form submission...');
    const submissionResponse = await axios.post(`${API_URL}/forms/${formId}/submit`, {
      name: 'John Doe',
      email: 'john@example.com',
      message: 'Test message'
    });
    console.log('Form submission successful:', submissionResponse.data);

    console.log('\nAll tests completed successfully!');
  } catch (error) {
    console.error('Test failed:', error.response?.data || error.message);
  }
}

testAPI(); 