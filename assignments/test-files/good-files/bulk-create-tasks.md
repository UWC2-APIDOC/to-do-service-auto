# Code examples

**Author:** `Brandon Cooper`

## `cURL` example

This example creates three tasks in a single request for efficiency.

### `cURL` command

```shell
curl -X POST "http://localhost:3000/tasks/bulk" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "title": "Schedule team meeting",
      "completed": false
    },
    {
      "title": "Prepare presentation slides",
      "completed": false
    },
    {
      "title": "Send status report",
      "completed": false
    }
  ]'
```

### `cURL` response

```shell
HTTP/1.1 201 Created
Content-Type: application/json

[
  {
    "id": 7,
    "title": "Schedule team meeting",
    "completed": false
  },
  {
    "id": 8,
    "title": "Prepare presentation slides",
    "completed": false
  },
  {
    "id": 9,
    "title": "Send status report",
    "completed": false
  }
]
```

## Postman example

Create three tasks at once by sending an array of task objects.

### Request

**Method**: `POST`

```shell
POST /tasks/bulk HTTP/1.1
Host: localhost:3000
Content-Type: application/json

[
  {
    "title": "Schedule team meeting",
    "completed": false
  },
  {
    "title": "Prepare presentation slides",
    "completed": false
  },
  {
    "title": "Send status report",
    "completed": false
  }
]
```

### Postman response

```shell
Status: 201 Created
Content-Type: application/json

[
  {
    "id": 7,
    "title": "Schedule team meeting",
    "completed": false
  },
  {
    "id": 8,
    "title": "Prepare presentation slides",
    "completed": false
  },
  {
    "id": 9,
    "title": "Send status report",
    "completed": false
  }
]
```
