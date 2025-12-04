---
layout: default
description: This file has intentionally broken YAML frontmatter
test:
  testable:
    - GET example
  server_url: localhost:3000
  # Missing closing quote on next line
  local_database: "/api/test.json
  broken_list: [unclosed
# Unclosed mapping
---

# Test Document with Broken Frontmatter

This file is used to test error handling when frontmatter is malformed.

The YAML above has several syntax errors:
- Unclosed string
- Unclosed list
- Other YAML syntax issues

The parser should gracefully handle this and return None.
