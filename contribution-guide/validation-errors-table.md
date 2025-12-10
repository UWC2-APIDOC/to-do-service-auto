# Validation errors reference

This table lists all problems reported by the PR validation workflow.

<!-- vale Google.Contractions = NO -->
<!-- vale Google.Passive = NO -->
<!-- vale Google.Parens = NO -->
<!-- vale write-good = NO -->

<!-- markdownlint-disable MD013 -->
<!-- markdownlint-disable MD056 -->

| Problem | Severity | Message | Help link |
| --------- | ---------- | --------- | ----------- |
| **File location** |
| Files modified outside allowed directories (non-admin user) | Error | Only files in /docs/ and /assignments/ can be modified by students. | <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/File-Locations> |
| **Filename** |
| Filename contains unsafe characters | Error | Found N unsafe filenames in changed-files list | None |
| **Commit structure** |
| Branch not up to date | Warning | PR branch not up to date. Consider rebasing. | <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Updating-Your-Branch> |
| Multiple commits in PR | Error | PR must contain exactly one commit; found N | <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Squashing-Commits> |
| PR contains merge commits | Error | PR contains merge commits; found N | <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Avoiding-Merge-Commits> |
| **Front matter** |
| Front matter required but has skip comment (docs directory) | Error | Front matter is required for files in /docs directory | None |
| Front matter recommended but has skip comment (assignments) | Warning | Front matter is recommended for assignment files | None |
| No front matter found | Error | No front matter found | None |
| Front matter validation failed (schema errors) | Error | \[Specific schema violation details\] | None |
| Description too short | Error | Description must be at least 10 characters | None |
| Description too long | Error | Description must be at most 200 characters | None |
| Invalid `topic_type` | Error | `topic_type` must be one of: reference, tutorial, guide, concept, overview | None |
| Invalid layout value | Error | layout must be one of: default, page, post | None |
| Database file not found | Error | Database not found: \[path\] | None |
| Using default database (no path specified) | Warning | Using default database | None |
| **MarkdownLint** |
| MD007: List indentation incorrect | Error | \[Line N\] Unordered list indentation (expected 4 spaces) | None |
| MD013: Line too long | Error | \[Line N\] Line length exceeds 100 characters | None |
| MD049: Wrong emphasis style | Error | \[Line N\] Emphasis style should be underscore | None |
| MD050: Wrong strong style | Error | \[Line N\] Strong style should be asterisk | None |
| MD060: Wrong link style | Error | \[Line N\] Link style should be compact | None |
| **Vale** |
| Vale style rule violation | Error | \[Line N\] \[Specific rule and suggestion\] | None |
| Grade level too high | Error | \[Line N\] Flesch-Kincaid grade level exceeds target | None |
| Incorrect terminology | Error | \[Line N\] Use \[correct term\] instead of \[incorrect term\] | None |
| Passive voice | Error | \[Line N\] Use active voice | None |
| Gendered pronouns | Error | \[Line N\] Use gender-neutral pronouns | None |
| **API examples** |
| Example not found or malformed | Warning | Could not find example '\[name\]' or it is not formatted correctly | <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format> |
| Example execution failed | Error | Example '\[name\]' failed: \[error details\] | None |
| Wrong HTTP status code | Error | Example '\[name\]' failed: Expected HTTP \[code\], got \[actual\] | None |
| Response not valid JSON | Error | Example '\[name\]' failed: Response is not valid JSON | None |
| Response section not found | Warning | Could not find documented response for '\[name\]' or it is not formatted correctly | <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format> |
| Response doesn't match documentation | Error | Example '\[name\]' failed: Response does not match documentation | None |
| No valid test configuration | Info | Skipping \[file\] (no valid test configuration) | None |
| **Server** |
| json-server failed to start | Error | json-server failed to start | None |
| json-server stopped responding | Error | json-server stopped responding | None |
| curl request timeout | Error | Request timed out | None |
| **Linter exceptions (informational)** |
| Vale exception found | Warning | Vale exception: \[rule\] | None |
| MarkdownLint exception found | Warning | MarkdownLint exception: \[rule\] | None |

<!-- markdownlint-enable MD056 -->
<!-- markdownlint-enable MD013 -->

## Notes

### Severity levels

**Error** - Validation fails, PR cannot be merged until fixed

**Warning** - Validation passes but issue should be addressed

**Info** - Informational message, no action required

### Message format

Messages shown in GitHub Actions annotations use this format:

```text
::level file=path,line=number::message
```

For example:

```text
::error file=docs/api/users.md,line=45::Line length exceeds 100 characters
::warning file=docs/guide.md::Front matter is recommended for assignment files
```

### Help links

Help links appear in the console output after the error message:

```text
Help: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Squashing-Commits
```

### MarkdownLint rules

For MarkdownLint errors, the rule number, such as `MD013`, appears in the error message.
You can look up rules at:

<https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>

### Vale rules

For Vale errors, the style and rule name appear in the format `Style.Rule`.
Rules come from these style packages:

- Vale (core rules)
- Google (Google Developer Documentation Style Guide)
- write-good (readability checks)
- Readability (Flesch-Kincaid and other metrics)

### API test error details

API test errors include additional context in the console output:

- The curl command that was executed
- The actual HTTP status code received
- Specific JSON differences between actual and expected responses
- JSON path notation for mismatched fields

### Tool test failures

If validation tool tests fail (when tools directory is modified),
the pytest output shows which tests failed and why.
This must be fixed before any other validation runs.
