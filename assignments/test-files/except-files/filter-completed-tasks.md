<!-- vale off -->
<!-- markdownlint-disable -->
# Code examples

**Author:** Robert Taylor

## cURL example

This example filters tasks to show only completed items.

### cURL command

```shell
curl -X GET "http://localhost:3000/tasks?completed=true" \
  -H "Accept: application/json"
```

### cURL response

```shell
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": 2,
    "title": "Review pull requests",
    "completed": true
  },
  {
    "id": 5,
    "title": "Update documentation",
    "completed": true
  }
]
```

## Postman example

Use query parameters to filter the task list by completion status.

### Request

**Method**: GET

```shell
GET /tasks?completed=true HTTP/1.1
Host: localhost:3000
Accept: application/json
```

### Postman response

```shell
Status: 200 OK
Content-Type: application/json

[
  {
    "id": 2,
    "title": "Review pull requests",
    "completed": true
  },
  {
    "id": 5,
    "title": "Update documentation",
    "completed": true
  }
]
```
