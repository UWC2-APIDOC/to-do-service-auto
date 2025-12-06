# Code examples

**Author:** `David Kim`

## `cURL` example

This example demonstrates how to delete a task from the system.

### `cURL` command

```shell
curl -X DELETE "http://localhost:3000/tasks/3" \
  -H "Accept: application/json"
```

### `cURL` response

```shell
HTTP/1.1 204 No Content
```

## Postman example

Remove a task permanently by sending a `DELETE` request with the task ID.

### Request

**Method**: `DELETE`

```shell
DELETE /tasks/3 HTTP/1.1
Host: localhost:3000
Accept: application/json
```

### Postman response

```shell
Status: 204 No Content
```
