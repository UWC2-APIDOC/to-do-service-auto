<!-- vale off -->
<!-- markdownlint-disable -->
# Code examples

**Author:** Emily Watson

## cURL example

This example updates the completion status of an existing task.

### cURL command

```shell
curl -X PATCH "http://localhost:3000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

### cURL response

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "title": "Complete project proposal",
  "completed": true
}
```

## Postman example

Mark a task as completed using a PATCH request.

### Request

**Method**: PATCH

```shell
PATCH /tasks/1 HTTP/1.1
Host: localhost:3000
Content-Type: application/json

{
  "completed": true
}
```

### Postman response

```shell
Status: 200 OK
Content-Type: application/json

{
  "id": 1,
  "title": "Complete project proposal",
  "completed": true
}
```
