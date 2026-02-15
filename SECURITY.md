# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Simulacra, please report it by:

1. **Do NOT** open a public GitHub issue
2. Email the maintainers directly with details
3. Include steps to reproduce the vulnerability
4. Allow reasonable time for a fix before public disclosure

## Security Best Practices

### API Key Management

#### ✅ DO:

- Store API keys in `.env` files (excluded from git)
- Use environment variables for all sensitive configuration
- Generate new API keys if you suspect compromise
- Rotate API keys periodically
- Use different API keys for development and production
- Set appropriate API key restrictions in Google Cloud Console

#### ❌ DON'T:

- Commit API keys to version control
- Share API keys in chat, email, or documentation
- Use the same API key across multiple projects
- Store API keys in code or configuration files tracked by git
- Use example API keys from documentation in production

### Environment Variables

#### Required Variables:

- `GOOGLE_API_KEY`: Your Google Gemini API key (required for LLM calls)
- `GOOGLE_API_MODEL`: Model name (default: gemini-2.0-flash-exp)

#### Optional Variables:

- `BACKEND_HOST`: Backend server host (default: 127.0.0.1)
- `BACKEND_PORT`: Backend server port (default: 8000)
- `CORS_ORIGINS`: Comma-separated allowed CORS origins
- `VITE_API_BASE`: Frontend API base URL (optional)

### CORS Configuration

The backend uses CORS middleware to control which origins can access the API.

#### Default Configuration:

```python
CORS_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"
```

#### Production Configuration:

Set `CORS_ORIGINS` environment variable to your production frontend URL:

```bash
CORS_ORIGINS=https://yourdomain.com
```

#### Security Considerations:

- Never use `*` (wildcard) for CORS origins in production
- Only allow specific, trusted origins
- Use HTTPS in production
- Enable credentials only if needed

### File Security

#### Files That Should NEVER Be Committed:

- `.env` - Contains sensitive environment variables
- `.env.local` - Local environment overrides
- `*.key` - Private keys
- `*.pem` - Certificates
- `credentials.json` - Service account credentials

#### Verify .gitignore:

Ensure your `.gitignore` includes:

```
.env
.env.local
.env.*.local
*.key
*.pem
credentials.json
```

### Dependency Security

#### Keep Dependencies Updated:

```bash
# Backend
uv sync --upgrade

# Frontend
npm update
npm audit fix
```

#### Check for Vulnerabilities:

```bash
# Backend
pip-audit  # Install with: pip install pip-audit

# Frontend
npm audit
```

### Network Security

#### Development:

- Backend runs on `127.0.0.1:8000` (localhost only)
- Frontend runs on `localhost:3000`
- Not accessible from external networks

#### Production:

- Use HTTPS for all connections
- Use a reverse proxy (nginx, Caddy)
- Enable rate limiting
- Use firewall rules to restrict access
- Consider using a VPN for admin access

### Error Handling Security

#### ✅ DO:

- Return generic error messages to users
- Log detailed errors server-side only
- Use appropriate HTTP status codes
- Return JSON errors (not HTML)

#### ❌ DON'T:

- Expose stack traces to users
- Include sensitive data in error messages
- Return database errors directly
- Expose internal system details

### Code Security

#### Input Validation:

- Validate all user inputs
- Use Pydantic models for type safety
- Sanitize inputs before processing
- Limit input sizes

#### Output Encoding:

- Escape HTML in user-generated content
- Use parameterized queries (if using database)
- Validate data before rendering

## Incident Response

If you discover that an API key has been compromised:

1. **Immediately revoke the key** in Google Cloud Console
2. **Generate a new key** and update your `.env` file
3. **Review access logs** to understand the scope of compromise
4. **Rotate any other credentials** that may have been exposed
5. **Update your security practices** to prevent future incidents

## Security Checklist for Deployment

- [ ] All API keys are stored in environment variables
- [ ] `.env` file is in `.gitignore`
- [ ] No credentials in source code
- [ ] CORS origins are properly configured
- [ ] HTTPS is enabled
- [ ] Dependencies are up to date
- [ ] Security headers are configured
- [ ] Rate limiting is enabled
- [ ] Logging is configured
- [ ] Error messages don't expose sensitive data
- [ ] Input validation is implemented
- [ ] API key restrictions are set in Google Cloud Console

## Additional Resources

- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [React Security Best Practices](https://react.dev/learn/security)

## Contact

For security concerns, please contact the maintainers directly rather than opening public issues.
