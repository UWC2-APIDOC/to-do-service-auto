<!-- vale Google.Headings = NO -->
<!-- vale Google.Parens = NO -->

# Documentation Requirements (From PR Validation Workflow)

<!-- vale Google.Colons = NO -->
<!-- vale Google.Passive = NO -->
<!-- vale write-good = NO -->

This document lists all requirements tested in the `pr-validation.yml` GitHub workflow.
These are the rules that documentation must follow to pass automated validation.

## File Location Requirements

### Allowed Directories

- Documentation files: `docs/**/*.md`
- Assignment files: `assignments/**/*.md`

### Restriction

- Students (non-admin, non-write permission users) can only modify files in `/docs/` and `/assignments/`
- Changes to other directories require admin or write permissions

**Violation Result:** PR validation fails with error
**Help Link:** `https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/File-Locations`

---

## Filename Requirements

### Character Restrictions

Filenames must not contain:

- Whitespace characters
- Shell meta-characters: `* ? [ ] | & ; $` `` ` `` `" ' < > ( )`
- Backslashes: `\`
- Colons: `:`

**Validation Tool:** `tools/test-filenames.py`
**Checked via:** `CHANGED_FILES` environment variable
**Violation Result:** Error annotation, PR fails

---

## Commit Requirements

### Commit Count

- PR must contain exactly 1 commit
- No more, no less

**Violation Result:** Error with message showing actual count
**Help Link:** `https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Squashing-Commits`

### Merge Commits

- PR must not contain any merge commits
- Use rebase instead

**Violation Result:** Error with message showing merge commit count
**Help Link:** `https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Avoiding-Merge-Commits`

### Branch Status

- Warning, if PR branch isn't up to date with base branch
- Recommendation to rebase

**Violation Result:** Warning annotation
**Help Link:** `https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Updating-Your-Branch`

---

## Markdown Linting Requirements

### MarkdownLint Rules

Configured in `.github/config/.MarkdownLint.jsonc`:

#### MD007: Unordered list indentation

- Required indent: 4 spaces

#### MD013: Line length

- Maximum: 100 characters

#### MD036: Emphasis used instead of heading

- Disabled

#### MD049: Emphasis style

- Required style: underscore (`_italic_`)

#### MD050: Strong style

- Required style: asterisk (`**bold**`)

#### MD060: Link style

- Required style: compact

**Validation Tool:** `DavidAnson/MarkdownLint-cli2-action@v21`
**Violation Result:** Error annotations on specific lines

---

## Vale (Writing Style) Requirements

Configured in `.vale.ini`:

### Enabled Style Packages

- Vale (core rules)
- Google Developer Documentation Style Guide
- write-good (readability checks)
- Readability (various readability metrics)

### Specific Settings

#### Ignored Scopes

- `code` blocks
- `tt` (teletype) elements

#### Skipped Scopes

- `script` tags
- `style` tags
- `pre` (pre-formatted) blocks
- `figure` elements
- `text.frontmatter` (YAML front matter)

#### Alert Level

- Minimum: suggestion
- All suggestions, warnings, and errors are reported

#### Enabled Rules

- `Vale.terms`: verifies project terminology
- `Google.*`: All Google style guide rules
- `write-good.*`: All rules except E-Prime
- `Readability.FleschKincaid`: checks reading level (complexity)
- Other readability metrics: NO

#### Disabled Rules

- `write-good.E-Prime`: Disabled (allows "to be" verbs)
- `Readability.AutomatedReadability`: Disabled
- `Readability.ColemanLiau`: Disabled
- `Readability.FleschReadingEase`: Disabled
- `Readability.GunningFog`: Disabled
- `Readability.LIX`: Disabled
- `Readability.SMOG`: Disabled

### Custom Vocabulary

- Location: `.github/valeStyles/projectTerms/`
- Project-specific approved terms

**Validation Tool:** `errata-ai/vale-action@v2.1.1`
**Version:** 3.12.0
**Violation Result:** Error annotations on specific lines
**Cached:** Yes (Vale binary cached for performance)

---

## Front Matter Requirements

### Presence

- All files in `/docs/` directory must have YAML front matter
- Front matter must be between `---` delimiters at start of file
- Files with `<!-- front matter not required -->` comment:
    - If in `/docs/`: An error, front matter is required
    - If in `/assignments/`: a warning, front matter is recommended
    - If elsewhere: Silently skipped

**Violation Result:** Error, file can't be tested

### Required Fields

As defined in `.github/schemas/front-matter-schema.json`:

- `layout`: string, must be `default`, `page`, or `post`
- `description`: string, 10-200 characters
- `topic_type`: string, must be `reference`, `tutorial`, `guide`, `concept`, or `overview`

### Optional Standard Fields

#### Navigation/Structure

- `parent`: string, exact match to parent page title
- `has_children`: Boolean, indicates if page has child pages
- `has_toc`: Boolean, indicates if page should show table of contents
- `nav_order`: integer, minimum 1 (lower numbers appear first)

#### Content Classification

- `tags`: array of strings, unique values
- `categories`: array of strings, unique values
- `ai_relevance`: string, must be `high`, `medium`, or `low`
- `importance`: integer, 1-10

#### Documentation Structure

- `prerequisites`: array of strings (page titles or concepts)
- `related_pages`: array of strings (page titles)
- `examples`: array of strings (example names for AI indexing)

#### API-Specific

- `api_endpoints`: array of strings matching pattern `^(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)? ?/.+`
- `version`: string matching pattern `^v[0-9]+\.[0-9]+(\.[0-9]+)?$`
- `last_updated`: string, date format

### Test Configuration (Optional)

Used when file contains testable API examples:

```yaml
test:
  test_apps:          # Array of npm-installable test servers (optional)
    - "json-server@0.17.4"
  server_url:         # URL where test server runs (optional)
    "localhost:3000"
  local_database:     # Path to test database JSON file (optional)
    "/api/to-do-db-source.json"
  testable:           # Array of testable examples (REQUIRED if test exists)
    - "GET example / 200"
    - "POST example / 201,204"
```

#### Test Field Rules

- If `test` object exists, `testable` array is REQUIRED
- `test_apps` pattern: `^[a-zA-Z0-9_-]+(@[0-9]+\.[0-9]+\.[0-9]+)?$`
- `server_url` pattern: `^(https?://)?([a-zA-Z0-9.-]+|localhost)(:[0-9]+)?$`
- `local_database` pattern: `^(/)?[a-zA-Z0-9/_.-]+\.json$`
- `testable` item pattern: `^.+( / [0-9,]+)?$`
    - Format: "example name" or "example name / 200,201"
    - Default status code if omitted: 200

**Validation Tool:** `tools/test-api-docs.py` with JSON schema validation
**Violation Result:** Error annotations with specific schema violation details

---

## API Documentation Testing Requirements

### When Tests Run

- Only runs if files in `docs/` or `assignments/` changed
- Only runs if Markdown linting passed
- Only runs if file has valid front matter with `test` configuration

### Test Discovery

1. Check for `<!-- front matter not required -->` comment (see Front Matter requirements)
2. Parse front matter
3. Validate against schema
4. Check for `test` object with `testable` array
5. Skip files without testable examples

### Example Format Requirements

For each item in `test.testable` array, the Markdown must contain:

#### Request Section

- Heading: `### {example_name} request` or `#### {example_name} request`
    - Example name can have words wrapped in backticks: `` `GET` example ``
    - Case-insensitive heading match
- Code block: ` ```bash ` or ` ```sh `
- Must contain: curl command
- URL substitution: `{server_url}` replaced with `test.server_url` value

**Format Help:** <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format>

#### Response Section

- Heading: `### {example_name} response` or `#### {example_name} response`
    - Same flexible matching as request section
- Code block: ` ```json `
- Must contain: valid JSON response body
- Used for: comparing actual API response with documented response

**Format Help:** <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format>

### Test Execution

#### Database Setup

- Test server: json-server@0.17.4 on port 3000
- Database reset: Before testing each file
- Source: `test.local_database` from file's front matter
- Default: `api/to-do-db-source.json` if not specified
- Format: JSON file with REST resources

#### Request Execution

1. Extract curl command from request section
2. Add `-i` flag if not present (to get headers)
3. Replace `{server_url}` with actual server URL
4. Execute with 10-second timeout
5. Parse HTTP status code from response headers

#### Response Validation

1. Check status code is in expected list
2. Validate response is valid JSON
3. Compare response structure with documented response
4. Report specific differences if mismatch

### Comparison Rules

- Type checking: actual and expected must have same type
- Objects:
    - All expected keys must exist in actual
    - Extra keys in actual generate warnings
- Arrays:
    - Length must match
    - Elements compared by index
- Primitives: Must match exactly
- Differences reported with JSON path

### Test Results

- Error if curl command not found or malformed
- Error if response section not found or malformed  
- Error if status code doesn't match expected
- Error if response isn't valid JSON
- Error if response structure doesn't match documentation
- Warning if example sections not formatted correctly

**Validation Tool:** `tools/test-api-docs.py`
**Violation Result:** Error annotations with specific test failure details

---

## Markdown Survey (Informational)

Not a validation requirement but provides statistics:

### Tracked Metrics

- Number of files processed
- Heading count per file
- Code block count per file
- Linter exceptions (Vale and MarkdownLint)

**Tool:** `tools/markdown-survey.py`
**Output:** Informational annotations (warnings)

---

## Linter Exception Tracking

Documents use of linter exception comments:

### Vale Exceptions

Format: `<!-- vale RuleName = NO -->`

- Tracked and reported
- Not a validation error

### MarkdownLint Exceptions

Format: `<!-- markdownlint-disable MD### -->`

- Tracked and reported
- Not a validation error (but noted)

**Tool:** `tools/list-linter-exceptions.py`
**Output:** Warning annotations showing location and rule

---

## Validation Stages and Dependencies

### Stage 0: Discover Changed Files

- Identifies all changed Markdown files
- Separates by directory (docs vs tools)
- Flags unauthorized changes

### Stage 1: Test Tools (Blocking)

- Runs if any files in `tools/` changed
- Runs pytest on `tools/tests/`
- **All other stages blocked if this fails**

### Stage 2: Lint and Validate Content (Parallel)

- Depends on: Test Tools (success or skipped)
- Runs if: Any Markdown files changed
- Sub-checks:
    - Filename validation
    - Linter exception listing (informational)
    - Markdown survey (informational)
    - MarkdownLint validation
    - Vale validation

### Stage 3: Test API Documentation

- Depends on: Lint and Validate Content (success)
- Runs if: Files in `docs/` or `assignments/` changed
- Tests API examples against live server

### Stage 4: Validate Commits (Final Gate)

- Depends on: Lint and Validate Content (success or skipped) and
    the Test API Documentation (success or skipped)
- Always runs as final check
- Sub-checks:
    - Unauthorized file changes (permission-based)
    - Feature branch status compared to original branch (warning only)
    - Commit count and merge commits

**Failure Behavior:** Fail-fast - if earlier stage fails, dependent stages don't run

---

## Tool Locations

### Python Scripts

- `tools/test-filenames.py` - Filename validation
- `tools/list-linter-exceptions.py` - Exception tracking
- `tools/markdown-survey.py` - Content statistics
- `tools/test-api-docs.py` - API example testing
- `tools/doc_test_utils.py` - Shared utilities
- `tools/schema_validator.py` - Front matter schema validation
- `tools/get-database-path.py` - Extract database path from front matter

### Configuration Files

- `.github/config/.MarkdownLint.jsonc` - MarkdownLint rules
- `.vale.ini` - Vale configuration
- `.github/schemas/front-matter-schema.json` - Front matter schema
- `.github/valeStyles/` - Custom Vale styles and vocabulary

### GitHub Actions

- `.github/workflows/pr-validation.yml` - Main validation workflow

---

## Exit Codes and Results

### Success

- All checks pass
- PR can be merged

### Failure Scenarios

1. **Tool tests fail** - Fix tools before proceeding
2. **Filename invalid** - Rename file to remove special characters
3. **Markdown lint errors** - Fix formatting issues
4. **Vale errors** - Fix writing style issues
5. **Schema validation fails** - Fix front matter structure
6. **API tests fail** - Fix example code or expected responses
7. **Unauthorized files** - Remove changes to restricted directories
8. **Multiple commits** - Squash into single commit
9. **Merge commits** - Rebase to remove merge commits

### Help Resources

- GitHub Wiki: <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/>
- Specific pages linked in error messages

---

## Performance Optimizations

### Caching

- Vale binary cached (3.12.0)
- Python pip dependencies cached

### Batch Processing

- Filename validation: All files in one call
- Linter exception listing: All files in one call
- Markdown survey: All files in one call
- MarkdownLint: All files in one call
- Vale: All files in one call

### Conditional Execution

- Tools tests: Only if tools changed
- Markdown linting: Only if Markdown files changed
- API testing: Only if docs/assignments changed
- Each stage skips if dependencies failed

**Result:** Faster feedback, lower resource usage
