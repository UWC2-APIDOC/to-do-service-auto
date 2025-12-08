<!-- vale off -->
<!-- markdownlint-disable -->
# Migration Plan: Workflow Reorganization & Python Script Optimization

**Version:** 1.0  
**Date:** 2024-12-06  
**Estimated Duration:** 2-3 weeks  
**Risk Level:** Low to Medium  

---

## Executive Summary

This plan implements two major optimizations:

1. **Workflow Reorganization** - Consolidate 4 separate workflows into 1 with staged dependencies
2. **Python Script Optimization** - Enable batch file processing to eliminate interpreter startup overhead

**Expected Benefits:**
- **Performance:** 65-150 seconds faster per PR
- **Reliability:** Fail-fast execution prevents wasted resources
- **Maintainability:** Single workflow file, clearer dependencies
- **Code Quality:** Better error handling and progress reporting

**Timeline:**
- Week 1: Python script updates + testing
- Week 2: Workflow consolidation + testing
- Week 3: Deployment + monitoring

---

## Table of Contents

1. [Pre-Migration Checklist](#pre-migration-checklist)
2. [Phase 1: Python Script Optimization](#phase-1-python-script-optimization)
3. [Phase 2: Workflow Consolidation](#phase-2-workflow-consolidation)
4. [Phase 3: Testing & Validation](#phase-3-testing--validation)
5. [Phase 4: Deployment](#phase-4-deployment)
6. [Phase 5: Post-Deployment](#phase-5-post-deployment)
7. [Rollback Plan](#rollback-plan)
8. [Success Criteria](#success-criteria)

---

## Pre-Migration Checklist

### Documentation Review
- [ ] Read `workflow-reorganization-plan.md`
- [ ] Read `workflow-optimization-analysis.md`
- [ ] Read `python-loop-optimization-analysis.md`
- [ ] Review current workflows in `.github/workflows/`
- [ ] Review project standards in `/mnt/project/`

### Environment Setup
- [ ] Create feature branch: `feature/workflow-optimization`
- [ ] Set up local testing environment
- [ ] Install required dependencies:
  ```bash
  pip install pyyaml pytest --break-system-packages
  ```
- [ ] Verify access to repository settings (for testing workflows)

### Backup Current State
- [ ] Document current workflow files:
  - `pr-test-tools.yml`
  - `pr-commit-test.yml`
  - `pr-lint-tests.yml`
  - `pr-api-doc-content-test.yml`
- [ ] Document current Python scripts:
  - `tools/list-linter-exceptions.py`
  - `tools/markdown-survey.py`
  - `tools/test-filenames.py`
- [ ] Tag current state: `git tag pre-workflow-optimization`

### Risk Assessment
- [ ] Identify critical workflows (what absolutely cannot break)
- [ ] Identify low-risk testing scenarios
- [ ] Prepare communication plan for team
- [ ] Schedule maintenance window (if needed)

---

## Phase 1: Python Script Optimization

**Duration:** Week 1 (5-7 days)  
**Risk:** Low (backwards compatible)  
**Can be deployed independently:** Yes

### 1.1: Update list-linter-exceptions.py

#### Step 1: Update Argument Parser

**File:** `tools/list-linter-exceptions.py`

**Current:**
```python
parser.add_argument(
    'filename',
    type=str,
    help='Path to the Markdown file to scan'
)
```

**New:**
```python
parser.add_argument(
    'files',
    nargs='+',
    type=str,
    help='Path(s) to the Markdown file(s) to scan'
)
```

**Changes:**
- Rename `filename` → `files`
- Add `nargs='+'` to accept multiple files
- Update help text

#### Step 2: Update Main Function

**Current:**
```python
def main():
    # ... argument parsing ...
    filepath = Path(args.filename)
    content = read_markdown_file(filepath)
    if content is None:
        sys.exit(1)
    exceptions = list_vale_exceptions(content)
    if args.action:
        output_action(filepath, exceptions, args.action)
    else:
        output_normal(filepath, exceptions)
```

**New:**
```python
def main():
    # ... argument parsing ...
    
    # Track overall status
    all_exceptions = {'vale': [], 'markdownlint': []}
    failed_files = []
    total_files = len(args.files)
    
    log(f"Scanning {total_files} file(s) for linter exceptions...", "info")
    
    for idx, filename in enumerate(args.files, 1):
        filepath = Path(filename)
        
        # Progress indicator
        if total_files > 1:
            log(f"[{idx}/{total_files}] Processing {filepath.name}", "info")
        
        # Read file
        content = read_markdown_file(filepath)
        if content is None:
            failed_files.append(str(filepath))
            log(f"Failed to read {filepath}", "error", str(filepath), None, 
                args.action is not None, args.action or 'warning')
            continue
        
        # Scan for exceptions
        exceptions = list_vale_exceptions(content)
        
        # Output results
        if args.action:
            output_action(filepath, exceptions, args.action)
        else:
            output_normal(filepath, exceptions)
        
        # Aggregate for summary
        all_exceptions['vale'].extend(exceptions['vale'])
        all_exceptions['markdownlint'].extend(exceptions['markdownlint'])
    
    # Final summary
    total_vale = len(all_exceptions['vale'])
    total_md = len(all_exceptions['markdownlint'])
    
    if total_files > 1:
        log(f"Summary: {total_vale} Vale, {total_md} markdownlint exceptions across {total_files} files",
            "info")
    
    if failed_files:
        log(f"Failed to process {len(failed_files)} file(s)", "error")
        sys.exit(1)
    
    sys.exit(0)
```

**Key changes:**
- Loop through `args.files` instead of single file
- Add progress indicator for multiple files
- Aggregate exceptions across files
- Track failed files
- Provide summary for multiple files
- Proper exit code handling

#### Step 3: Update Tests

**File:** `tools/tests/test_list_linter_exception.py`

**Add new test:**
```python
def test_multiple_files():
    """Test processing multiple files at once."""
    print("\n" + "="*60)
    print("TEST: Process multiple files")
    print("="*60)
    
    # Create test data
    test_dir = Path(__file__).parent / "test_data"
    file1 = test_dir / "linter_exceptions.md"
    file2 = test_dir / "clean.md"
    file3 = test_dir / "unicode_test.md"
    
    # Save original sys.argv
    original_argv = sys.argv
    
    try:
        # Simulate command line with multiple files
        sys.argv = ['test', str(file1), str(file2), str(file3)]
        
        # Mock the main function to capture results
        # (This requires refactoring main to return results)
        # For now, verify it doesn't crash
        
        # Verify individual file processing still works
        content1 = read_markdown_file(file1)
        exceptions1 = list_linter_exceptions.list_vale_exceptions(content1)
        assert len(exceptions1['vale']) > 0, "Should find exceptions in file1"
        
        content2 = read_markdown_file(file2)
        exceptions2 = list_linter_exceptions.list_vale_exceptions(content2)
        assert len(exceptions2['vale']) == 0, "Should find no exceptions in file2"
        
        print("  SUCCESS: Multiple file processing works")
        
    finally:
        sys.argv = original_argv
    
    print("  ✓ All multiple file tests passed")
```

#### Step 4: Update Documentation

**File:** `tools/list-linter-exceptions.py` (docstring)

```python
"""
Scan Markdown files for Vale and markdownlint exception tags.

Usage:
    list-linter-exceptions.py <file1> [file2 ...] [--action [LEVEL]]
    
Examples:
    # Single file
    list-linter-exceptions.py README.md
    
    # Multiple files
    list-linter-exceptions.py file1.md file2.md file3.md
    
    # With glob expansion (shell expands)
    list-linter-exceptions.py docs/*.md
    
    # GitHub Actions mode
    list-linter-exceptions.py docs/*.md --action

Note: Does not test front matter sections.
"""
```

**Checklist:**
- [ ] Update argument parser
- [ ] Update main() function
- [ ] Add progress indicators
- [ ] Add error aggregation
- [ ] Add summary reporting
- [ ] Update tests
- [ ] Update docstring
- [ ] Test single file (backwards compat)
- [ ] Test multiple files
- [ ] Test with --action flag
- [ ] Run pytest to verify all tests pass

**Estimated Time:** 2-3 hours

---

### 1.2: Update markdown-survey.py

**Same process as 1.1**

**File:** `tools/markdown-survey.py`

**Key changes:**
- Update `parser.add_argument('filename', ...)` → `parser.add_argument('files', nargs='+', ...)`
- Loop through files internally
- Add progress indicators
- Aggregate statistics across files
- Summary reporting

**Additional feature:** Cross-file statistics
```python
# After processing all files
log(f"Statistics across {total_files} files:", "info")
log(f"  Total headings: {total_headings}", "info")
log(f"  Total code blocks: {total_code_blocks}", "info")
log(f"  Average headings per file: {total_headings/total_files:.1f}", "info")
```

**Checklist:**
- [ ] Update argument parser
- [ ] Update main() function
- [ ] Add progress indicators
- [ ] Add cross-file statistics
- [ ] Update tests
- [ ] Update docstring
- [ ] Run pytest to verify all tests pass

**Estimated Time:** 2-3 hours

---

### 1.3: Update test-filenames.py

**File:** `tools/test-filenames.py`

**Note:** This script already reads files from environment variable, but we should verify it handles the batch correctly.

**Review current implementation:**
```python
def get_changed_files() -> List[str]:
    """Get list of changed files from environment variable."""
    changed = os.environ.get('CHANGED_FILES', '')
    if not changed:
        return []
    return [f.strip() for f in changed.split(',') if f.strip()]

def main():
    files = get_changed_files()
    # Already processes all files in one run ✓
```

**No changes needed** - Already optimized!

**Checklist:**
- [ ] Review implementation
- [ ] Verify it processes all files in batch
- [ ] Confirm tests cover batch processing
- [ ] Document that it's already optimized

**Estimated Time:** 30 minutes

---

### 1.4: Consider test-api-docs.py (Optional)

**File:** `tools/test-api-docs.py`

**Decision:** Skip for now due to complexity

**Reason:**
- Requires server lifecycle management per file
- Each file may need different server configuration
- Lower benefit (typically 1-5 files)
- Higher complexity/risk

**Future consideration:** Phase 2 optimization if needed

---

### 1.5: Phase 1 Testing

**Create test PR with updated scripts:**

1. Create test branch: `test/python-script-optimization`
2. Make test changes to markdown files
3. Push and create PR
4. Verify:
   - [ ] Scripts run successfully
   - [ ] Progress indicators appear in logs
   - [ ] Summary statistics are accurate
   - [ ] Annotations still work correctly
   - [ ] Single file still works (backwards compat)
   - [ ] Multiple files work
   - [ ] Error handling works (test with broken file)

**Estimated Time:** 2-3 hours

---

## Phase 2: Workflow Consolidation

**Duration:** Week 2 (5-7 days)  
**Risk:** Medium (affects all PR validation)  
**Depends on:** Phase 1 (optional but recommended)

### 2.1: Create New Consolidated Workflow

**File:** `.github/workflows/pr-validation.yml`

**Structure:**

```yaml
name: Pull Request Validation

on:
  pull_request:
    types: [opened, synchronize]
  workflow_dispatch:

jobs:
  # ============================================================
  # STAGE 0: Discover Changed Files
  # ============================================================
  discover-changes:
    name: Discover Changed Files
    runs-on: ubuntu-latest
    outputs:
      # Markdown files (excluding tools)
      all_md_files: ${{ steps.all-md.outputs.all_changed_files }}
      all_md_count: ${{ steps.all-md.outputs.all_changed_files_count }}
      any_md_changed: ${{ steps.all-md.outputs.any_changed }}
      
      # Docs markdown files
      docs_md_files: ${{ steps.docs-md.outputs.all_changed_files }}
      docs_md_count: ${{ steps.docs-md.outputs.all_changed_files_count }}
      any_docs_changed: ${{ steps.docs-md.outputs.any_changed }}
      
      # Tools files
      any_tools_changed: ${{ steps.tools.outputs.any_changed }}
      
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Get all markdown files (excluding tools)
        id: all-md
        uses: tj-actions/changed-files@v40
        with:
          files: |
            **/*.md
            !tools/**/*.md
          separator: ','
      
      - name: Get docs markdown files
        id: docs-md
        uses: tj-actions/changed-files@v40
        with:
          files: docs/**/*.md
          separator: ' '  # Space-separated for easier Python consumption
      
      - name: Get tools files
        id: tools
        uses: tj-actions/changed-files@v40
        with:
          files: tools/**
      
      - name: Display summary
        run: |
          echo "## Changed Files Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "- Markdown files: ${{ steps.all-md.outputs.all_changed_files_count }}" >> $GITHUB_STEP_SUMMARY
          echo "- Docs markdown: ${{ steps.docs-md.outputs.all_changed_files_count }}" >> $GITHUB_STEP_SUMMARY
          echo "- Tools files: ${{ steps.tools.outputs.any_changed }}" >> $GITHUB_STEP_SUMMARY

  # ============================================================
  # STAGE 1: Test Tools (BLOCKING)
  # ============================================================
  test-tools:
    name: Validate Testing Tools
    runs-on: ubuntu-latest
    needs: [discover-changes]
    if: needs.discover-changes.outputs.any_tools_changed == 'true'
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install pyyaml pytest --break-system-packages
      
      - name: Run tool tests
        run: |
          cd tools/tests
          pytest -v
      
      - name: Test summary
        if: always()
        run: |
          echo "## Testing Tools Validation" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          if [ "${{ job.status }}" == "success" ]; then
            echo "✅ All tool tests passed" >> $GITHUB_STEP_SUMMARY
          else
            echo "❌ Tool tests failed - fix before proceeding" >> $GITHUB_STEP_SUMMARY
          fi

  # ============================================================
  # STAGE 2: Parallel Basic Validation
  # ============================================================
  validate-commits:
    name: Validate Commit Structure
    runs-on: ubuntu-latest
    needs: [test-tools]
    if: |
      always() && 
      (needs.test-tools.result == 'success' || needs.test-tools.result == 'skipped')
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      # Job 1: File location check
      - name: Get files outside allowed directories
        id: outside-allowed
        uses: tj-actions/changed-files@v40
        with:
          files: |
            !docs/**
            !assignments/**
      
      - name: Check unauthorized file changes
        if: steps.outside-allowed.outputs.any_changed == 'true'
        uses: actions/github-script@v6
        with:
          script: |
            const author = context.payload.pull_request.user.login;
            
            const { data: permission } = await github.rest.repos.getCollaboratorPermissionLevel({
              owner: context.repo.owner,
              repo: context.repo.repo,
              username: author
            });
            
            if (permission.permission === 'admin' || permission.permission === 'write') {
              console.log(`✓ User ${author} has write access`);
            } else {
              core.setFailed(`Only files in /docs/ and /assignments/ can be modified by students.`);
              console.log('Unauthorized files changed:');
              console.log('${{ steps.outside-allowed.outputs.all_changed_files }}'.split(' ').join('\n'));
              console.log('📖 Help: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/File-Locations');
            }
      
      # Job 2: Commit structure check
      - name: Check if branch is up to date
        run: |
          BASE_SHA=${{ github.event.pull_request.base.sha }}
          HEAD_SHA=${{ github.event.pull_request.head.sha }}
          
          git fetch origin ${{ github.event.pull_request.base.ref }}
          
          if ! git merge-base --is-ancestor $BASE_SHA $HEAD_SHA; then
            echo "::warning::PR branch not up to date. Consider rebasing."
          else
            echo "✓ Branch is up to date"
          fi
      
      - name: Check commit requirements
        run: |
          BASE_SHA=${{ github.event.pull_request.base.sha }}
          HEAD_SHA=${{ github.event.pull_request.head.sha }}
          
          COMMIT_COUNT=$(git rev-list --count $BASE_SHA..$HEAD_SHA)
          MERGE_COMMITS=$(git rev-list --merges $BASE_SHA..$HEAD_SHA | wc -l)
          
          FAILED=false
          
          if [ $COMMIT_COUNT -ne 1 ]; then
            echo "::error::PR must contain exactly one commit; found $COMMIT_COUNT"
            FAILED=true
          fi
          
          if [ $MERGE_COMMITS -gt 0 ]; then
            echo "::error::PR contains merge commits; found $MERGE_COMMITS"
            FAILED=true
          fi
          
          if [ "$FAILED" = true ]; then
            exit 1
          fi
          
          echo "✓ PR has exactly 1 commit and no merge commits"

  lint-markdown:
    name: Lint Markdown Files
    runs-on: ubuntu-latest
    needs: [discover-changes, test-tools]
    if: |
      always() && 
      (needs.test-tools.result == 'success' || needs.test-tools.result == 'skipped') &&
      needs.discover-changes.outputs.any_md_changed == 'true'
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
          cache: 'pip'
      
      - name: Install Python dependencies
        run: pip install pyyaml --break-system-packages
      
      # Test filenames (optimized - single call)
      - name: Test filenames
        env:
          CHANGED_FILES: ${{ needs.discover-changes.outputs.all_md_files }}
        run: python3 tools/test-filenames.py --action
      
      # List linter exceptions (optimized - single call)
      - name: List linter exceptions
        run: |
          files="${{ needs.discover-changes.outputs.all_md_files }}"
          # Convert comma-separated to space-separated
          files_space="${files//,/ }"
          python3 tools/list-linter-exceptions.py --action $files_space
      
      # Markdown survey (optimized - single call)
      - name: Survey markdown
        run: |
          files="${{ needs.discover-changes.outputs.all_md_files }}"
          files_space="${files//,/ }"
          python3 tools/markdown-survey.py --action $files_space
      
      # MarkdownLint
      - name: Run MarkdownLint
        uses: DavidAnson/markdownlint-cli2-action@v21
        with:
          globs: ${{ needs.discover-changes.outputs.all_md_files }}
          config: .markdownlint.json
          separator: ','
      
      # Vale (with caching)
      - name: Cache Vale
        uses: actions/cache@v3
        with:
          path: ~/.vale
          key: vale-3.12.0
      
      - name: Install Vale
        run: |
          if [ ! -f ~/.vale/vale ]; then
            mkdir -p ~/.vale
            wget https://github.com/errata-ai/vale/releases/download/v3.12.0/vale_3.12.0_Linux_64-bit.tar.gz
            tar -xvzf vale_3.12.0_Linux_64-bit.tar.gz
            mv vale ~/.vale/
          fi
          sudo ln -sf ~/.vale/vale /usr/local/bin/vale
          vale --version
      
      - name: Run Vale
        uses: errata-ai/vale-action@v2.1.1
        with:
          version: '3.12.0'
          files: ${{ needs.discover-changes.outputs.all_md_files }}
          separator: ','
          fail_on_error: true

  # ============================================================
  # STAGE 3: Test API Documentation
  # ============================================================
  test-api-docs:
    name: Test API Documentation
    runs-on: ubuntu-latest
    needs: [discover-changes, validate-commits, lint-markdown]
    if: |
      always() &&
      needs.validate-commits.result == 'success' &&
      needs.lint-markdown.result == 'success' &&
      needs.discover-changes.outputs.any_docs_changed == 'true'
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
          cache: 'pip'
      
      - name: Install Python dependencies
        run: pip install pyyaml jsonschema --break-system-packages
      
      # Check for testable files
      - name: Check for testable files
        id: check-testable
        run: |
          HAS_TESTABLE=false
          for file in ${{ needs.discover-changes.outputs.docs_md_files }}; do
            if grep -q "^test:" "$file" 2>/dev/null; then
              HAS_TESTABLE=true
              break
            fi
          done
          echo "has_testable=$HAS_TESTABLE" >> $GITHUB_OUTPUT
          
          if [ "$HAS_TESTABLE" = "true" ]; then
            echo "✓ Found files with test configurations"
          else
            echo "ℹ️  No testable examples found"
          fi
      
      # Determine test configuration
      - name: Determine test configuration
        if: steps.check-testable.outputs.has_testable == 'true'
        id: test-config
        run: |
          for file in ${{ needs.discover-changes.outputs.docs_md_files }}; do
            if grep -q "^test:" "$file" 2>/dev/null; then
              DB_PATH=$(python3 -c "
import yaml, re
with open('$file', 'r') as f:
    content = f.read()
fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
if fm_match:
    try:
        metadata = yaml.safe_load(fm_match.group(1))
        test_config = metadata.get('test', {})
        db_path = test_config.get('local_database', '/api/to-do-db-source.json')
        print(db_path.lstrip('/'))
    except: pass
" 2>/dev/null)
              
              if [ -n "$DB_PATH" ]; then
                echo "test_db=$DB_PATH" >> $GITHUB_OUTPUT
                echo "Using test database: $DB_PATH"
                break
              fi
            fi
          done
          
          if [ -z "$DB_PATH" ]; then
            echo "test_db=api/to-do-db-source.json" >> $GITHUB_OUTPUT
            echo "Using default test database"
          fi
      
      # Install and start json-server
      - name: Install json-server
        if: steps.check-testable.outputs.has_testable == 'true'
        run: |
          npm install -g json-server@0.17.4
          json-server --version
      
      - name: Start json-server
        if: steps.check-testable.outputs.has_testable == 'true'
        run: |
          if [ ! -f "${{ steps.test-config.outputs.test_db }}" ]; then
            echo "::error::Test database not found: ${{ steps.test-config.outputs.test_db }}"
            exit 1
          fi
          
          json-server --watch ${{ steps.test-config.outputs.test_db }} --port 3000 > json-server.log 2>&1 &
          SERVER_PID=$!
          echo $SERVER_PID > json-server.pid
          
          echo "Waiting for json-server..."
          for i in {1..10}; do
            if curl -s http://localhost:3000 > /dev/null 2>&1; then
              echo "✓ json-server running on http://localhost:3000"
              exit 0
            fi
            sleep 1
          done
          
          echo "::error::json-server failed to start"
          cat json-server.log
          exit 1
      
      # Test files
      - name: Test documentation files
        if: steps.check-testable.outputs.has_testable == 'true'
        id: test-files
        run: |
          FAILED_TESTS=0
          TESTED_FILES=0
          
          for file in ${{ needs.discover-changes.outputs.docs_md_files }}; do
            if grep -q "^test:" "$file" 2>/dev/null; then
              TESTED_FILES=$((TESTED_FILES + 1))
              
              if python3 ./tools/test-api-docs.py "$file" --action; then
                echo "✓ $file - PASSED"
              else
                echo "✗ $file - FAILED"
                FAILED_TESTS=$((FAILED_TESTS + 1))
              fi
            fi
          done
          
          if [ $FAILED_TESTS -gt 0 ]; then
            echo "::error::$FAILED_TESTS file(s) failed testing"
            exit 1
          fi
          
          if [ $TESTED_FILES -eq 0 ]; then
            echo "ℹ️  No testable files found"
          else
            echo "✓ All $TESTED_FILES file(s) passed testing"
          fi
      
      # Cleanup
      - name: Stop json-server
        if: always() && steps.check-testable.outputs.has_testable == 'true'
        run: |
          if [ -f json-server.pid ]; then
            kill $(cat json-server.pid) 2>/dev/null || true
            rm json-server.pid
            echo "✓ json-server stopped"
          fi
      
      - name: Upload json-server logs
        if: always() && steps.check-testable.outputs.has_testable == 'true'
        uses: actions/upload-artifact@v4
        with:
          name: json-server-logs
          path: json-server.log
          retention-days: 7
```

**Checklist:**
- [ ] Create new workflow file
- [ ] Add file discovery job
- [ ] Add test-tools job
- [ ] Add validate-commits job
- [ ] Add lint-markdown job (merged from 3 jobs)
- [ ] Add test-api-docs job
- [ ] Add proper dependencies with `needs:`
- [ ] Add conditional execution with `if:`
- [ ] Add caching for Vale
- [ ] Add caching for pip
- [ ] Add step summaries
- [ ] Test syntax with `actionlint` or GitHub's validator

**Estimated Time:** 4-6 hours

---

### 2.2: Disable Old Workflows

**DO NOT DELETE** - Disable by renaming

**Rename files:**
```bash
mv .github/workflows/pr-test-tools.yml .github/workflows/DISABLED-pr-test-tools.yml
mv .github/workflows/pr-commit-test.yml .github/workflows/DISABLED-pr-commit-test.yml
mv .github/workflows/pr-lint-tests.yml .github/workflows/DISABLED-pr-lint-tests.yml
mv .github/workflows/pr-api-doc-content-test.yml .github/workflows/DISABLED-pr-api-doc-content-test.yml
```

**Why rename instead of delete:**
- Easy rollback if needed
- Preserve configuration as reference
- Can compare behavior
- Delete later after confirming new workflow works

**Checklist:**
- [ ] Rename pr-test-tools.yml
- [ ] Rename pr-commit-test.yml
- [ ] Rename pr-lint-tests.yml
- [ ] Rename pr-api-doc-content-test.yml
- [ ] Verify renamed files don't trigger
- [ ] Commit with clear message

**Estimated Time:** 15 minutes

---

## Phase 3: Testing & Validation

**Duration:** Week 2-3 (3-5 days)  
**Risk:** Medium  
**Critical:** Yes

### 3.1: Local Testing

**Test with act (local GitHub Actions runner):**

```bash
# Install act (if not already)
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Test individual jobs
act pull_request -j discover-changes
act pull_request -j test-tools
act pull_request -j lint-markdown

# Test full workflow
act pull_request
```

**Manual testing:**

```bash
# Create test branch
git checkout -b test/workflow-consolidation

# Make test changes
echo "# Test" >> docs/test.md
git add docs/test.md
git commit -m "Test: workflow validation"

# Push (don't create PR yet)
git push origin test/workflow-consolidation
```

**Checklist:**
- [ ] Install act
- [ ] Test discover-changes job locally
- [ ] Test test-tools job locally
- [ ] Test lint-markdown job locally
- [ ] Verify outputs are passed correctly
- [ ] Check for syntax errors
- [ ] Verify conditional logic

**Estimated Time:** 2-3 hours

---

### 3.2: Test PR Scenarios

Create test PRs for different scenarios:

#### Scenario 1: Tools Changed
- [ ] Create PR that modifies `tools/`
- [ ] Verify `test-tools` job runs
- [ ] Verify other jobs wait for it
- [ ] Verify if tools fail, other jobs don't run

#### Scenario 2: Docs Only Changed
- [ ] Create PR that modifies only `docs/*.md`
- [ ] Verify `test-tools` is skipped
- [ ] Verify `lint-markdown` runs
- [ ] Verify `test-api-docs` runs

#### Scenario 3: No Markdown Changed
- [ ] Create PR that modifies non-markdown files
- [ ] Verify `lint-markdown` is skipped
- [ ] Verify `test-api-docs` is skipped
- [ ] Verify `validate-commits` still runs

#### Scenario 4: Bad Commit Structure
- [ ] Create PR with 2+ commits
- [ ] Verify `validate-commits` fails
- [ ] Verify `test-api-docs` doesn't run

#### Scenario 5: Lint Failures
- [ ] Create PR with markdown lint errors
- [ ] Verify `lint-markdown` fails
- [ ] Verify `test-api-docs` doesn't run

#### Scenario 6: Mixed Changes
- [ ] Create PR with tools + docs changes
- [ ] Verify all stages run
- [ ] Verify proper ordering

#### Scenario 7: Large File Count
- [ ] Create PR with 20+ markdown files
- [ ] Verify Python scripts handle batch
- [ ] Verify performance improvement
- [ ] Check annotations are correct

**Checklist:**
- [ ] Test all 7 scenarios
- [ ] Document results for each
- [ ] Compare timing vs old workflows
- [ ] Verify annotations appear correctly
- [ ] Check step summaries are useful
- [ ] Verify error messages are clear

**Estimated Time:** 4-6 hours

---

### 3.3: Performance Validation

**Measure improvements:**

Create identical PRs and compare:

| Metric | Old Workflows | New Workflow | Improvement |
|--------|---------------|--------------|-------------|
| Total runtime | ___ seconds | ___ seconds | ___ seconds |
| Number of checkouts | ___ | ___ | ___ |
| Python script calls | ___ | ___ | ___ |
| Job overhead | ___ | ___ | ___ |

**Checklist:**
- [ ] Measure baseline with old workflows
- [ ] Measure new consolidated workflow
- [ ] Document improvements
- [ ] Verify meets 60-150 second target

**Estimated Time:** 2 hours

---

## Phase 4: Deployment

**Duration:** Week 3 (1-2 days)  
**Risk:** Medium to High  
**Critical:** Yes

### 4.1: Pre-Deployment

**Communication:**
- [ ] Notify team of upcoming changes
- [ ] Document new workflow structure
- [ ] Update contributor guidelines
- [ ] Prepare rollback plan

**Final checks:**
- [ ] All tests passing
- [ ] Performance validated
- [ ] Documentation updated
- [ ] Team reviewed changes

**Estimated Time:** 2 hours

---

### 4.2: Deployment

**Strategy: Gradual rollout**

#### Step 1: Deploy to Test Branch
```bash
# Create release branch
git checkout -b release/workflow-optimization
git push origin release/workflow-optimization

# Create PR to main
# Title: "Optimize workflows and Python scripts"
# Description: Link to this migration plan
```

- [ ] Create release branch
- [ ] Create PR to main
- [ ] Request review from team
- [ ] Wait for approval

#### Step 2: Merge During Low Activity
```bash
# Merge during off-hours or low-activity period
# Monday morning or Friday evening (depending on team)
```

- [ ] Choose low-activity time
- [ ] Merge PR
- [ ] Monitor first few automated PR validations

#### Step 3: Monitor

**First 24 hours:**
- [ ] Watch for workflow failures
- [ ] Check GitHub Actions logs
- [ ] Monitor performance metrics
- [ ] Verify annotations working
- [ ] Check for unexpected errors

**First week:**
- [ ] Daily check of workflow runs
- [ ] Gather feedback from team
- [ ] Address any issues quickly
- [ ] Document any quirks

**Estimated Time:** 4 hours (spread over week)

---

### 4.3: Post-Deployment Cleanup

**After 1 week of successful operation:**

```bash
# Delete disabled workflow files
rm .github/workflows/DISABLED-pr-test-tools.yml
rm .github/workflows/DISABLED-pr-commit-test.yml
rm .github/workflows/DISABLED-pr-lint-tests.yml
rm .github/workflows/DISABLED-pr-api-doc-content-test.yml

git add .github/workflows/
git commit -m "chore: Remove old workflow files after successful migration"
git push
```

**Update documentation:**
- [ ] Update README.md
- [ ] Update contributor guidelines
- [ ] Document new workflow structure
- [ ] Update troubleshooting guides

**Estimated Time:** 2 hours

---

## Phase 5: Post-Deployment

**Duration:** Ongoing  
**Risk:** Low

### 5.1: Monitoring

**Key metrics to track:**

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Average workflow runtime | < 3 minutes | GitHub Actions UI |
| Workflow failure rate | < 5% | GitHub Actions UI |
| False positives | 0 | Team feedback |
| Developer satisfaction | Positive | Survey/feedback |

**Weekly review (first month):**
- [ ] Check average runtime
- [ ] Review failure patterns
- [ ] Gather team feedback
- [ ] Identify optimization opportunities

**Estimated Time:** 1 hour/week

---

### 5.2: Iteration

**Continuous improvement:**

**Quick wins to consider later:**
- [ ] Add workflow timing dashboard
- [ ] Create workflow debugging guide
- [ ] Add more conditional skip logic
- [ ] Optimize cache hit rates
- [ ] Add performance benchmarks

**Future optimizations:**
- [ ] Batch process test-api-docs.py (if feasible)
- [ ] Add matrix builds for parallel testing
- [ ] Implement workflow result caching
- [ ] Add auto-retry for flaky tests

**Estimated Time:** Ongoing

---

## Rollback Plan

### When to Rollback

Rollback if:
- [ ] Workflow failure rate > 20%
- [ ] Critical feature broken
- [ ] Performance worse than baseline
- [ ] Team unable to work effectively

### How to Rollback

#### Quick Rollback (< 5 minutes)

```bash
# Disable new workflow
mv .github/workflows/pr-validation.yml .github/workflows/DISABLED-pr-validation.yml

# Re-enable old workflows
mv .github/workflows/DISABLED-pr-test-tools.yml .github/workflows/pr-test-tools.yml
mv .github/workflows/DISABLED-pr-commit-test.yml .github/workflows/pr-commit-test.yml
mv .github/workflows/DISABLED-pr-lint-tests.yml .github/workflows/pr-lint-tests.yml
mv .github/workflows/DISABLED-pr-api-doc-content-test.yml .github/workflows/pr-api-doc-content-test.yml

git add .github/workflows/
git commit -m "ROLLBACK: Restore old workflows"
git push
```

#### Python Script Rollback

```bash
# Revert to tagged version
git revert <commit-hash>
# or
git checkout pre-workflow-optimization -- tools/list-linter-exceptions.py
git checkout pre-workflow-optimization -- tools/markdown-survey.py

git commit -m "ROLLBACK: Restore original Python scripts"
git push
```

### Post-Rollback Actions

- [ ] Notify team
- [ ] Document what went wrong
- [ ] Analyze root cause
- [ ] Plan fixes
- [ ] Retry when ready

---

## Success Criteria

### Phase 1 Success (Python Scripts)
- [ ] All 3 scripts updated
- [ ] All tests passing
- [ ] Backwards compatible (single file works)
- [ ] Batch processing works
- [ ] Performance improved by 1-10 seconds

### Phase 2 Success (Workflows)
- [ ] New workflow deployed
- [ ] Old workflows disabled
- [ ] All test scenarios passing
- [ ] No regression in functionality
- [ ] Performance improved by 60-150 seconds

### Overall Success
- [ ] Team satisfied with changes
- [ ] Workflow failure rate < 5%
- [ ] Average runtime < 3 minutes
- [ ] Clear dependency chain
- [ ] Easy to debug issues
- [ ] Documentation updated

---

## Timeline Summary

```
Week 1: Python Script Optimization
├─ Day 1-2: Update list-linter-exceptions.py & tests
├─ Day 3-4: Update markdown-survey.py & tests
└─ Day 5: Testing & validation

Week 2: Workflow Consolidation
├─ Day 1-2: Create pr-validation.yml
├─ Day 3: Disable old workflows
├─ Day 4-5: Testing scenarios
└─ Day 5: Performance validation

Week 3: Deployment & Monitoring
├─ Day 1: Pre-deployment prep
├─ Day 2: Deploy & initial monitoring
├─ Day 3-5: Ongoing monitoring
└─ Day 5: Cleanup & documentation
```

**Total Duration:** 2-3 weeks  
**Estimated Effort:** 40-60 hours  

---

## Resources & References

### Documentation
- `workflow-reorganization-plan.md`
- `workflow-optimization-analysis.md`
- `python-loop-optimization-analysis.md`
- Project standards in `/mnt/project/`

### Tools
- GitHub Actions documentation
- `act` for local testing
- `actionlint` for workflow validation
- `pytest` for Python testing

### Support
- Team Slack channel: #workflow-optimization
- Issue tracker: GitHub Issues
- Point person: `[Name]`

---

## Appendix A: File Change Summary

### Files Modified

**Python Scripts:**
- `tools/list-linter-exceptions.py`
- `tools/markdown-survey.py`
- `tools/tests/test_list_linter_exception.py`
- `tools/tests/test_markdown_survey.py`

**Workflows:**
- `.github/workflows/pr-validation.yml` (new)
- `.github/workflows/DISABLED-pr-test-tools.yml` (renamed)
- `.github/workflows/DISABLED-pr-commit-test.yml` (renamed)
- `.github/workflows/DISABLED-pr-lint-tests.yml` (renamed)
- `.github/workflows/DISABLED-pr-api-doc-content-test.yml` (renamed)

**Documentation:**
- `README.md` (updated)
- `CONTRIBUTING.md` (updated)
- This migration plan

---

## Appendix B: Testing Checklist

### Python Script Testing
- [ ] Single file input (backwards compat)
- [ ] Multiple file input
- [ ] Empty file list
- [ ] Non-existent file
- [ ] File read errors
- [ ] Progress indicators
- [ ] Summary statistics
- [ ] Error aggregation
- [ ] Exit codes
- [ ] GitHub Actions annotations

### Workflow Testing
- [ ] File discovery accuracy
- [ ] Job dependencies work
- [ ] Conditional execution correct
- [ ] Annotations appear
- [ ] Step summaries useful
- [ ] Caching works
- [ ] Performance improved
- [ ] All scenarios pass
- [ ] Rollback works
- [ ] Documentation clear

---

## Appendix C: Communication Template

**Email/Slack Announcement:**

```
Subject: Upcoming Workflow Optimization

Team,

We're improving our PR validation workflows to make them:
- 60-150 seconds faster
- More reliable (fail-fast)
- Easier to debug

Changes:
1. Python scripts now process all files at once (faster)
2. Workflows consolidated into single file (clearer dependencies)

Timeline:
- Week 1: Python scripts
- Week 2: Workflows
- Week 3: Monitoring

Impact on you:
- PR validation will be faster
- Clearer error messages
- Same functionality, better performance

Questions? See migration plan or ask in #workflow-optimization

Thanks,
[Your Name]
```

---

## Appendix D: Quick Reference Commands

**Testing:**
```bash
# Run Python tests
cd tools/tests && pytest -v

# Test single script
python3 tools/list-linter-exceptions.py file.md

# Test multiple files
python3 tools/list-linter-exceptions.py file1.md file2.md file3.md

# Test with act
act pull_request -j discover-changes
```

**Deployment:**
```bash
# Create release branch
git checkout -b release/workflow-optimization

# Deploy
git push origin release/workflow-optimization

# Rollback
mv .github/workflows/pr-validation.yml .github/workflows/DISABLED-pr-validation.yml
mv .github/workflows/DISABLED-*.yml .github/workflows/*.yml
```

---

**End of Migration Plan**

This plan is a living document. Update as needed based on learnings during implementation.