# Code examples

**Author:** `Michael Rodriguez`

## `cURL` example

This example creates a new task in the to-do list.

### `cURL` command

```shell
curl -X POST "http://localhost:3000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Deploy to production",
    "completed": false
  }'
```

### `cURL` response

```shell
HTTP/1.1 201 Created
Content-Type: application/json
Location: /tasks/3

{
  "id": 3,
  "title": "Deploy to production",
  "completed": false
}
```

## Postman example

Create a new task by sending a POST request with task details.

### Request

**Method**: `POST`

```shell
POST /tasks HTTP/1.1
Host: localhost:3000
Content-Type: application/json

{
  "title": "Deploy to production",
  "completed": false
}
```

### Postman response

```shell
Status: 201 Created
Content-Type: application/json
Location: /tasks/3

{
  "id": 3,
  "title": "Deploy to production",
  "completed": false
}
```
