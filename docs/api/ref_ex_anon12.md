---
# markdownlint-disable
# vale  off
layout: default
nav_order: 4
parent: task resource
has_children: false
has_toc: false
# tags used by AI files
description: "Information about PUT a task in the `task` resource"
tags: 
    - api
categories: 
    - api-reference
ai_relevance: high
importance: 8
prerequisites: []
related_pages: 
 examples: []
api_endpoints:
    - /tasks
version: "v1.0"
last_updated: "2025-10-27"
# vale  on
# markdownlint-enable
---

# `task` resource - PUT task

Base endpoint:

```shell
http://localhost:3000/tasks/
```

This endpoint can be used to update an existing task on the To-Do Service API.

In some cases if the resource does not already exist, the API will create a new task.

For this example, we are focusing on the update case.

To have a task in the service, the user must be added to
the service first. Learn more about the [user resource](user.md).

## Resource properties

Sample `task` resource

```json

{
    "userId": 1,
    "title": "Grocery shopping",
    "description": "eggs, bacon, gummy bears",
    "dueDate": "2025-02-20T17:00",
    "warning": "10",
    "id": 1
}
```

| Property name | Type | Description |
| ------------- | ----------- | ----------- |
| `userId` | number | The ID of the user resource to which this task is assigned |
| `title` | string | The title or short description of the task |
| `description` | string | The long description of the task|
| `dueDate` | string | The ISO 8601 format of the date and time the task is due |
| `warning` | number | The number of minutes before the `dueDate` to alert the user of the task |
| `id` | number | The unique record ID of the task |

## Example

Using PostMan, select the `PUT` operation.
Enter the endpoint: `http://localhost:3000/tasks/{taskid}`, replacing `{taskid}` with the task number.
and click on the "Body" tab.
Select the radio button for "raw" and make sure that you select the language as "JSON."
Click "Send." The task will be updated.
The example below would update the top task to be the bottom task.
All of the attributes of the task except the warning have been changed.

```json
{
    "userId": 1,
    "title": "Grocery shopping",
    "description": "eggs, bacon, gummy bears",
    "dueDate": "2025-02-20T17:00",
    "warning": "10",
    "id": 1
}
```

```json
{
    "0": {
        "userId": 2,
        "title": "Take dog out for a walk",
        "description": "Go for a walk with Fido for at least 30 minutes",
        "dueDate": "2025-10-27T17:00",
        "warning": "10",
        "id": 6
    },
    "id": 4
}
```

## Return Values

| Value | Description |
| ------------- | ----------- |
| `200` | OK - the operation has been completed successfully |
| `404` |  Not found - the task does not exist or the server is not running |
| `Connection refused` | You do not have the login credentials for the server |

## Related topics

* [Task resource](task.md)
* [User resource](user.md)
* [Get all users](users-get-all-users.md)
* [Get user by ID](users-get-user-by-id.md)
