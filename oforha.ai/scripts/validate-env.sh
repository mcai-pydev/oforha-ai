#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a variable is set
check_required() {
    local var=$1
    local value=${!var}
    if [ -z "$value" ] || [ "$value" = "your_*" ]; then
        echo -e "${RED}❌ $var is not set${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $var is set${NC}"
        return 0
    fi
}

# Function to validate URL format
validate_url() {
    local var=$1
    local value=${!var}
    if [[ $value =~ ^https?:// ]]; then
        echo -e "${GREEN}✓ $var has valid URL format${NC}"
        return 0
    else
        echo -e "${RED}❌ $var has invalid URL format${NC}"
        return 1
    fi
}

# Function to validate number range
validate_number_range() {
    local var=$1
    local value=${!var}
    local min=$2
    local max=$3
    if [[ $value =~ ^[0-9]+$ ]] && [ "$value" -ge "$min" ] && [ "$value" -le "$max" ]; then
        echo -e "${GREEN}✓ $var is within valid range ($min-$max)${NC}"
        return 0
    else
        echo -e "${RED}❌ $var is not within valid range ($min-$max)${NC}"
        return 1
    fi
}

# Function to validate boolean
validate_boolean() {
    local var=$1
    local value=${!var}
    if [[ $value =~ ^(true|false)$ ]]; then
        echo -e "${GREEN}✓ $var has valid boolean value${NC}"
        return 0
    else
        echo -e "${RED}❌ $var has invalid boolean value${NC}"
        return 1
    fi
}

# Function to validate file exists
validate_file_exists() {
    local var=$1
    local value=${!var}
    if [ -f "$value" ]; then
        echo -e "${GREEN}✓ File $value exists${NC}"
        return 0
    else
        echo -e "${RED}❌ File $value does not exist${NC}"
        return 1
    fi
}

# Function to validate directory exists
validate_directory_exists() {
    local var=$1
    local value=${!var}
    if [ -d "$value" ]; then
        echo -e "${GREEN}✓ Directory $value exists${NC}"
        return 0
    else
        echo -e "${RED}❌ Directory $value does not exist${NC}"
        return 1
    fi
}

# Main validation function
validate_environment() {
    local errors=0
    echo -e "${YELLOW}Validating environment variables...${NC}\n"

    # Required variables
    echo -e "${YELLOW}Checking required variables...${NC}"
    check_required "MONGODB_URI" || ((errors++))
    check_required "REDIS_HOST" || ((errors++))
    check_required "OPENAI_API_KEY" || ((errors++))
    check_required "JWT_SECRET" || ((errors++))
    check_required "SENDGRID_API_KEY" || ((errors++))
    check_required "AI_SERVICE_API_KEY" || ((errors++))

    # URL validations
    echo -e "\n${YELLOW}Validating URLs...${NC}"
    validate_url "AI_SERVICE_URL" || ((errors++))
    validate_url "CORS_ORIGIN" || ((errors++))

    # Number range validations
    echo -e "\n${YELLOW}Validating numeric ranges...${NC}"
    validate_number_range "PORT" 1 65535 || ((errors++))
    validate_number_range "MAX_CONNECTIONS" 1 1000 || ((errors++))
    validate_number_range "WORKER_THREADS" 1 16 || ((errors++))

    # Boolean validations
    echo -e "\n${YELLOW}Validating boolean values...${NC}"
    validate_boolean "ENABLE_HTTPS" || ((errors++))
    validate_boolean "ENABLE_METRICS" || ((errors++))
    validate_boolean "ENABLE_AI_CHAT" || ((errors++))

    # File validations
    echo -e "\n${YELLOW}Validating file paths...${NC}"
    if [ "$ENABLE_HTTPS" = "true" ]; then
        validate_file_exists "SSL_CERT_PATH" || ((errors++))
        validate_file_exists "SSL_KEY_PATH" || ((errors++))
    fi

    # Directory validations
    echo -e "\n${YELLOW}Validating directory paths...${NC}"
    validate_directory_exists "COURSE_STORAGE_PATH" || ((errors++))
    validate_directory_exists "BACKUP_PATH" || ((errors++))

    # MongoDB connection test
    echo -e "\n${YELLOW}Testing MongoDB connection...${NC}"
    if mongosh "$MONGODB_URI" --eval "db.serverStatus()" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ MongoDB connection successful${NC}"
    else
        echo -e "${RED}❌ MongoDB connection failed${NC}"
        ((errors++))
    fi

    # Redis connection test
    echo -e "\n${YELLOW}Testing Redis connection...${NC}"
    if redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Redis connection successful${NC}"
    else
        echo -e "${RED}❌ Redis connection failed${NC}"
        ((errors++))
    fi

    # Print summary
    echo -e "\n${YELLOW}Validation Summary:${NC}"
    if [ $errors -eq 0 ]; then
        echo -e "${GREEN}✓ All validations passed!${NC}"
    else
        echo -e "${RED}❌ Found $errors validation errors${NC}"
        exit 1
    fi
}

# Run validation
validate_environment 