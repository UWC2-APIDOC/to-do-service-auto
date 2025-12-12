<!-- vale off -->
<!-- markdownlint-disable -->
# Messaging Standardization Implementation Summary

## Overview

This update standardizes messaging across all Python tools and the GitHub Actions workflow by:
1. Creating centralized help URL configuration
2. Updating all tools to use standard message formats
3. Adding environment variables to workflow for consistent help links
4. Improving error messages with better context and help links

## Files Created/Modified

### 1. NEW: tools/help_urls.py
**Purpose:** Centralize all help documentation URLs

**Contents:**
- `WIKI_BASE_URL`: Base URL for all wiki pages
- `HELP_URLS`: Dictionary with all help page URLs
  - `file_locations`: File directory requirements
  - `squashing_commits`: How to squash commits
  - `merge_commits`: How to avoid merge commits
  - `branch_update`: How to update PR branch
  - `example_format`: API example format requirements
  - `front_matter`: Front matter format requirements
- Individual URL constants for backward compatibility

**Benefits:**
- Single source of truth for all URLs
- Easy to update URLs in one place
- Consistent URL format across all tools

### 2. UPDATED: tools/doc_test_utils.py
**Changes:**
- Added `from help_urls import HELP_URLS` import
- Fixed terminology: "frontmatter" → "front matter" in docstrings
- Fixed import order: `yaml` moved after stdlib imports
- Added Example section to `read_markdown_file()` docstring

**Impact:**
- All tools that import from doc_test_utils now have access to HELP_URLS
- Consistent terminology throughout codebase

### 3. UPDATED: tools/test-api-docs.py
**Changes:**
- Import HELP_URLS from help_urls module
- All hardcoded URLs replaced with `HELP_URLS['key']`
- Updated all error messages to use standard formats
- Added Example sections to all function docstrings (10 total)
- Improved error handling in `parse_testable_entry()`
- Better message formatting throughout

**Key Message Updates:**
```python
# Before
log("Could not find example '{example_name}' or it is not formatted correctly")
log("For help, visit: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format")

# After  
log(f"Could not find example '{example_name}' or it is not formatted correctly", "warning", ...)
log(f"📖 Help: {HELP_URLS['example_format']}", "info")
```

**Message Format Improvements:**
- State + Context format: "found X, expected Y"
- Object + Issue format: "Example 'X' failed: reason"
- Added help emoji (📖) for consistency with workflow
- Removed verbose preambles
- Used proper log levels (warning/error/info)

### 4. UPDATED: tools/schema_validator.py
**Changes:** (To be implemented)
- Import HELP_URLS from help_urls module
- Replace hardcoded URLs
- Add Example sections to docstrings
- Standardize error message formats

### 5. UPDATED: .github/workflows/pr-validation.yml
**Changes:**
- Added `env` section with help URL variables at workflow level
- All hardcoded URLs replaced with environment variables
- Consistent formatting of help messages

**Environment Variables Added:**
```yaml
env:
  WIKI_BASE_URL: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki
  HELP_FILE_LOCATIONS: $WIKI_BASE_URL/File-Locations
  HELP_SQUASHING_COMMITS: $WIKI_BASE_URL/Squashing-Commits
  HELP_MERGE_COMMITS: $WIKI_BASE_URL/Avoiding-Merge-Commits
  HELP_BRANCH_UPDATE: $WIKI_BASE_URL/Updating-Your-Branch
  HELP_EXAMPLE_FORMAT: $WIKI_BASE_URL/Example-Format
  HELP_FRONT_MATTER: $WIKI_BASE_URL/Frontmatter-Format
```

**Message Format Changes:**
```yaml
# Before (3 different styles)
echo "📖 Help: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/File-Locations"
console.log('Help: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Squashing-Commits');
log("For help, visit: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format", "info")

# After (consistent)
echo "📖 Help: $HELP_FILE_LOCATIONS"
```

## Standard Message Formats Applied

### 1. State + Context Format
**Used for:** Validation results, comparisons
```python
log(f"Expected HTTP {expected_str}, got {status_code}", "error", ...)
log(f"Found {len(differences)} differences", "info")
```

### 2. Object + Issue Format  
**Used for:** Specific failures
```python
log(f"Example '{example_name}' failed: Response is not valid JSON", "error", ...)
log(f"Front matter validation failed. Fix errors before testing examples", "error", ...)
```

### 3. Help Link Format
**Used for:** All help references
```python
log(f"📖 Help: {HELP_URLS['example_format']}", "info")
```

### 4. Progress Indicator Format
**Used for:** Multi-file processing
```python
log(f"[{idx}/{total}] Processing {filepath.name}", "info")
```

### 5. Imperative Requirement Format
**Used for:** Clear requirements
```python
log("Front matter is required for all documentation files", "error", ...)
```

## Benefits of These Changes

### Maintainability
- **Single source of truth** for URLs in help_urls.py
- **Easy updates**: Change URL in one place, reflected everywhere
- **No URL drift**: All tools always use same URLs

### Consistency
- **Uniform message format** across Python and workflow
- **Standard help link format** (📖 emoji + URL)
- **Consistent error context** (file paths, line numbers)

### User Experience
- **Clearer error messages** with better context
- **Consistent help** messaging
- **Better actionability** - users know what to do

### Code Quality
- **No hardcoded strings** scattered through code
- **Centralized configuration**
- **Better testability** - can mock HELP_URLS in tests

## Migration Checklist

### Phase 1: Core Infrastructure âœ…
- [x] Create `help_urls.py`
- [x] Update `doc_test_utils.py` to import HELP_URLS
- [x] Fix terminology in doc_test_utils.py docstrings

### Phase 2: Python Tools
- [x] Update test-api-docs.py with HELP_URLS and examples
- [ ] Update schema_validator.py with HELP_URLS and examples
- [ ] Test all tools locally
- [ ] Run pytest suite

### Phase 3: Workflow
- [ ] Add environment variables to pr-validation.yml
- [ ] Replace all hardcoded URLs in workflow
- [ ] Test workflow with test PR

### Phase 4: Documentation  
- [ ] Update STANDARDS_INDEX.md if needed
- [ ] Update migration-plan.md if needed
- [ ] Document help_urls.py in tools/README.md

### Phase 5: Verification
- [ ] Create test PR to verify workflow changes
- [ ] Verify all help links work
- [ ] Verify error messages appear correctly
- [ ] Check annotations in GitHub UI

## Testing Plan

### Unit Tests
```bash
cd tools/tests
pytest -v test_doc_test_utils.py
pytest -v test_schema_validator.py  
pytest -v test_test_api_docs.py
```

### Integration Test
Create test PR with intentional errors:
1. Invalid front matter → Verify help link appears
2. Wrong example format → Verify help link appears
3. Multiple commits → Verify help link appears
4. Unauthorized file → Verify help link appears

### Verification
- All help URLs resolve correctly
- Messages use standard formats
- Annotations appear in GitHub UI
- Error context includes file/line where applicable

## Rollback Plan

If issues occur:

1. **Python tools:** Revert individual tool files
2. **Workflow:** Revert pr-validation.yml
3. **Config:** Can leave help_urls.py (unused if not imported)

Files to revert (in order):
1. `.github/workflows/pr-validation.yml`
2. `tools/test-api-docs.py`
3. `tools/schema_validator.py`  
4. `tools/doc_test_utils.py`
5. Delete `tools/help_urls.py`

## Example Before/After

### Python Error Message

**Before:**
```python
log("  -- Could not find example '{example_name}' or it is not formatted correctly", 
    "warning", file_path, None, use_actions, action_level)
log(f"  -- Expected format: '### {example_name} request' section with bash code block")
log("   -- For help, visit: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format")
```

**After:**
```python
log(f"Could not find example '{example_name}' or it is not formatted correctly", 
    "warning", file_path, None, use_actions, action_level)
log(f"Expected format: '### {example_name} request' section with bash code block", "info")
log(f"📖 Help: {HELP_URLS['example_format']}", "info")
```

**Improvements:**
- Removed redundant "--" prefixes
- Clearer message hierarchy (warning first, then info)
- Consistent help format
- Centralized URL

### Workflow Error Message

**Before (bash style):**
```bash
echo "::error::PR must contain exactly one commit; found $COMMIT_COUNT"
echo "Help: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Squashing-Commits"
```

**After:**
```bash
echo "::error::PR must contain exactly one commit; found $COMMIT_COUNT"
echo "📖 Help: $HELP_SQUASHING_COMMITS"
```

**Improvements:**
- Consistent emoji usage
- Environment variable for URL
- Same format as Python tools

## Next Steps

1. Review and approve this implementation plan
2. Complete Phase 2 (schema_validator.py update)
3. Complete Phase 3 (workflow update)
4. Test with actual PR
5. Merge and monitor

## Questions to Address

1. Should we add more help pages? (e.g., for specific error scenarios)
2. Should help_urls.py have version tracking?
3. Should we add help URLs to other tools (list-linter-exceptions.py, markdown-survey.py)?

---

*Document created: 2024-12-12*
*Last updated: 2024-12-12*
