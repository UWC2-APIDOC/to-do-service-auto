<!-- vale off -->
# AI Assistant Prompt for Documentation Testing Tools Refactoring

Use this prompt when starting a new session or continuing refactoring work on
the documentation testing tools project.

---

## Session Initialization Prompt

```text
I'm working on the documentation testing tools refactoring project.
This is an ongoing project to refactor Python scripts and GitHub Actions workflows
to use shared utilities with comprehensive testing.

Please review these key documents to understand the project:

1. **REFACTORING_PHASES_OVERVIEW.md** - Complete project overview, all phases, current status
2. **STANDARDS_INDEX.md** - Master guide to all project standards and documentation
3. **REFACTORING_CHECKLIST.md** - Step-by-step process for migrations

Key project conventions you must follow:

**Terminology:**
- "front matter" (two words in text/documentation)
- "front_matter" (underscore in Python code)
- See TERMINOLOGY.md for complete list

**Code Style:**
- Use shared utilities from doc_test_utils.py
- Function names: snake_case
- File names: kebab-case.py for scripts, snake_case.py for modules
- Test files: test_*.py (pytest convention)
- Follow CODE_STYLE_GUIDE.md

**Testing:**
- Place valid test files in tests/test_data/
- Place invalid test files in tests/fail_data/
- Write comprehensive tests (happy path, edge cases, errors)
- Follow TEST_STANDARDS.md

**CLI Arguments:**
- Use --action [all|warning|error] for GitHub Actions annotations
- Default to 'warning' level when flag present without argument
- Follow PROJECT_CONVENTIONS.md

**Logging:**
- Use shared log() function: log(message, level, file_path, line, use_actions, action_level)
- Levels: info, notice, warning, error, success
- info/success never create annotations

**Current Status:**
- Phase 1: ✅ Complete (shared utilities created)
- Phase 2: ✅ Complete (list-linter-exceptions.py migrated, standards docs created)
- Phase 3: 🔄 In Progress (next: markdown-survey.py)

Please confirm you've understood these requirements and are ready to proceed with [specific task].
```

---

## Task-Specific Prompts

### For Script Migration

```text
I need to migrate [script-name.py] to use shared utilities following Phase 3 of the refactoring project.

Please:
1. Read REFACTORING_CHECKLIST.md for the complete process
2. Review the existing script at [path/to/script.py]
3. Follow these standards:
   - CODE_STYLE_GUIDE.md for coding conventions
   - TERMINOLOGY.md for correct terms
   - PROJECT_CONVENTIONS.md for CLI and logging patterns
4. Create comprehensive tests following TEST_STANDARDS.md
5. Document changes in a phase summary

Key migration steps:
- Replace file reading with read_markdown_file()
- Replace front matter parsing with parse_front_matter()
- Replace custom logging with shared log()
- Update CLI to use --action [LEVEL] pattern
- Create test suite with test_data/ and fail_data/ files
- Verify all tests pass

Start by analyzing the existing script and proposing the migration plan.
```

### For Adding Tests

```text
I need to add tests for [feature/function] following project test standards.

Please:
1. Read TEST_STANDARDS.md for test structure and organization
2. Create test functions following the Arrange-Act-Assert pattern
3. Cover these scenarios:
   - Happy path (valid input)
   - Invalid input
   - Empty/None input
   - Edge cases
   - Error conditions
4. Place valid test files in tests/test_data/
5. Place invalid test files in tests/fail_data/
6. Document test files in appropriate README.md
7. Verify tests pass: python3 test_file.py AND pytest test_file.py -v

Use TERMINOLOGY.md for correct term usage in test names and documentation.
```

### For Bug Fixes

```text
I found a bug in [component]: [description of bug]

Please:
1. Read CODE_STYLE_GUIDE.md for conventions
2. Create a regression test that reproduces the bug (following TEST_STANDARDS.md)
3. Verify the test fails with current code
4. Fix the bug
5. Verify the test passes
6. Follow error handling patterns from PROJECT_CONVENTIONS.md
7. Update documentation if behavior changes

Use TERMINOLOGY.md for correct term usage in any documentation updates.
```

### For Documentation Updates

```text
I need to update documentation for [topic/section].

Please:
1. Read MARKDOWN_FORMATTING_GUIDE.md for formatting standards
2. Read TERMINOLOGY.md for correct term usage
3. Follow these conventions:
   - Sentence-style capitalization for headings
   - No heading punctuation
   - Active voice
   - Use "you" for second person
4. Maintain consistency with existing documentation
5. Update related cross-references if needed

The documentation to update is: [path/to/doc.md]
```

### For Creating New Utilities

```text
I need to create a new utility function for [purpose].

Please:
1. Read CODE_STYLE_GUIDE.md for coding standards
2. Read TERMINOLOGY.md for correct term usage
3. Add the function to doc_test_utils.py (or propose new module if warranted)
4. Follow these requirements:
   - Google-style docstrings with examples
   - Type hints for all parameters
   - Return None for errors with appropriate logging
   - Keep functions under 50 lines
5. Create comprehensive test suite following TEST_STANDARDS.md
6. Update tests/README.md with new test information

Start by proposing the function signature and explaining the approach.
```

---

## Quick Reference for Common Tasks

### Continue Current Phase

```text
I'm continuing Phase 3 of the refactoring project. The next script to migrate is markdown-survey.py.

Please:
1. Review REFACTORING_PHASES_OVERVIEW.md for context
2. Follow REFACTORING_CHECKLIST.md step-by-step
3. Apply all standards from STANDARDS_INDEX.md
4. Create comprehensive tests
5. Document the migration

Start by analyzing markdown-survey.py and proposing the migration approach.
```

### Review Code Changes

```text
I've made changes to [file-name]. Please review for compliance with project standards.

Check against:
- CODE_STYLE_GUIDE.md (naming, structure, docstrings)
- TERMINOLOGY.md (correct term usage)
- PROJECT_CONVENTIONS.md (logging, error handling)
- TEST_STANDARDS.md (if tests included)

Provide specific feedback on what needs to change.
```

### Troubleshoot Test Failures

```text
Tests are failing for [test-file]. Here's the output:
[paste test output]

Please:
1. Analyze the failure
2. Refer to TEST_STANDARDS.md for expected patterns
3. Check CODE_STYLE_GUIDE.md for potential issues
4. Propose fixes
5. Explain what caused the failure
```

---

## Information to Provide

When starting a session, provide:

**Required:**

- Which phase you're working on (see REFACTORING_PHASES_OVERVIEW.md)
- What specific task needs to be done
- Location of relevant files

**Helpful:**

- Current test status (passing/failing)
- Any recent changes or context
- Specific concerns or questions

**Available Resources:**
The AI has access to these key documents:

- CODE_STYLE_GUIDE.md
- MARKDOWN_FORMATTING_GUIDE.md
- PROJECT_CONVENTIONS.md
- REFACTORING_CHECKLIST.md
- REFACTORING_PHASES_OVERVIEW.md
- STANDARDS_INDEX.md
- TERMINOLOGY.md
- TEST_STANDARDS.md

And phase summaries:

- PHASE_1_SUMMARY.md
- PHASE_2_SUMMARY.md
- FRONT_MATTER_REFACTORING.md
- TEST_REORGANIZATION.md

---

## Example Complete Session Start

```text
I'm working on the documentation testing tools refactoring project.
This is Phase 3 - migrating remaining scripts to use shared utilities.

Project overview:
- Phase 1 ✅ Complete: Created shared utilities (doc_test_utils.py)
- Phase 2 ✅ Complete: Migrated list-linter-exceptions.py, created standards docs
- Phase 3 🔄 In Progress: Next to migrate is markdown-survey.py

Please review these documents to understand the project:
1. REFACTORING_PHASES_OVERVIEW.md - Complete project context
2. STANDARDS_INDEX.md - All standards documentation
3. REFACTORING_CHECKLIST.md - Step-by-step migration process

Key conventions:
- "front matter" (two words in text), "front_matter" (in code)
- Use shared utilities from doc_test_utils.py
- CLI pattern: --action [all|warning|error]
- Test organization: test_data/ (pass) vs fail_data/ (fail)
- Follow CODE_STYLE_GUIDE.md, TEST_STANDARDS.md, TERMINOLOGY.md

Task: Migrate markdown-survey.py to use shared utilities

The script is located at [path]. Please:
1. Analyze the current script
2. Identify what needs to change to use shared utilities
3. Propose the migration plan
4. Follow REFACTORING_CHECKLIST.md throughout

Ready to proceed?
```

---

## Tips for Effective Sessions

### Do

✅ Reference specific standards documents by name
✅ Ask the AI to confirm understanding before starting
✅ Break large tasks into steps
✅ Request verification against checklists
✅ Ask for explanations of design decisions

### Don't

❌ Assume the AI remembers previous sessions (always provide context)
❌ Skip referencing the standards documents
❌ Merge multiple unrelated tasks
❌ Forget to verify tests pass after changes
❌ Skip documentation updates

---

## Handling Common Situations

### "I'm not sure which phase we're on"

```text
Please read REFACTORING_PHASES_OVERVIEW.md and tell me:
1. What the current phase status is
2. What's been completed
3. What's next in the sequence
4. What I should work on now
```

### "I need to understand the standards"

```text
Please read STANDARDS_INDEX.md and summarize:
1. What each standards document covers
2. Which documents are most relevant for [my task]
3. The key conventions I must follow
```

### "The tests are failing and I don't know why"

```text
Please analyze this test failure:
[paste output]

Then:
1. Review TEST_STANDARDS.md for expected patterns
2. Check if the test follows project conventions
3. Identify the root cause
4. Propose a fix
```

### "I need to onboard a new contributor"

```text
A new contributor is joining the project. Please:
1. Read REFACTORING_PHASES_OVERVIEW.md
2. Read STANDARDS_INDEX.md
3. Create an onboarding guide that covers:
   - Project goals and current status
   - Key conventions they must follow
   - How to run tests
   - Which documents to read first
   - How to get started with their first task
```

---

## Version History

- **v1.0** (2024-12-04): Initial prompt guide created
    - Phase 1 and 2 complete
    - All standards documents available
    - 13 tests passing

---

## Notes

- These prompts assume the AI has access to all standards documents
- Adjust file paths based on your actual project structure
- The AI may need to use conversation_search or recent_chats tools to find previous context
- Always verify the AI understood the requirements before it starts work
- Keep prompts focused on one task at a time for best results

---

_Save this document for quick reference when starting new AI sessions.
Update version history as project progresses._
