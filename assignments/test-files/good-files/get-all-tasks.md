# Code examples

**Author:** Sarah Chen

## cURL example

This example retrieves all tasks from the to-do service.

### cURL command

```shell
curl -X GET "http://localhost:3000/tasks" \
  -H "Accept: application/json"
```

### cURL response

```shell
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "title": "Complete project proposal",
    "completed": false
  },
  {
    "id": 2,
    "title": "Review pull requests",
    "completed": true
  }
]
```

## Postman example

Retrieve the complete list of tasks using Postman.

### Request

**Method**: GET

```shell
GET /tasks HTTP/1.1
Host: localhost:3000
Accept: application/json
```

### Postman response

```shell
Status: 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "title": "Complete project proposal",
    "completed": false
  },
  {
    "id": 2,
    "title": "Review pull requests",
    "completed": true
  }
]
```
