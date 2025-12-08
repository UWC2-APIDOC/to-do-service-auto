---
# markdownlint-disable
# vale  off
layout: default
parent: task resource
nav_order: 1
# tags used by AI files
description: DELETE the `task` resource with the specified ID from the service
tags:
    - api
categories:
    - api-reference
ai_relevance: high
importance: 7
prerequisites: 
    - /api/task
related_pages: []
examples: []
api_endpoints: 
    - DELETE /tasks/{id}
version: "v1.0"
last_updated: "2025-10-27"
# vale  on
# markdownlint-enable
---

# Delete a task by ID

This action deletes a [`task`](task.md) specified by the `id` parameter of the `task` resource.

## URL

```shell

{server_url}/tasks/{id}
```

## Parameters

| Parameter name | Type | Description |
| -------------- | ------ | ------------ |
| `id` | number | ID of the task that you want to delete |

## Request information

You don't have to specify the header information and this request has no request body.

This call also doesn't return anything, no matter if the call is successful or not.
To verify that the deletion was successful, check the task list again.
Another option is to run a GET call with this ´id´ to make sure that it doesn't exist anymore.

## Example

```js

curl -X DELETE http://localhost:3000/tasks/5
```

## Return status

| Status value | Return status | Description |
| ------------- | ----------- | ----------- |
| 200 | Success | Requested data returned successfully |
| 404 | Error | Specified user record not found |
|  ECONNREFUSED | N/A | Service is offline. Start the service and try again. |
