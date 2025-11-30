---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
parent: user resource
nav_order: 1
# tags used by AI files
description: GET all `user` resources from the service
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

<!-- vale Vale.Terms = NO -->
<!-- vale Google.Passive = NO -->
<!-- vale Google.Headings = NO -->

# Get all users

Returns an array of [`user`](user.md) objects that contains all users that have registered with the service.

## URL

```shell

{server_url}/users
```

## Parameters

None

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
    },
    {
        "lastName": "Jones",
        "firstName": "Jillio",
        "email": "jlo.jones@example.com",
        "id": 2
    }
    ...
]
```

## Return status

| Status value | Return status | Description |
| ------------- | ----------- | ----------- |
| 200 | Success | Requested data returned successfully |
| ECONNREFUSED | N/A | Service is offline. Start the service and try again. |
