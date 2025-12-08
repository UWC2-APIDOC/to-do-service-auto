---
# markdownlint-disable
# vale  off
layout: default
# nav_order: 1
parent: user resource
# tags used by AI files
description: Get User resource by ID reference topic
topic_type: reference
tags:
    - overview
categories: 
    - overview
ai_relevance: high
importance: 6
prerequisites: []
related_pages: []
examples:
    - GET /users/id
test:
    test_apps:
        - json-server@0.17.4
    server_url: localhost:3000
    local_database: /api/to-do-db-source.json
    testable:
        - GET user by id example
api_endpoints:
  - /users
version: "v1.0"
last_updated: "2025-11-02"
# vale  on
# markdownlint-enable
---

# `GET /users/{id}`

Retrieves a single user by their unique identifier.

## Endpoint

`GET /users/{id}`

## Description

Use this operation to fetch details for a specific user.
This is useful when displaying a profile or managing user-specific data.

## Path parameters

| Parameter | Type | Required | Description |
| ---------- | ------ | ---------- | ------------- |
| `id` | integer | Yes | Unique identifier for the user. |

## Response properties

| Property | Type | Description |
| --------- | ------ | ------------- |
| `firstName` | string | The user’s given name. |
| `lastName` | string | The user’s last name. |
| `email` | string | Contact email for the user. |
| `id` | integer | Unique identifier for the user. |

## `GET user` by `id` example

This example gets a specific user resource.

### `GET user` by `id` example request

```shell
curl http://localhost:3000/users/2
```

### `GET user` by `id` example response

```json
{
  "lastName": "Jones",
  "firstName": "Jill",
  "email": "j.jones@example.com",
  "id": 2
}
```

## Related operations

* [`task` resource](./task.md)
* [`user` resource](./user.md)
