# Code examples

**Author:** Amanda Foster

## cURL example

This example updates the title of an existing task while preserving other fields.

### cURL command

```shell
curl -X PATCH "http://localhost:3000/tasks/4" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Write comprehensive test cases"
  }'
```

### cURL response

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 4,
  "title": "Write comprehensive test cases",
  "completed": false
}
```

## Postman example

Modify only the title field of a task without affecting its completion status.

### Request

**Method**: PATCH

```shell
PATCH /tasks/4 HTTP/1.1
Host: localhost:3000
Content-Type: application/json

{
  "title": "Write comprehensive test cases"
}
```

### Postman response

```shell
Status: 200 OK
Content-Type: application/json

{
  "id": 4,
  "title": "Write comprehensive test cases",
  "completed": false
}
```
