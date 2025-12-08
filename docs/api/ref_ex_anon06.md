---
# markdownlint-disable
# vale  off
layout: default
parent: task resource
nav_order: 1
# tags used by AI files
description: Post `task` resource to the service
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
    - POST /tasks
version: "v1.0"
last_updated: "2025-09-03"
# vale  on
# markdownlint-enable
---

# Post task

Post new task to the service.

## URL

```shell
{server_url}/tasks
```

## Parameters

None

## Request headers

None

## Request body

```json
{
    "userId": 1,
    "title": "New task 1",
    "description": "an urgent task",
    "dueDate": "2026-02-21T17:00",
    "warning": "10"
}
```

## Return body

Returns the new task

```json
{
    "userId": 1,
    "title": "New task 1",
    "description": "an urgent task",
    "dueDate": "2026-02-21T17:00",
    "warning": "10",
    "id": 5
}
```

## Return status

| Status value | Return status | Description |
| ------------- | ----------- | ----------- |
| 201 | Success | New task resource added successfully |
| 404 | Error | Requested data not posted successfully |
|  ECONNREFUSED | N/A | Service is offline. Start the service and try again. |

## Related topics

[task resource](./task.md)
