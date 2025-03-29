const config = {
    // Scaling tiers configuration
    tiers: {
        development: {
            name: 'Development',
            maxUsers: 100,
            resources: {
                hostinger: {
                    plan: 'premium',
                    cost: 2.99,
                    ram: '4GB',
                    cpu: '2cores'
                },
                gcp: {
                    vertexAI: {
                        requestsPerMinute: 60,
                        maxConcurrent: 10
                    },
                    storage: {
                        maxSize: '10GB'
                    }
                }
            }
        },
        production: {
            name: 'Production',
            maxUsers: 1000,
            resources: {
                hostinger: {
                    plan: 'premium',
                    cost: 2.99,
                    ram: '4GB',
                    cpu: '2cores'
                },
                gcp: {
                    vertexAI: {
                        requestsPerMinute: 300,
                        maxConcurrent: 50
                    },
                    storage: {
                        maxSize: '50GB'
                    }
                }
            }
        },
        enterprise: {
            name: 'Enterprise',
            maxUsers: 10000,
            resources: {
                hostinger: {
                    plan: 'business',
                    cost: 4.99,
                    ram: '8GB',
                    cpu: '4cores'
                },
                gcp: {
                    vertexAI: {
                        requestsPerMinute: 1000,
                        maxConcurrent: 200
                    },
                    storage: {
                        maxSize: '200GB'
                    }
                }
            }
        }
    },

    // Local n8n integration
    n8n: {
        enabled: true,
        local: {
            port: 5678,
            workflows: {
                aiProcessing: {
                    enabled: true,
                    maxConcurrent: 5,
                    timeout: 30000
                },
                dataSync: {
                    enabled: true,
                    interval: '5m',
                    batchSize: 100
                },
                monitoring: {
                    enabled: true,
                    metrics: ['workflowRuns', 'executionTime', 'errors']
                }
            }
        }
    },

    // Development tools integration
    development: {
        cursor: {
            enabled: true,
            features: ['codeCompletion', 'pairProgramming', 'codeReview'],
            maxConcurrent: 5
        },
        gpt: {
            enabled: true,
            model: 'gpt-4-turbo-preview',
            maxTokens: 4096,
            features: ['codeGeneration', 'documentation', 'optimization']
        }
    },

    // Auto-scaling rules
    autoScaling: {
        enabled: true,
        rules: [
            {
                metric: 'cpu',
                threshold: 80,
                action: 'scaleUp',
                cooldown: 300
            },
            {
                metric: 'memory',
                threshold: 85,
                action: 'scaleUp',
                cooldown: 300
            },
            {
                metric: 'requests',
                threshold: 1000,
                action: 'scaleUp',
                cooldown: 300
            }
        ],
        limits: {
            maxInstances: 3,
            minInstances: 1,
            scaleUpIncrement: 1,
            scaleDownIncrement: 1
        }
    },

    // Cost optimization
    optimization: {
        // Cache strategy
        cache: {
            enabled: true,
            strategy: 'hybrid',
            levels: {
                memory: {
                    enabled: true,
                    maxSize: '1GB',
                    ttl: 3600
                },
                redis: {
                    enabled: true,
                    maxSize: '5GB',
                    ttl: 86400
                }
            }
        },

        // Resource utilization
        resources: {
            cpu: {
                target: 70,
                max: 90
            },
            memory: {
                target: 75,
                max: 90
            },
            storage: {
                target: 80,
                max: 95
            }
        },

        // AI request optimization
        ai: {
            batching: {
                enabled: true,
                maxBatchSize: 10,
                timeout: 1000
            },
            caching: {
                enabled: true,
                ttl: 3600,
                maxSize: '2GB'
            }
        }
    },

    // Monitoring and alerts
    monitoring: {
        enabled: true,
        metrics: {
            system: ['cpu', 'memory', 'disk', 'network'],
            application: ['requests', 'latency', 'errors'],
            ai: ['modelLatency', 'tokenUsage', 'cost'],
            n8n: ['workflowSuccess', 'executionTime', 'queueSize']
        },
        alerts: {
            cpu: {
                warning: 80,
                critical: 90
            },
            memory: {
                warning: 85,
                critical: 95
            },
            latency: {
                warning: 1000,
                critical: 2000
            },
            errors: {
                warning: 5,
                critical: 10
            }
        }
    }
};

module.exports = config; 