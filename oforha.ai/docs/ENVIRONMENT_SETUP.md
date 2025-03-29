# Environment Setup Guide

This guide provides detailed instructions for setting up and managing environment variables in the Oforha.ai project.

## Table of Contents
1. [Overview](#overview)
2. [Environment Files](#environment-files)
3. [Setup Process](#setup-process)
4. [Validation](#validation)
5. [Environment-Specific Configurations](#environment-specific-configurations)
6. [Security Considerations](#security-considerations)
7. [Troubleshooting](#troubleshooting)

## Overview

The Oforha.ai project uses environment variables to manage configuration across different environments (development, staging, production). This setup ensures secure and flexible configuration management.

## Environment Files

The project includes several environment-related files:

- `.env`: Main environment file (not committed to version control)
- `.env.example`: Template file with placeholder values
- `config/environments/development.env`: Development-specific configuration
- `config/environments/production.env`: Production-specific configuration
- `scripts/setup-env.sh`: Setup script for environment variables
- `scripts/validate-env.sh`: Validation script for environment variables

## Setup Process

### 1. Initial Setup

```bash
# Clone the repository
git clone https://github.com/your-username/oforha.ai.git
cd oforha.ai

# Make setup script executable
chmod +x scripts/setup-env.sh

# Run setup script
./scripts/setup-env.sh
```

### 2. Required Variables

The following variables must be set:

- `MONGODB_URI`: MongoDB connection string
- `REDIS_HOST`: Redis host address
- `OPENAI_API_KEY`: OpenAI API key
- `JWT_SECRET`: Secret for JWT token generation
- `SENDGRID_API_KEY`: SendGrid API key
- `AI_SERVICE_API_KEY`: AI service API key

### 3. Optional Variables

Additional variables can be configured based on your needs:

- `NODE_ENV`: Environment (development/production)
- `PORT`: Server port
- `API_VERSION`: API version
- `LOG_LEVEL`: Logging level
- Various feature flags and service configurations

## Validation

### 1. Running Validation

```bash
# Make validation script executable
chmod +x scripts/validate-env.sh

# Run validation
./scripts/validate-env.sh
```

### 2. What Gets Validated

The validation script checks:

- Required variables are set
- URL formats are valid
- Numeric values are within ranges
- Boolean values are valid
- File paths exist
- Directory paths exist
- Database connections work
- Redis connections work

## Environment-Specific Configurations

### Development Environment

- Debug mode enabled
- Detailed logging
- Mock services available
- Development tools enabled
- Relaxed security settings
- Local database connections

### Production Environment

- Debug mode disabled
- Optimized logging
- Real services required
- Development tools disabled
- Strict security settings
- Remote database connections
- CDN enabled
- Performance optimizations enabled

## Security Considerations

### 1. Sensitive Data

Never commit sensitive data to version control:
- API keys
- Database credentials
- JWT secrets
- Service passwords

### 2. File Permissions

Ensure proper file permissions:
```bash
chmod 600 .env
chmod 644 .env.example
```

### 3. Environment Variables

- Use strong, unique values for secrets
- Rotate secrets regularly
- Use different values for each environment
- Consider using a secrets management service

## Troubleshooting

### Common Issues

1. **Missing Variables**
   ```bash
   # Check if variable is set
   echo $VARIABLE_NAME
   
   # Check .env file
   cat .env | grep VARIABLE_NAME
   ```

2. **Invalid Values**
   ```bash
   # Run validation script
   ./scripts/validate-env.sh
   ```

3. **Connection Issues**
   ```bash
   # Test MongoDB connection
   mongosh "$MONGODB_URI" --eval "db.serverStatus()"
   
   # Test Redis connection
   redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping
   ```

### Getting Help

1. Check the logs:
   ```bash
   tail -f logs/app.log
   ```

2. Enable debug mode:
   ```bash
   export LOG_LEVEL=debug
   ```

3. Contact the development team for support.

## Best Practices

1. **Version Control**
   - Never commit `.env` files
   - Keep `.env.example` updated
   - Document all new variables

2. **Security**
   - Use strong passwords
   - Rotate secrets regularly
   - Follow principle of least privilege

3. **Maintenance**
   - Review configurations regularly
   - Update dependencies
   - Monitor for security updates

4. **Documentation**
   - Document all environment variables
   - Keep setup instructions updated
   - Document troubleshooting steps

## Additional Resources

- [MongoDB Documentation](https://docs.mongodb.com/)
- [Redis Documentation](https://redis.io/documentation)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [SendGrid Documentation](https://docs.sendgrid.com/)
- [JWT Best Practices](https://auth0.com/blog/jwt-security-best-practices/) 