# Code examples

**Author:** `Christopher Lee`

## `cURL` example

This example replaces an entire task record with new data using `PUT`.

### `cURL` command

```shell
curl -X PUT "http://localhost:3000/tasks/6" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 6,
    "title": "Conduct code review session",
    "completed": false,
    "priority": "high"
  }'
```

### `cURL` response

```shell
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 6,
  "title": "Conduct code review session",
  "completed": false,
  "priority": "high"
}
```

## Postman example

Replace all fields of a task by sending a complete task object.

### Request

**Method**: `PUT`

```shell
PUT /tasks/6 HTTP/1.1
Host: localhost:3000
Content-Type: application/json

{
  "id": 6,
  "title": "Conduct code review session",
  "completed": false,
  "priority": "high"
}
```

### Postman response

```shell
Status: 200 OK
Content-Type: application/json

{
  "id": 6,
  "title": "Conduct code review session",
  "completed": false,
  "priority": "high"
}
```
