---
# markdownlint-disable
# vale  off
layout: default
parent: user resource
nav_order: 2
# tags used by AI files
description: GET the `user` resource with the lastName field
tags:
    - api
categories:
    - api-reference
ai_relevance: high
importance: 7
prerequisites: 
    - /api/user
related_pages: []
examples: []
api_endpoints: 
    - GET users?last_name=
version: "v1.0"
last_updated: "2025-10-26"
# vale  on
# markdownlint-enable
---

# Get a user by last name

Returns an array of users that share the same `lastName` parameter, if they exist.

## Method

`GET`

## URL

```shell
{server_url}/users?last_name=
```

## Parameters

|Parameter name|Type|Description|
|--------------|------|------------|
|`last_name`|string|The last name of the users to return|

## Request headers

None

## Request body

None

## Example request with matching users

```shell
curl -X GET "{server_url}/users?last_name=Smith"
```

## Return body

```json
[
    {
        "lastName": "Smith",
        "firstName": "Ferdinand",
        "email": "f.smith@example.com",
        "id": 1
    },

    {
        "lastName": "Smith",
        "firstName": "Jacqueline",
        "email": "jaq.smith@example.com",
        "id": 5
    }
]
```

**Status:** 200 OK

## Return body properties

|Property name|Type|Description|
|-------------|-----------|-----------|
|`lastName`|string|The last name of the user resource|
|`firstName`|string|The first name of the user resource|
|`email`|string|The email address of the user resource|
|`id`|number|The user's unique record ID|

## Example request with no matching users

**Request:**

```shell
curl "{server_url}/users?last_name=doesNotExist"
```

**Response:**

```json
[]
```

**Status:** 200 OK

## Return status

|Status value|Return status|Description|
|-------------|-----------|-----------|
|200|Success|Requested data returned successfully; empty array `[]` if no matches|
|400|Error|Bad request; missing or invalid `last_name` parameter|
|ECONNREFUSED|N/A|Service is offline; start service, try again|

## Related topics

- [Get all users](../api/users-get-all-users.md)
- [Get a user by ID](../api/users-get-user-by-id.md)
