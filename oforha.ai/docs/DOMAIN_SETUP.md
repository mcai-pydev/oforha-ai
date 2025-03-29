# Domain Setup Guide

## 1. Domain Registration

### oforha.com
1. Log in to Hostinger control panel
2. Go to "Domains" section
3. Click "Register Domain"
4. Enter "oforha.com"
5. Select registration period (4 years recommended)
6. Complete registration process

### oforha.ai
1. Log in to Hostinger control panel
2. Go to "Domains" section
3. Click "Register Domain"
4. Enter "oforha.ai"
5. Select registration period (4 years recommended)
6. Complete registration process

## 2. Hosting Configuration

### Main Domain (oforha.com)
1. Go to "Hosting" section
2. Select Business Plan
3. Choose 4-year commitment
4. Configure hosting settings:
   - PHP version: 8.1+
   - Node.js version: 18+
   - Enable SSH access
   - Enable Git version control

### Additional Domain (oforha.ai)
1. Go to "Hosting" section
2. Click "Add Domain"
3. Enter "oforha.ai"
4. Configure as addon domain
5. Set up subdomain structure:
   - www.oforha.ai
   - api.oforha.ai
   - learn.oforha.ai

## 3. SSL Configuration

### oforha.com
1. Go to "SSL/TLS" section
2. Select "Let's Encrypt SSL"
3. Choose "Wildcard SSL" option
4. Install SSL certificate
5. Configure automatic renewal

### oforha.ai
1. Go to "SSL/TLS" section
2. Select "Let's Encrypt SSL"
3. Choose "Wildcard SSL" option
4. Install SSL certificate
5. Configure automatic renewal

## 4. DNS Configuration

### oforha.com
```
Type    Name    Value
A       @       [Hostinger IP]
CNAME   www     @
A       api     [Hostinger IP]
A       learn   [Hostinger IP]
```

### oforha.ai
```
Type    Name    Value
A       @       [Hostinger IP]
CNAME   www     @
A       api     [Hostinger IP]
A       learn   [Hostinger IP]
```

## 5. Email Setup

### oforha.com
1. Go to "Email" section
2. Create email accounts:
   - admin@oforha.com
   - support@oforha.com
   - info@oforha.com
3. Configure email clients
4. Set up SPF records

### oforha.ai
1. Go to "Email" section
2. Create email accounts:
   - admin@oforha.ai
   - support@oforha.ai
   - info@oforha.ai
3. Configure email clients
4. Set up SPF records

## 6. Performance Optimization

### CDN Setup
1. Enable Hostinger CDN
2. Configure cache settings
3. Set up cache exclusions
4. Enable GZIP compression

### Database Optimization
1. Enable Redis cache
2. Configure query cache
3. Set up database backups
4. Optimize database settings

## 7. Security Configuration

### Firewall Rules
1. Enable ModSecurity
2. Configure WAF rules
3. Set up IP blocking
4. Enable DDoS protection

### Backup Strategy
1. Configure daily backups
2. Set up remote backup storage
3. Enable backup encryption
4. Test backup restoration

## 8. Monitoring Setup

### Resource Monitoring
1. Enable server monitoring
2. Set up resource alerts
3. Configure performance tracking
4. Enable error logging

### Uptime Monitoring
1. Set up uptime checks
2. Configure alert notifications
3. Enable status page
4. Set up incident reporting

## 9. Development Environment

### Git Setup
1. Enable Git version control
2. Configure deployment hooks
3. Set up staging environment
4. Enable CI/CD integration

### SSH Access
1. Generate SSH keys
2. Configure SSH access
3. Set up SFTP access
4. Enable SSH tunneling

## 10. Maintenance Plan

### Regular Tasks
1. Weekly security updates
2. Monthly performance review
3. Quarterly backup testing
4. Annual SSL renewal

### Emergency Procedures
1. Server failure response
2. DDoS attack handling
3. Data recovery process
4. Incident communication plan 