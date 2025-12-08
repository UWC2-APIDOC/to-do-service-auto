---
# markdownlint-disable
# vale  off
layout: default
parent: user resource
nav_order: 1
# tags used by AI files
description: Patch `userId` using JSON array of resource properties
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
    - PATCH /users/{userId}
version: "v1.0"
last_updated: "2025-11-03"
# vale  on
# markdownlint-enable
---

# Patch user

Returns the [`user`](user.md) object with modified resource parameters.

## URL

```shell
{server_url}/users/{userId}
```

## Example CURL command

```shell
curl -X PATCH https://localhost:3000/users/1 \
    -H "Content-Type: application/json" 
    -d '{"lastName": "Ferdinand", "firstName": "Franz", "email": "f.ferdinand@example.com"}'
```

## Path Parameters

| Parameter | Type | Description | Required |
|:-|:-|:-|:-|
| `userId` | `integer` | User's ID | yes |

## Request headers

None

## Request body

Sample request body

```json
{
    "lastName": "Ferdinand",
    "firstName": "Franz",
    "email": "f.ferdinand@example.com"
}
```

| Property name | Type | Description |
|:-|:-|:-|
| `lastName` | `string` | User's last name |
| `firstName` | `string` | User's first name |
| `email` | `string` | User's email address |

## Return body

```json
{
    "lastName": "Ferdinand",
    "firstName": "Franz",
    "email": "f.ferdinand@example.com",
    "id": 1
}
```

| Property name | Type | Description | Required |
|:-|:-|:-|:-|
| `email` | `string` | User's email address | no |
| `firstName` | `string` | User's first name | no |
| `id` | `integer` | User's ID | no |
| `lastName` | `string` | User's last name | no |

## Return status

| Status value | Return status | Description |
|:-|:-|:-|
| `200` | `OK` | Request successful. The server has responded as required. |
| `404` | `Not Found` | Requested resource not found. Check your URL path parameters and try again. |
| `ECONNREFUSED` | `Error` | Couldn't send request. Start the service and try again. |
