# Security Policy

## Supported Versions

We actively support and patch the following versions of **CreditGuard AI**:

| Version | Supported |
| ------- | --------- |
| 2.0.x   | Yes       |
| 1.0.x   | No        |

---

## Reporting a Vulnerability

We take the security of our predictive services and applicant data seriously. If you find a security vulnerability, please report it via the following process:

1. **Do not open a public GitHub issue**.
2. Email your findings to **security-alert@creditguard-ai.com** *(mock contact)*.
3. Include:
   - Detailed description of the exploit vector.
   - Step-by-step instructions to reproduce the issue.
   - Potential impact metrics (data leaks, privilege escalation, server denial of service).
4. Our core team will acknowledge receipt of the report within 24 hours and provide weekly updates until a patch is released.

---

## Security Safeguards Implemented
- **Password Protection**: BCrypt/Scrypt key derivation prevents raw database password storage.
- **Session Protections**: Secure HTTPOnly flags block Cross-Site Scripting (XSS) cookie extraction.
- **CSRF Safeguards**: Cryptographic tokens protect all state-modifying requests from forgery.
- **Rate Limiting**: Custom middleware controls request volume to prediction endpoints.
