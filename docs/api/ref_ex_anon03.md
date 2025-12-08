---
# markdownlint-disable
# vale  off
layout: default
# nav_order: 1
parent: task resource
# tags used by AI files
description: Get Tasks reference topic
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
last_updated: "2025-11-14"
# vale  on
# markdownlint-enable
---

# `Get /tasks`

**Return the full list of tasks in the system.**

## URL

`http://localhost:3000/tasks` or `{server_url/tasks}`

## Description

This endpoint will:

- Show all tasks logged in the system.
  
- Display task lists in the console.
  
- Return task data in the console.

## Return status

| Status Value | Return | Description |
| ------------ | ------ | ----------- |
| 200 | Success | Data returned successfully |
| 404 | Unsuccessful | Specified not found |
| ECONNREFUSED | N/A | Service Offline / Restart Needed |

## Related topics

- [Get task by ID](./get-task-by-taskid-lauren-march.md)
- [task resource](./task.md)
