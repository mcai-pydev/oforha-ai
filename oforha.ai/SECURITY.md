# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability within Oforha.ai, please send an email to mcofora@gmail.com. All security vulnerabilities will be promptly addressed.

## Security Measures

1. **Content Security Policy (CSP)**
   - Strict CSP headers to prevent XSS attacks
   - Frame protection against clickjacking
   - Protection against MIME type sniffing

2. **HTTPS Enforcement**
   - All traffic is forced over HTTPS
   - HSTS is enabled
   - Modern TLS protocols only

3. **Access Controls**
   - Limited permissions for external resources
   - Strict origin policies
   - Controlled API access

4. **Data Protection**
   - No sensitive data storage in client-side code
   - Secure handling of user inputs
   - Regular security audits

## Version Support

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Updates

Security updates are published in our GitHub repository and announced through our official channels. 