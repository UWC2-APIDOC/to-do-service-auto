<!-- vale off -->
# Front Matter Refactoring Complete

## Changes Made

Refactored from "frontmatter" (one word) to "front matter" / "front_matter" (two words) per
Merriam-Webster dictionary.

### Code Files Updated

1. **doc_test_utils.py**

   - `parse_frontmatter()` → `parse_front_matter()`
   - Updated all docstrings and comments
   - "frontmatter" → "front matter" in documentation

2. **tests/test_doc_test_utils.py**

   - `test_parse_frontmatter()` → `test_parse_front_matter()`
   - Updated import statement
   - Updated all function calls
   - Updated test output messages

### Test Data Files Renamed

1. **test_data/**

   - `edge_cases_frontmatter.md` → `edge_cases_front_matter.md`

2. **fail_data/**

   - `broken_frontmatter.md` → `broken_front_matter.md`
   - `no_frontmatter.md` → `no_front_matter.md`

### Documentation Updated

1. **tests/README.md**

   - Updated test coverage descriptions
   - "Frontmatter" → "Front matter"

2. **tests/test_data/README.md**

   - Updated all file descriptions
   - Updated naming conventions
   - Updated code examples

3. **tests/fail_data/README.md**

   - Updated all file descriptions
   - Updated code examples
   - Updated expected behavior descriptions

4. **File Content**

   - Updated markdown content within test files
   - Headings and descriptions now use "front matter"

## Verification

All tests passing after refactoring:

```text
======================================================================
 TEST SUMMARY: 6 passed, 0 failed
======================================================================
```

## File Structure After Refactoring

```text
tests/
├── test_doc_test_utils.py              # Uses parse_front_matter()
├── test_data/
│   └── edge_cases_front_matter.md      # Renamed
└── fail_data/
    ├── broken_front_matter.md          # Renamed
    └── no_front_matter.md              # Renamed
```

## Consistency Rules Going Forward

**In text/documentation:** Use "front matter" (two words)

- Example: "The front matter contains metadata"

**In code:**

- Python: Use `front_matter` (underscore)
    - Functions: `parse_front_matter()`
    - Variables: `front_matter_data`
- File names: Use `front_matter` (underscore) or `front-matter` (hyphen)
    - Test files: `edge_cases_front_matter.md`
    - Documentation: `front-matter-guide.md`

## Still To Be Refactored

**test-api-docs.py** (Phase 3) will need:

- `parse_frontmatter()` → `parse_front_matter()`
- `validate_frontmatter()` → `validate_front_matter()`
- All related variable names and comments

This will be done when we migrate test-api-docs.py to use shared utilities.
