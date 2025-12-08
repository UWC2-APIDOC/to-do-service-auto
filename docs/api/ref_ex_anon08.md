---
# markdownlint-disable
# vale  off
layout: default
# nav_order: 1
parent: user resource
# tags used by AI files
description: Alternate overview topic
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
last_updated: "2025-11-13"
# vale  on
# markdownlint-enable
---

# Using PUT /users/{userId}

This operation uses the HTTP PUT method to update an existing user’s details in the To-Do Service.

---

## Overview

Use this operation to update the details of an existing user account.
Specify the user’s unique `userId`. Only include the fields you want to update.
Any omitted fields remain unchanged.

This endpoint is typically used by administrators or by users updating their own profiles.

**Base path:**  
`https://api.todo-service.com/v1`

---

## Request

### HTTP method and endpoint

`PUT /users/{userId}`

### Required authorization

This operation requires a valid Bearer token with the `users.write` permission scope.

### Path parameter

| Name     | Type   | Required | Description                                |
|----------|--------|----------|--------------------------------------------|
| `userId` | string | Yes      | Unique identifier of the user to update.   |

### Request headers

| Header         | Required | Description                      |
|----------------|----------|----------------------------------|
| `Authorization`| Yes      | Bearer token for authentication. |
| `Content-Type` | Yes      | Must be `application/json`.      |

### Request body

<!-- markdownlint-disable MD013 -->

| Property   | Type       | Required | Description                                                    |
|------------|-----------|----------|-----------------------------------------------------------------|
| `name`     | string    | No       | The user’s full name.                                           |
| `email`    | string    | No       | The user’s email address. Must be unique and valid format.      |
| `role`     | string    | No       | The user’s role (`admin`, `member`, `viewer`).                  |
| `isActive` | `boolean` | No       | Indicates whether the user account is active: true or false.    |

<!-- markdownlint-enable MD013 -->

#### Example CURL request

```bash
curl -X PUT "https://api.todo-service.com/v1/users/12345" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
        "name": "Drashti Bhatt",
        "email": "drashti@example.com",
        "role": "member",
        "isActive": true
      }'
```

### Response

If successful, the API returns the updated user object.

#### Example response body

```json
{
  "id": "12345",
  "name": "Drashti Bhatt",
  "email": "drashti@example.com",
  "role": "member",
  "isActive": true,
  "updatedAt": "2025-10-31T14:22:00Z"
}
```

## Response properties

<!-- markdownlint-disable MD013 -->

| Property    | Type                   | Description                                               |
|------------|-----------------------|-------------------------------------------------------------|
| `id`       | string                | The user’s unique ID.                                       |
| `name`     | string                | Updated name of the user.                                   |
| `email`    | string                | Updated email of the user.                                  |
| `role`     | string                | Updated role within the service.                            |
| `isActive` | `boolean`             | Indicates whether the account is active.                    |
| `updatedAt`| `string` (ISO 8601, date-time format) | Timestamp showing when the system last modified the user record. |

---

## Status codes

| Code | Meaning                   | Description                                                     |
|------|---------------------------|-----------------------------------------------------------------|
| 200  | 200 OK                    | Success—the user record was updated successfully.               |
| 400  | 400 bad request           | Client error—the request body contains invalid or missing data. |
| 401  | 401 unauthorized          | Authentication error—missing or invalid credentials/token.      |
| 403  | 403 forbidden             | Permission error—token lacks required scope or permission denied. |
| 404  | 404 not found             | Not found—no user exists with the specified `userId`.           |
| 409  | 409 conflict              | Conflict—update violates a uniqueness constraint.               |
| 500  | 500 internal server error | Server error—an unexpected server-side error occurred.          |

<!-- markdownlint-enable MD013 -->

## Error response examples

### 400 Bad request

```json
{
  "error": {
    "code": 400,
    "message": "Invalid email format provided."
  }
}
```

### 401 unauthorized

```json
{
  "error": {
    "code": 401,
    "message": "Authentication required."
  }
}
```

### 403 forbidden

```json
{
  "error": {
    "code": 403,
    "message": "Insufficient permission to update this user."
  }
}
```

### 404 not found

```json
{
  "error": {
    "code": 404,
    "message": "User not found."
  }
}
```

### 409 conflict

```json
{
  "error": {
    "code": 409,
    "message": "Email address already in use."
  }
}
```

## Related topics

Read [GET /users/{userId}](./users-get-user-by-id.md) to retrieve a user by ID.
