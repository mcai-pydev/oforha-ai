const { VertexAI } = require('@google-cloud/vertexai');
const { Storage } = require('@google-cloud/storage');
const { BigQuery } = require('@google-cloud/bigquery');

class AIService {
    constructor() {
        this.vertexai = new VertexAI({project: 'oforha-ai', location: 'us-central1'});
        this.storage = new Storage();
        this.bigquery = new BigQuery();
    }

    // Chatbot with context-aware responses
    async handleChatbotQuery(query, context) {
        const model = this.vertexai.preview.getGenerativeModel({
            model: 'gemini-pro',
            generation_config: {
                max_output_tokens: 2048,
                temperature: 0.7
            }
        });

        try {
            const response = await model.generateContent({
                contents: [{ role: 'user', parts: [{ text: this.buildPrompt(query, context) }] }]
            });
            return response.response.candidates[0].content;
        } catch (error) {
            console.error('Chatbot error:', error);
            throw new Error('Failed to process chatbot query');
        }
    }

    // Recommendation system using user behavior
    async generateRecommendations(userId) {
        const query = `
            SELECT * FROM \`oforha-ai.user_data.interactions\`
            WHERE user_id = @userId
            ORDER BY timestamp DESC
            LIMIT 100
        `;
        
        try {
            const [rows] = await this.bigquery.query({
                query,
                params: { userId }
            });
            
            // Process with Vertex AI for personalized recommendations
            const model = this.vertexai.preview.getGenerativeModel({
                model: 'gemini-pro'
            });
            
            return await model.generateContent({
                contents: [{ role: 'user', parts: [{ text: this.buildRecommendationPrompt(rows) }] }]
            });
        } catch (error) {
            console.error('Recommendation error:', error);
            throw new Error('Failed to generate recommendations');
        }
    }

    // Sentiment analysis with enhanced context
    async analyzeSentiment(text) {
        const model = this.vertexai.preview.getGenerativeModel({
            model: 'gemini-pro'
        });

        try {
            const response = await model.generateContent({
                contents: [{
                    role: 'user',
                    parts: [{
                        text: `Analyze the sentiment and key aspects of the following text. 
                               Provide a detailed breakdown including:
                               1. Overall sentiment (positive/negative/neutral)
                               2. Key topics discussed
                               3. Emotional intensity
                               4. Action items or recommendations
                               
                               Text: "${text}"`
                    }]
                }]
            });
            return response.response.candidates[0].content;
        } catch (error) {
            console.error('Sentiment analysis error:', error);
            throw new Error('Failed to analyze sentiment');
        }
    }

    // RAG-based content generation
    async generateContent(topic, context) {
        // Fetch relevant documents from Cloud Storage
        const docs = await this.fetchRelevantDocs(topic);
        
        const model = this.vertexai.preview.getGenerativeModel({
            model: 'gemini-pro'
        });

        try {
            const response = await model.generateContent({
                contents: [{
                    role: 'user',
                    parts: [{
                        text: this.buildRAGPrompt(topic, docs, context)
                    }]
                }]
            });
            return response.response.candidates[0].content;
        } catch (error) {
            console.error('Content generation error:', error);
            throw new Error('Failed to generate content');
        }
    }

    // Predictive maintenance
    async predictMaintenance(systemData) {
        const model = this.vertexai.preview.getGenerativeModel({
            model: 'gemini-pro'
        });

        try {
            const response = await model.generateContent({
                contents: [{
                    role: 'user',
                    parts: [{
                        text: `Analyze the following system data and predict potential maintenance needs:
                               ${JSON.stringify(systemData, null, 2)}`
                    }]
                }]
            });
            return response.response.candidates[0].content;
        } catch (error) {
            console.error('Prediction error:', error);
            throw new Error('Failed to generate maintenance prediction');
        }
    }

    // Helper methods
    buildPrompt(query, context) {
        return `Context: ${context}\nQuery: ${query}\nProvide a helpful and contextually relevant response.`;
    }

    buildRecommendationPrompt(userData) {
        return `Based on the following user interactions, suggest personalized recommendations:
                ${JSON.stringify(userData, null, 2)}`;
    }

    buildRAGPrompt(topic, docs, context) {
        return `Topic: ${topic}
                Context: ${context}
                Reference Documents: ${JSON.stringify(docs, null, 2)}
                Generate comprehensive and accurate content using the provided references.`;
    }

    async fetchRelevantDocs(topic) {
        // Implement vector similarity search here
        // This is a placeholder
        return [];
    }
}

module.exports = new AIService(); 