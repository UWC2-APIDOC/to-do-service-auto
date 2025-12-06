# Code examples

**Author:** Nicole Anderson

## cURL example

This example searches for tasks containing specific keywords in their title.

### cURL command

```shell
curl -X GET "http://localhost:3000/tasks?q=review" \
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
    "id": 6,
    "title": "Conduct code review session",
    "completed": false
  }
]
```

## Postman example

Use the query parameter to search for tasks matching a text pattern.

### Request

**Method**: GET

```shell
GET /tasks?q=review HTTP/1.1
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
    "id": 6,
    "title": "Conduct code review session",
    "completed": false
  }
]
```
