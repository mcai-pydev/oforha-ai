const { OpenAI } = require('openai');
const { ChromaClient } = require('chromadb');
const { Document } = require('langchain/document');
const { RecursiveCharacterTextSplitter } = require('langchain/text_splitter');

class RAGService {
    constructor() {
        this.openai = new OpenAI();
        this.chromadb = new ChromaClient();
        this.collection = null;
    }

    async initialize() {
        this.collection = await this.chromadb.createCollection({
            name: 'oforha_knowledge_base',
            metadata: { description: 'AI and ML knowledge base' }
        });
    }

    // Enhanced document processing with GPT-4
    async processDocuments(documents) {
        const splitter = new RecursiveCharacterTextSplitter({
            chunkSize: 1500,
            chunkOverlap: 200
        });

        const chunks = await splitter.splitDocuments(documents);

        // Use GPT-4 to enhance chunks with metadata
        const enhancedChunks = await Promise.all(chunks.map(async chunk => {
            const enhancement = await this.openai.chat.completions.create({
                model: "gpt-4-turbo-preview",
                messages: [{
                    role: "system",
                    content: "Analyze this text chunk and provide key concepts, topics, and relationships."
                }, {
                    role: "user",
                    content: chunk.pageContent
                }]
            });

            const metadata = JSON.parse(enhancement.choices[0].message.content);
            return {
                ...chunk,
                metadata: {
                    ...chunk.metadata,
                    ...metadata,
                    embedding_model: "openai-text-embedding-3-large"
                }
            };
        }));

        return enhancedChunks;
    }

    // Semantic search with context-aware reranking
    async semanticSearch(query, topK = 5) {
        // Generate query embedding
        const queryEmbedding = await this.openai.embeddings.create({
            model: "text-embedding-3-large",
            input: query
        });

        // Search in ChromaDB
        const results = await this.collection.query({
            queryEmbeddings: [queryEmbedding.data[0].embedding],
            nResults: topK * 2  // Get more results for reranking
        });

        // Use GPT-4 to rerank results based on relevance
        const reranking = await this.openai.chat.completions.create({
            model: "gpt-4-turbo-preview",
            messages: [{
                role: "system",
                content: "Rerank these search results based on relevance to the query. Return JSON array of indices in order of relevance."
            }, {
                role: "user",
                content: JSON.stringify({
                    query: query,
                    results: results.documents[0]
                })
            }]
        });

        const rerankedIndices = JSON.parse(reranking.choices[0].message.content);
        return rerankedIndices.slice(0, topK).map(idx => results.documents[0][idx]);
    }

    // Generate contextual response using retrieved documents
    async generateResponse(query, retrievedDocs) {
        const response = await this.openai.chat.completions.create({
            model: "gpt-4-turbo-preview",
            messages: [{
                role: "system",
                content: "Generate a comprehensive response using the provided context. Cite sources where appropriate."
            }, {
                role: "user",
                content: `
                Query: ${query}
                
                Retrieved Context:
                ${retrievedDocs.join('\n\n')}
                
                Generate a detailed response that incorporates the relevant information from the context.
                `
            }]
        });

        return {
            response: response.choices[0].message.content,
            sources: retrievedDocs.map(doc => doc.metadata.source)
        };
    }

    // Continuous learning and optimization
    async optimizeSystem(queryLogs) {
        const analysis = await this.openai.chat.completions.create({
            model: "gpt-4-turbo-preview",
            messages: [{
                role: "system",
                content: "Analyze query logs to identify patterns and suggest optimizations for the RAG system."
            }, {
                role: "user",
                content: JSON.stringify(queryLogs)
            }]
        });

        return {
            insights: JSON.parse(analysis.choices[0].message.content),
            timestamp: new Date()
        };
    }
}

module.exports = new RAGService(); 