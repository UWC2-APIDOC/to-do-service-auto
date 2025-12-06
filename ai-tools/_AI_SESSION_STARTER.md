<!-- vale off -->
# Session Starter: Documentation Testing Tools Refactoring

Use this template to start a new AI session for continuing the refactoring work.

---

## Quick Start (Copy-Paste This)

Replace `tool-refactor-1` with the current working feature branch and then,
use the following prompt.

```text
I'm working on the documentation testing tools refactoring project.

Repository: https://github.com/rbwatson/to-do-service-auto
Branch: tool-refactor-1
Tools directory: tools/

Please fetch and review these key documents:

**Project Overview:**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/REFACTORING_PHASES_OVERVIEW.md

**Standards Master Index:**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/STANDARDS_INDEX.md

**Step-by-Step Process:**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/REFACTORING_CHECKLIST.md

**Key Conventions (read these next):**
- https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/CODE_STYLE_GUIDE.md
- https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/TEST_STANDARDS.md
- https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/TERMINOLOGY.md
- https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/PROJECT_CONVENTIONS.md

**Current Project Status:**
- Phase 1: ✅ Complete (shared utilities created)
- Phase 2: ✅ Complete (list-linter-exceptions.py migrated, standards docs created)
- Phase 3: 🔄 In Progress (next: markdown-survey.py)

**Task:** [Describe what you want to do - e.g., "Migrate markdown-survey.py to use shared utilities"]

Please confirm you've reviewed the documentation and are ready to proceed.
```

---

## For Script Migration (Phase 3)

Replace `tool-refactor-1` with the current working feature branch and then,
use the following prompt.

```text
I'm continuing Phase 3 of the refactoring project - migrating markdown-survey.py.

Repository: https://github.com/rbwatson/to-do-service-auto
Branch: tool-refactor-1

Please fetch these files:

**Standards & Process:**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/REFACTORING_PHASES_OVERVIEW.md
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/REFACTORING_CHECKLIST.md
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/CODE_STYLE_GUIDE.md
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/TERMINOLOGY.md

**Shared Utilities (for reference):**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/doc_test_utils.py

**Already Migrated (for pattern reference):**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/list-linter-exceptions.py

**Script to Migrate:**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/markdown-survey.py

**Test Structure (for reference):**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/tests/README.md

Please:
1. Analyze markdown-survey.py
2. Identify what needs to change to use shared utilities
3. Propose the migration plan
4. Follow REFACTORING_CHECKLIST.md step-by-step

Ready to start?
```

---

## For Adding/Debugging Tests

Replace `tool-refactor-1` with the current working feature branch and then,
use the following prompt.

```text
I need to [add tests for / debug tests in] [component name].

Repository: https://github.com/rbwatson/to-do-service-auto
Branch: tool-refactor-1

Please fetch:

**Testing Standards:**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/TEST_STANDARDS.md
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/TERMINOLOGY.md

**Test Structure:**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/tests/README.md

**Example Test Suite:**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/tests/test_doc_test_utils.py

**Component to Test:**
[Add URL to the file you're testing]

[If debugging, add: "Tests are failing with this output: [paste output]"]

Please help me [add comprehensive tests / debug the failing tests].
```

---

## For Documentation Updates

Replace `tool-refactor-1` with the current working feature branch and then,
use the following prompt.

```text
I need to update documentation for [topic].

Repository: https://github.com/rbwatson/to-do-service-auto
Branch: tool-refactor-1

Please fetch:

**Formatting Standards:**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/MARKDOWN_FORMATTING_GUIDE.md
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/TERMINOLOGY.md

**Document to Update:**
[Add URL to the file you're updating]

Please review the document and help me update it following the standards.
```

---

## For Bug Fixes

Replace `tool-refactor-1` with the current working feature branch and then,
use the following prompt.

```text
I found a bug in [component]: [description]

Repository: https://github.com/rbwatson/to-do-service-auto
Branch: tool-refactor-1

Please fetch:

**Standards:**
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/CODE_STYLE_GUIDE.md
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/TEST_STANDARDS.md

**Component with Bug:**
[Add URL to the file with the bug]

**Related Tests (if any):**
[Add URL to test file]

Please:
1. Create a regression test that reproduces the bug
2. Fix the bug
3. Verify the test passes
```

---

## All Available Documents (Reference)

### Core Project Documentation

- **REFACTORING_PHASES_OVERVIEW.md** - Complete project overview and status
- **STANDARDS_INDEX.md** - Master guide to all standards
- **AI_ASSISTANT_PROMPTS.md** - This file

### Standards Documents

- **CODE_STYLE_GUIDE.md** - Python coding standards
- **TEST_STANDARDS.md** - Testing best practices
- **TERMINOLOGY.md** - Canonical terms and usage
- **PROJECT_CONVENTIONS.md** - Project-wide conventions
- **REFACTORING_CHECKLIST.md** - Step-by-step migration process
- **MARKDOWN_FORMATTING_GUIDE.md** - Text formatting standards

### Phase Summaries

- **PHASE_1_SUMMARY.md** - Shared utilities creation
- **PHASE_2_SUMMARY.md** - First script migration
- **FRONT_MATTER_REFACTORING.md** - Terminology standardization
- **TEST_REORGANIZATION.md** - Test data restructuring

### Code Files

- **doc_test_utils.py** - Shared utilities module
- **list-linter-exceptions.py** - Migrated script (example)
- **markdown-survey.py** - Next to migrate
- **test-api-docs.py** - To be migrated

### Test Infrastructure

- **tests/README.md** - Testing overview
- **tests/test_doc_test_utils.py** - Utility tests
- **tests/test_list_linter_exceptions.py** - Script tests
- **tests/test_data/README.md** - Valid test files documentation
- **tests/fail_data/README.md** - Invalid test files documentation

---

## URL Template for Any File

Replace `tool-refactor-1` with the current working feature branch and then,
use the following prompt.

```text
https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/[FILE_PATH]


**Examples:**

- https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/doc_test_utils.py
- https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/tests/test_doc_test_utils.py
- https://github.com/rbwatson/to-do-service-auto/blob/tool-refactor-1/tools/tests/test_data/sample.md

```

---

## Key Conventions Reminder

When providing URLs to the AI, remember these key conventions from the documentation:

**Terminology:**

- "front matter" (two words in text), "front_matter" (underscore in code)

**Code Style:**

- Use shared utilities from doc_test_utils.py
- Functions: snake_case
- Scripts: kebab-case.py
- Test files: test_*.py

**Testing:**

- Valid files in tests/test_data/
- Invalid files in tests/fail_data/
- Follow AAA pattern (Arrange-Act-Assert)

**CLI Arguments:**

- Use --action `[all|warning|error]`
- Default to 'warning' when present without argument

**Logging:**

- Use log(message, level, file_path, line, use_actions, action_level)
- Levels: info, notice, warning, error, success

---

## Tips

1. **Always provide explicit URLs** - The AI can't browse the repo freely
2. **Start with project overview** - REFACTORING_PHASES_OVERVIEW.md gives full context
3. **Reference the checklist** - REFACTORING_CHECKLIST.md ensures nothing is missed
4. **One task per session** - Focus on one script or one test suite at a time
5. **Verify tests pass** - Run tests after any changes

---

## Version Info

- **Repository:** `https://github.com/rbwatson/to-do-service-auto`
- **Branch:** tool-refactor-1
- **Last Updated:** 2024-12-04
- **Current Phase:** Phase 3 (script migration)
- **Tests Passing:** 13/13

---

_Keep this file handy for quick reference when starting new AI sessions!_
