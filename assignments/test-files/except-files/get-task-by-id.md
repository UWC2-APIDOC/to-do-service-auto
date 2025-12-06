<!-- vale off -->
<!-- markdownlint-disable -->
# Code examples

**Author:** Jessica Martinez

## cURL example

This example retrieves a specific task by its unique identifier.

### cURL command

```shell
curl -X GET "http://localhost:3000/tasks/2" \
  -H "Accept: application/json"
```

### cURL response

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 2,
  "title": "Review pull requests",
  "completed": true,
  "createdAt": "2024-12-01T10:30:00Z"
}
```

## Postman example

Fetch details of a single task using its ID in the URL path.

### Request

**Method**: GET

```shell
GET /tasks/2 HTTP/1.1
Host: localhost:3000
Accept: application/json
```

### Postman response

```shell
Status: 200 OK
Content-Type: application/json

{
  "id": 2,
  "title": "Review pull requests",
  "completed": true,
  "createdAt": "2024-12-01T10:30:00Z"
}
```
