#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up environment variables for Oforha.ai${NC}\n"

# Check if .env file exists
if [ -f .env ]; then
    echo -e "${RED}Warning: .env file already exists. This will overwrite it.${NC}"
    read -p "Do you want to continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Setup cancelled.${NC}"
        exit 1
    fi
fi

# Create .env file
cp .env.example .env

# Function to prompt for sensitive values
prompt_for_value() {
    local key=$1
    local description=$2
    local current_value=$(grep "^$key=" .env | cut -d '=' -f2)
    
    echo -e "${YELLOW}$description${NC}"
    if [ ! -z "$current_value" ] && [ "$current_value" != "your_*" ]; then
        echo -e "Current value: $current_value"
        read -p "Keep current value? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    
    read -p "Enter new value: " value
    sed -i "s|^$key=.*|$key=$value|" .env
}

# Prompt for sensitive values
echo -e "${GREEN}Please enter the following values:${NC}\n"

# MongoDB
prompt_for_value "MONGODB_USER" "MongoDB username"
prompt_for_value "MONGODB_PASSWORD" "MongoDB password"

# Redis
prompt_for_value "REDIS_PASSWORD" "Redis password"

# OpenAI
prompt_for_value "OPENAI_API_KEY" "OpenAI API key"

# JWT
prompt_for_value "JWT_SECRET" "JWT secret (generate a secure random string)"

# SendGrid
prompt_for_value "SENDGRID_API_KEY" "SendGrid API key"

# AI Service
prompt_for_value "AI_SERVICE_API_KEY" "AI Service API key"

# External Services
prompt_for_value "GITHUB_API_KEY" "GitHub API key"
prompt_for_value "LINKEDIN_API_KEY" "LinkedIn API key"
prompt_for_value "TWITTER_API_KEY" "Twitter API key"

# Generate secure random values for other sensitive fields
echo -e "\n${GREEN}Generating secure random values...${NC}"

# Generate a secure random string for JWT if not set
if grep -q "^JWT_SECRET=your_jwt_secret" .env; then
    JWT_SECRET=$(openssl rand -base64 32)
    sed -i "s|^JWT_SECRET=.*|JWT_SECRET=$JWT_SECRET|" .env
fi

# Set development-specific values
if [ "$NODE_ENV" = "development" ]; then
    sed -i 's|^ENABLE_HTTPS=.*|ENABLE_HTTPS=false|' .env
    sed -i 's|^LOG_LEVEL=.*|LOG_LEVEL=debug|' .env
    sed -i 's|^ENABLE_DEBUG_TOOLS=.*|ENABLE_DEBUG_TOOLS=true|' .env
fi

echo -e "\n${GREEN}Environment setup complete!${NC}"
echo -e "${YELLOW}Please review the .env file and make any additional adjustments.${NC}"
echo -e "${YELLOW}Remember to never commit the .env file to version control.${NC}" 