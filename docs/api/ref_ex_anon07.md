---
# markdownlint-disable
# vale  off
layout: default
# nav_order: 1
parent: user resource
# tags used by AI files
description: POST new user resources
tags:
    - overview
categories: 
    - overview
ai_relevance: high
importance: 6
prerequisites: []
related_pages: []
examples: []
api_endpoints:
version: "v1.0"
last_updated: "2025-11-15"
# vale  on
# markdownlint-enable
---

# POST /users

Creates a new user account.

## Endpoint

```text
POST /api/v1/users
```

**Authentication:** Required (token)  
**Permissions:** `users:create` or `admin`

## Request Body

```json
{
  "email": "jane.smith@example.com",
  "firstName": "Jane",
  "lastName": "Smith"
}
```

### Required Fields

- `email` - Valid email address (must be unique)
- `firstName` - 1-50 characters
- `lastName` - 1-50 characters

## Response

### Success (201 Created)

```json
{
  "id": "usr_7k2m9p4q8r",
  "firstName": "Jane",
  "lastName": "Smith",
  "email": "jane.smith@example.com"
}
```

### Common Errors

| Code | Reason |
|------|--------|
| 400 | Invalid request (validation failed) |
| 401 | Missing or invalid authentication |
| 403 | Insufficient permissions |
| 409 | Email or username already exists |

## Example

```bash
curl -X POST https://api.example.com/api/v1/users \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.smith@example.com",
    "firstName": "Jane",
    "lastName": "Smith"
  }'
```

## Notes

- Verification email sent automatically upon creation
- Rate limit: 100 requests/hour
