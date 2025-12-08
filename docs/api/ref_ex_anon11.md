---
# markdownlint-disable
# vale  off
layout: default
parent: task resource
nav_order: 3
# tags used by AI files
description: "GET all `task` resources for a specified `userId` from the service"
tags:
    - api
categories:
    - api-reference
ai_relevance: high
importance: 7
prerequisites:
    - /api/task
    - /api/user
related_pages: []
examples: []
api_endpoints:
    - GET /tasks
version: "v1.0"
last_updated: "2025-09-03"
# vale  on
# markdownlint-enable
---

# Get tasks by user ID

Returns an array of [`task`](task.md) objects assigned to the specified `userId`.
The service returns an empty array if no tasks exist for the user.

## URL

```shell
{server_url}/tasks?userId={id}
```

## Query parameters

| Parameter name | Type    | Description                               |
| :------------- | :------ | :---------------------------------------- |
| `userId`       | integer | The unique `id` of the user whose tasks to retrieve. |

## Request headers

None

## Request body

None

## Return body

The following example shows the response for a request where `userId` is `1`.

```json
[
    {
      "userId": 1,
      "title": "Grocery shopping",
      "description": "eggs, bacon, gummy bears",
      "dueDate": "2025-09-20T17:00",
      "warning": "10",
      "id": 1
    },
    {
      "userId": 1,
      "title": "Piano recital",
      "description": "Daughter's first concert appearance",
      "dueDate": "2025-10-02T15:00",
      "warning": "30",
      "id": 2
    }
]
```

## Return status

| Status value | Return status | Description                                          |
| :----------- | :------------ | :--------------------------------------------------- |
| 200          | Success       | Requested data returned successfully.                |
| 404          | Not Found     | The specified `userId` doesn't exist.               |
| ECONNREFUSED | N/A           | Service is offline. Start the service and try again. |
