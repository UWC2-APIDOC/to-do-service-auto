---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
parent: user resource
nav_order: 2
# tags used by AI files
description: GET the `user` resource with the specified ID from the service
topic_type: reference
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
last_updated: "2026-03-01"
# vale  on
# markdownlint-enable
---

# Get a user by ID

<!-- vale Google.Passive = NO -->
<!-- vale Google.Headings = NO -->

Returns an array of  [`user`](user.md) resources that match
the user specified by the `id` parameter, if one exists.

## URL

```shell

{server_url}/users/{id}
```

## Parameters

| Parameter name | Type | Description |
| -------------- | ------ | ------------ |
| `id` | number | The record ID of the user to return |

## Request headers

None

## Request body

None

## Return body

```js
[
    {
        "lastName": "Smith",
        "firstName": "Ferdinand",
        "email": "f.smith@example.com",
        "id": 1
    }
]
```

## Return status

| Status value | Return status | Description |
| ------------- | ----------- | ----------- |
| 200 | Success | Requested data returned successfully |
| 404 | Error | Specified user record not found |
| ECONNREFUSED | N/A | Service is offline. Start the service and try again. |
