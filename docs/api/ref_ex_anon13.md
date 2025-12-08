---
# markdownlint-disable
# vale  off
layout: default
parent: user resource
nav_order: 2
# tags used by AI files
description: Use this endpoint to GET the `user` by their first name
tags:
    - api
categories:
    - api-reference
ai_relevance: high
importance: 7
prerequisites: 
    - /api/user
related_pages: []
examples: []
api_endpoints: 
    - GET /users
version: "v1.0"
last_updated: "2025-09-03"
# vale  on
# markdownlint-enable
---

# Get a user by first name

Use the /users endpoint to GET a [`user`](user.md) by their first name, if the first name exists.

## URL

```shell

{server_url}/users?firstame={firstame}
```

## Query parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `firstName` | string | Yes | The first name of the user to search for |

## Request headers

None

## Request body

None

## Request syntax

```bash
curl http://localhost:3000/users?firstName={firstName}
```

## Response format

| Property name | Type | Description |
| ------------- | ----------- | ----------- |
| `lastName` | string | The user's last name |
| `firstName` | string | The user's first name |
| `email` | string | The user's email address |
| `id` | number | The user's unique record ID |

## Request example

```bash
curl http://localhost:3000/users?firstName=Jill
```

## Response example

```json
[
  {
    "lastName": "Jones",
    "firstName": "Jill",
    "email": "j.jones@example.com",
    "id": 2
  }
]
```

## Return status

| Status value | Return status | Description |
| ------------- | ----------- | ----------- |
| 200 | Success | Requested data returned successfully |
| 404 | Error | Specified user record not found |
|  ECONNREFUSED | N/A | Service is offline. Start the service and try again. |
