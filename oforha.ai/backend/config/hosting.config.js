const config = {
    // Environment configuration
    environment: process.env.NODE_ENV || 'development',
    
    // Hosting configuration
    hosting: {
        // Primary hosting (Hostinger)
        primary: {
            type: 'hostinger',
            region: 'europe', // Vienna, Austria
            plan: 'premium',
            cost: 2.99,
            features: {
                storage: '100GB',
                bandwidth: 'unlimited',
                ram: '4GB',
                cpu: '2cores'
            }
        },
        
        // GCP for AI components only
        ai: {
            type: 'gcp',
            project: 'oforha-ai',
            region: 'us-central1',
            components: {
                vertexAI: {
                    enabled: true,
                    model: 'gemini-pro',
                    maxTokens: 2048,
                    temperature: 0.7
                },
                cloudStorage: {
                    enabled: true,
                    bucket: 'oforha-ai-storage',
                    maxSize: '10GB'
                }
            }
        }
    },
    
    // Cost optimization settings
    optimization: {
        // Cache configuration
        cache: {
            enabled: true,
            ttl: 3600, // 1 hour
            maxSize: '1GB'
        },
        
        // AI request batching
        batching: {
            enabled: true,
            maxBatchSize: 10,
            timeout: 1000 // ms
        },
        
        // Resource limits
        limits: {
            maxConcurrentRequests: 100,
            maxMemoryUsage: '2GB',
            maxCPUUsage: 80 // percentage
        }
    },
    
    // Monitoring and scaling
    monitoring: {
        enabled: true,
        metrics: ['cpu', 'memory', 'requests', 'latency'],
        alerts: {
            cpuThreshold: 80,
            memoryThreshold: 85,
            latencyThreshold: 1000
        }
    }
};

module.exports = config; 