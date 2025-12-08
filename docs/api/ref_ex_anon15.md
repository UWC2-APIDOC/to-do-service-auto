---
# markdownlint-disable
# vale  off
layout: default
parent: user resource
nav_order: 1
# tags used by AI files
description: DELETE the `user` resource with the specified ID from the service
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
    - DELETE /users/{userId}
version: "v1.0"
last_updated: "2025-10-27"
# vale  on
# markdownlint-enable
---

# Delete a user by ID

DELETE
{: .label .label-red }
{: .d-inline-block }

`{base_url}/users/{id}`
{: .d-inline-block }

Deletes the [`user`](user.md) object with the specified `userId` parameter, if it exists.

## Requirements

| Type           | Description          |
| -------------- | -------------------- |
| Authentication | Access token         |
| Permission     | Write                |

## Request parameters

| Parameter      | Format | Description                                |
| -------------- | ------ | ------------------------------------------ |
| `base_url`     | string | The server address `http://localhost:3000` |
| `userId`       | number | The record ID of the user to delete        |

### Headers

_None_

### Body

_None_

## Example request

```js
curl -X DELETE http://localhost:3000/users/4
```

## Example response

{: .d-inline-block }

200
{: .label .label-green }

```js
{}
```

### Response status codes

| Status code   | Description          |
| ------------- | -------------------- |
| 200           | Success              |
| 404           | User not found       |
| ECONNREFUSED  | Restart the service  |
