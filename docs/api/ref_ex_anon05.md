---
# markdownlint-disable
# vale  off
layout: default
# nav_order: 1
parent: task resource
# tags used by AI files
description: PATCH method reference topic for task resource
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

# Update a task by ID

This operation updates or patches one or more properties of an existing task by ID.

---

## Endpoint structure

```bash
PATCH /tasks/{id}
```

---

## Path parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | The unique identifier of the task to update |

---

## Request headers

| Header | Value | Required |
|--------|-------|----------|
| `Content-Type` | `application/json` | Yes |

---

## Request body

Include only the properties you want to update. All fields are optional.

| Property | Type | Description |
|----------|------|-------------|
| `userId` | integer | The ID of the user who owns this task |
| `title` | string | Short description of the task |
| `description` | string | Detailed description of the task |
| `dueDate` | string | When the task is due |
| `warning` | integer | Minutes before due date to send reminder |

---

## Postman request

1. Set the request method to `PATCH`
2. Enter the URL: `http://localhost:3000/tasks/1`
   - Replace `1` with the ID of the task you want to update
3. Go to the **Headers** tab and add:
   - `Content-Type: application/json`
4. Go to the **Body** tab:
   - Select **raw**
   - Choose **JSON** from the dropdown
   - Enter your request body
5. Click **Send**

---

## Example: Update due date

**Request:**

```bash
PATCH http://localhost:3000/tasks/1
Content-Type: application/json
```

**Body:**

```json
{
  "dueDate": "2026-02-20T17:00:00-05:00"
}
```

**Response - 200 OK:**

```json
{
  "userId": 1,
  "title": "Grocery shopping",
  "description": "eggs, bacon, gummy bears",
  "dueDate": "2026-02-20T17:00:00-05:00",
  "warning": 10,
  "id": 1
}
```

---

## More request buffer examples

### Update title and description

```json
{
  "title": "Weekly grocery shopping",
  "description": "eggs, bacon, gummy bears, milk, bread"
}
```

### Set reminder to 24 hours before due date

```json
{
  "warning": 1440
}
```

### Update more than one property at once

```json
{
  "title": "Annual vet appointment",
  "description": "Annual vaccinations and checkup",
  "dueDate": "2026-02-20T17:00:00-05:00",
  "warning": 2880
}
```

---

## Response

Returns the complete updated task object with all properties.

**Success:** `200 OK`

**Response body includes:**

- `id` - Task identifier - unchanged
- `userId` - User who owns the task
- `title` - Task title
- `description` - Task description
- `dueDate` - When the task is due
- `warning` - Reminder timing in minutes

---

## Error responses

| Status Code | Description |
|-------------|-------------|
| `400 Bad Request` | Invalid request body or parameter format |
| `404 Not Found` | Task with the specified ID doesn't exist |
| `500 Server Error` | Unexpected server error occurred |

---

## Related topics

- [Get a user by ID](./users-get-user-by-id.md) - Retrieve details for a specific user
- [Add a new task](../tutorials/add-a-new-task.md) - Add a new task to the service
- [Enroll a new user](../tutorials/enroll-a-new-user.md) - Add a new user to the service
- [Get all users](./users-get-all-users.md) - Retrieve all users in the service
