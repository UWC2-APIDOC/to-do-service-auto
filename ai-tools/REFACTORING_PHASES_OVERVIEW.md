<!-- vale off -->
<!-- markdownlint-disable MD024 -->

# Refactoring Project Phases Overview

This document provides a comprehensive overview of the refactoring project phases
for the documentation testing tools.

## Project Goal

Refactor redundant code across multiple Python scripts (list-linter-exceptions.py,
markdown-survey.py, test-api-docs.py) and workflows to use shared utilities, with
comprehensive testing for regression detection.

---

## Phase 1: Create Shared Utilities ✅ COMPLETE

### Objectives

- Extract common functionality into reusable utilities
- Establish consistent patterns for file operations, parsing, and logging
- Create comprehensive test infrastructure

### Deliverables

#### 1. Core Utility Module: `doc_test_utils.py`

**Functions created:**

- `parse_front_matter(content)` - Extract YAML from markdown
- `get_test_config(metadata)` - Get test configuration from front matter
- `get_server_database_key(metadata)` - Return (test_apps, server_url, local_database) tuple
- `read_markdown_file(filepath)` - Read markdown with error handling
- `log(message, level, file_path, line, use_actions, action_level)` - Unified
    logging with GitHub Actions annotations

**Log function design:**

- Levels: info, notice, warning, error, success
- Text-only labels (INFO:, WARNING:, ERROR:) for universal compatibility
- Annotation filtering: all, warning, error
- info/success never produce annotations

#### 2. Test Suite: `test_doc_test_utils.py`

**6 test functions covering:**

- Front matter parsing (valid, missing, invalid YAML)
- Config extraction and server/database key generation
- Console output and GitHub Actions annotation filtering
- File reading with error handling
- All tests passing, pytest-compatible

#### 3. Test Data Organization

**test_data/** - Valid files (5 files):

- `sample.md` - Valid front matter with API examples
- `clean.md` - No linter exceptions
- `linter_exceptions.md` - 3 Vale + 3 markdownlint exceptions
- `edge_cases_front_matter.md` - Valid YAML edge cases
- `unicode_test.md` - Unicode characters with exceptions

**fail_data/** - Invalid files (4 files):

- `broken_front_matter.md` - Invalid YAML syntax
- `no_front_matter.md` - Missing front matter delimiters
- `malformed_exceptions.md` - Invalid exception tags
- `empty.md` - Zero-length file

Each directory has comprehensive README.md documentation.

### Key Design Decisions

1. **Text-only severity labels** - Better log file compatibility
2. **Separate test directory structure** - Clear pass/fail organization
3. **Single --action flag** - Simplified CLI (`--action [all|warning|error]`)
4. **Standardized error handling** - Return None, don't raise exceptions
5. **pytest compatibility** - Tests can run standalone or via pytest

### Files Created

- `/mnt/user-data/outputs/doc_test_utils.py`
- `/mnt/user-data/outputs/tests/test_doc_test_utils.py`
- `/mnt/user-data/outputs/tests/test_data/*.md` (5 files + README)
- `/mnt/user-data/outputs/tests/fail_data/*.md` (4 files + README)
- `/mnt/user-data/outputs/tests/README.md`
- `/mnt/user-data/outputs/PHASE_1_SUMMARY.md`

### Test Results

- 6 tests, all passing
- 0 warnings
- Regression protection established

---

## Phase 2: Migrate list-linter-exceptions.py ✅ COMPLETE

### Objectives

- Migrate first script to use shared utilities
- Establish migration pattern for remaining scripts
- Create comprehensive standards documentation

### Deliverables

#### 1. Migrated Script: `list-linter-exceptions.py`

**Changes:**

- Removed 78 lines of custom `annotate()` function
- Replaced with calls to shared `log()` function
- Updated CLI from two flags to single `--action [LEVEL]`
- Uses `read_markdown_file()` from shared utilities
- Code reduction: 237 lines → 215 lines (9% reduction)

**More importantly:** Eliminated duplicated annotation logic that will be shared across all tools.

#### 2. Test Suite: `test_list_linter_exceptions.py`

**7 test functions covering:**

- Vale exception parsing (single, multiple, none)
- markdownlint exception parsing (single, multiple, none)
- Mixed exceptions (both types in same file)
- Malformed tag rejection
- Empty file handling
- Line number accuracy
- Real test data file usage

**All tests passing.**

#### 3. Terminology Refactoring

**"frontmatter" → "front matter":**

- Updated in all code: `parse_front_matter()`
- Updated in all documentation
- Updated in all test files
- Test files renamed: `edge_cases_front_matter.md`, etc.
- Established two-word standard (per Merriam-Webster)

#### 4. Standards Documentation (6 comprehensive guides)

**CODE_STYLE_GUIDE.md:**

- Python naming conventions
- File naming patterns
- Docstring format
- Import organization
- Error handling patterns

**TEST_STANDARDS.md:**

- Test organization (test_data/ vs fail_data/)
- Test structure (AAA pattern)
- Assertion standards
- Coverage requirements
- Output formatting

**TERMINOLOGY.md:**

- Front matter usage rules
- Linter exceptions
- Test vs fail data
- Logging levels
- Naming conventions

**PROJECT_CONVENTIONS.md:**

- Directory structure
- CLI argument patterns
- Logging conventions
- GitHub Actions integration
- Error handling patterns

**REFACTORING_CHECKLIST.md:**

- Step-by-step migration process
- Code changes checklist
- Testing requirements
- Documentation needs
- Verification steps

**STANDARDS_INDEX.md:**

- Document summaries
- Usage patterns
- AI assistant prompts
- Quick reference table

**MARKDOWN_FORMATTING_GUIDE.md:**

- Heading standards (capitalization, punctuation)
- Lists and bullets
- Voice and tone
- Punctuation rules
- Numbers and dates
- Code formatting

### Files Created

- `/mnt/user-data/outputs/list-linter-exceptions.py` (migrated)
- `/mnt/user-data/outputs/tests/test_list_linter_exceptions.py`
- `/mnt/user-data/outputs/CODE_STYLE_GUIDE.md`
- `/mnt/user-data/outputs/TEST_STANDARDS.md`
- `/mnt/user-data/outputs/TERMINOLOGY.md`
- `/mnt/user-data/outputs/PROJECT_CONVENTIONS.md`
- `/mnt/user-data/outputs/REFACTORING_CHECKLIST.md`
- `/mnt/user-data/outputs/STANDARDS_INDEX.md`
- `/mnt/user-data/outputs/MARKDOWN_FORMATTING_GUIDE.md`
- `/mnt/user-data/outputs/PHASE_2_SUMMARY.md`
- `/mnt/user-data/outputs/FRONT_MATTER_REFACTORING.md`
- `/mnt/user-data/outputs/TEST_REORGANIZATION.md`

### Test Results

- 13 total tests (6 utilities + 7 list-linter)
- All passing
- 0 warnings
- Full regression coverage

---

## Phase 3: Migrate Remaining Scripts 🔄 IN PROGRESS

### Objectives

- Migrate `markdown-survey.py` to use shared utilities
- Migrate `test-api-docs.py` to use shared utilities
- Add comprehensive tests for each
- Document any new patterns discovered

### Planned Changes

#### markdown-survey.py

- Replace file reading with `read_markdown_file()`
- Replace logging with shared `log()` function
- Standardize CLI arguments
- Add test suite with appropriate test data

#### test-api-docs.py

- Use `parse_front_matter()` for YAML parsing
- Replace logging with shared `log()` function
- Standardize CLI arguments
- Add comprehensive test suite
- Note: Schema validation may become separate utility in Phase 5

### Expected Deliverables

- Migrated scripts
- Test suites for each
- Updated documentation
- Phase 3 summary document

---

## Phase 4: Extract Workflow Frontmatter Parsing 📋 PLANNED

### Objectives

- Remove front matter parsing from GitHub Actions workflows
- Create utility script for grouping files by server/database configuration
- Simplify workflow YAML files

### Planned Changes

#### Create `get-test-configs.py`

- Accepts list of markdown files
- Parses front matter from each
- Groups files by (test_apps, server_url, local_database)
- Outputs grouped file lists for workflow to process
- Uses shared utilities

#### Update Workflows

- Remove inline front matter parsing logic
- Call `get-test-configs.py` to group files
- Process each group with appropriate configuration
- Cleaner, more maintainable workflow files

### Expected Deliverables

- `get-test-configs.py` utility
- Test suite for grouping logic
- Updated workflow files
- Phase 4 summary document

---

## Phase 5: Schema Validation Utilities 📋 PLANNED

### Objectives

- Extract schema validation logic from `test-api-docs.py`
- Create reusable schema validation utilities
- Support JSON schema validation for front matter

### Planned Changes

#### Potential New Utilities

- `validate_schema(metadata, schema)` - Validate front matter against JSON schema
- Schema loading and caching
- Better error reporting for schema violations

#### Update test-api-docs.py

- Use shared schema validation utilities
- Focus on API-specific testing logic
- Simplified error handling

### Expected Deliverables

- Schema validation utilities
- Test suite for validation
- Updated `test-api-docs.py`
- Phase 5 summary document

---

## Future Enhancements (Post-Phase 5)

### File List/Glob Support

- Add ability to pass file lists or glob patterns to all tools
- Batch processing capabilities
- Better integration with workflows

### Performance Optimization

- Profile tools for bottlenecks
- Optimize for large file sets
- Caching where appropriate

### Additional Test Coverage

- Property-based testing
- Fuzz testing for parser edge cases
- Performance benchmarks

### Documentation

- User guide for all tools
- Architecture documentation
- Contribution guidelines

---

## Success Metrics

### Code Quality

✅ **Achieved:**

- Eliminated code duplication (78 lines removed from list-linter-exceptions.py)
- Established consistent patterns
- Comprehensive test coverage (13 tests and counting)

**Ongoing:**

- Maintain test coverage above 80%
- Keep functions under 50 lines
- Follow all style guide standards

### Maintainability

✅ **Achieved:**

- Centralized shared functionality
- Clear documentation structure
- Standardized CLI patterns

**Ongoing:**

- All tools use shared utilities
- Consistent error handling
- Clear upgrade path for future changes

### Regression Protection

✅ **Achieved:**

- Test suites for all shared utilities
- Test data organized by pass/fail
- All tests passing in CI/CD

**Ongoing:**

- Tests added for each migrated tool
- Tests added for each bug fix
- Weekly scheduled test runs

---

## Timeline Summary

**Phase 1:** ✅ Complete (2024-12-03 to 2024-12-04)

- Shared utilities created
- Test infrastructure established
- Foundation laid

**Phase 2:** ✅ Complete (2024-12-04)

- First script migrated
- Standards documentation created
- Terminology standardized
- 13 tests passing

**Phase 3:** 🔄 In Progress

- Next script: markdown-survey.py
- Then: test-api-docs.py

**Phase 4:** 📋 Planned

- Workflow refactoring
- File grouping utility

**Phase 5:** 📋 Planned

- Schema validation utilities
- Final test-api-docs.py cleanup

---

## Key Learnings

### What Worked Well

1. **Test-Driven Approach**
   - Writing tests alongside utilities caught issues early
   - Test data organization (pass/fail) clarified expectations
   - Comprehensive test coverage provides confidence

2. **Documentation First**
   - Creating standards before migrating remaining tools
   - Clear terminology definitions prevent confusion
   - Checklists ensure consistency

3. **Incremental Migration**
   - One tool at a time allows pattern refinement
   - Early wins (78 lines removed) validate approach
   - Each phase builds on previous work

### What We'd Do Differently

1. **Standards Earlier**
   - Having standards docs from Phase 1 would have prevented some refactoring
   - Terminology guide should precede any code

2. **More Test Data Upfront**
   - Could have created more edge case files initially
   - Some test data needs evolved during testing

3. **Performance Baseline**
   - Should have established performance metrics before refactoring
   - Would help track any regressions

---

## Resources

### Documentation

- `STANDARDS_INDEX.md` - Master guide to all standards
- `CODE_STYLE_GUIDE.md` - Python coding standards
- `TEST_STANDARDS.md` - Testing best practices
- `TERMINOLOGY.md` - Canonical terms and usage
- `PROJECT_CONVENTIONS.md` - Project-wide conventions
- `REFACTORING_CHECKLIST.md` - Step-by-step process
- `MARKDOWN_FORMATTING_GUIDE.md` - Text formatting standards

### Summaries

- `PHASE_1_SUMMARY.md` - Shared utilities creation
- `PHASE_2_SUMMARY.md` - First script migration
- `FRONT_MATTER_REFACTORING.md` - Terminology standardization
- `TEST_REORGANIZATION.md` - Test data restructuring

### Test Infrastructure

- `tests/README.md` - Testing overview
- `tests/test_data/README.md` - Valid test files
- `tests/fail_data/README.md` - Invalid test files

---

## Next Steps

### Immediate (Phase 3)

1. Review standards documentation
2. Begin `markdown-survey.py` migration
3. Follow REFACTORING_CHECKLIST.md
4. Create test suite
5. Verify all tests pass
6. Document Phase 3

### Near-term (Phase 4)

1. Design `get-test-configs.py` utility
2. Create test suite for file grouping
3. Update workflows to use new utility
4. Test workflow changes in CI
5. Document Phase 4

### Long-term (Phase 5+)

1. Extract schema validation
2. Add batch processing support
3. Performance optimization
4. User documentation
5. Architecture documentation

---

## Contact and Collaboration

For questions about:

- **Standards:** See STANDARDS_INDEX.md
- **Testing:** See TEST_STANDARDS.md
- **Terminology:** See TERMINOLOGY.md
- **Process:** See REFACTORING_CHECKLIST.md

---

## Version History

- **v1.0** (2024-12-04): Initial phases document created
    - Phase 1 complete
    - Phase 2 complete
    - Standards documentation established
    - 13 tests passing

---
