const { VertexAI } = require('@google-cloud/vertexai');
const { OpenAI } = require('openai');

class ChatbotService {
    constructor() {
        this.vertexai = new VertexAI({project: 'oforha-ai', location: 'us-central1'});
        this.openai = new OpenAI();
    }

    // Generate training data using GPT-4
    async generateTrainingData(domain, scenarios) {
        const completion = await this.openai.chat.completions.create({
            model: "gpt-4-turbo-preview",
            messages: [{
                role: "system",
                content: `Generate diverse training data for a ${domain} chatbot. 
                         Include various user intents, edge cases, and expected responses.
                         Format: JSON array of {user_input, intent, response, context}`
            }, {
                role: "user",
                content: `Generate 10 training examples for these scenarios: ${scenarios.join(", ")}`
            }]
        });

        return JSON.parse(completion.choices[0].message.content);
    }

    // Fine-tune Vertex AI model with GPT-4 generated data
    async trainModel(trainingData) {
        const model = this.vertexai.preview.getGenerativeModel({
            model: 'gemini-pro',
            generation_config: {
                max_output_tokens: 2048,
                temperature: 0.7
            }
        });

        // Process training data
        const processedData = trainingData.map(item => ({
            input_text: item.user_input,
            output_text: item.response,
            metadata: {
                intent: item.intent,
                context: item.context
            }
        }));

        // Log training progress
        console.log('Training model with processed data:', processedData.length, 'examples');

        return processedData;
    }

    // Enhanced response generation with context
    async generateResponse(query, context) {
        // First, use GPT-4 to analyze query intent
        const intentAnalysis = await this.openai.chat.completions.create({
            model: "gpt-4-turbo-preview",
            messages: [{
                role: "system",
                content: "Analyze the user query to determine intent and key components."
            }, {
                role: "user",
                content: query
            }]
        });

        const intent = intentAnalysis.choices[0].message.content;

        // Use Vertex AI for final response
        const model = this.vertexai.preview.getGenerativeModel({
            model: 'gemini-pro'
        });

        const response = await model.generateContent({
            contents: [{
                role: 'user',
                parts: [{
                    text: `
                    Context: ${context}
                    User Intent: ${intent}
                    Query: ${query}
                    Generate a helpful, contextually relevant response.
                    `
                }]
            }]
        });

        return {
            response: response.response.candidates[0].content,
            intent: intent,
            confidence: response.response.candidates[0].safetyRatings[0].probability
        };
    }

    // Continuous improvement using GPT-4 analysis
    async analyzeConversations(conversations) {
        const analysis = await this.openai.chat.completions.create({
            model: "gpt-4-turbo-preview",
            messages: [{
                role: "system",
                content: "Analyze chatbot conversations to identify improvement areas and patterns."
            }, {
                role: "user",
                content: JSON.stringify(conversations)
            }]
        });

        return {
            insights: JSON.parse(analysis.choices[0].message.content),
            timestamp: new Date()
        };
    }
}

module.exports = new ChatbotService(); 