<!-- vale off -->
<!-- markdownlint-disable -->
# Action Flag Standardization Summary

**Date:** 2024-12-08  
**Change Type:** Breaking change (requires migration)  
**Scope:** All Python scripts in tools/ with --action flag

## Problem Fixed

The `--action` flag used `nargs='?'` which caused argument parsing ambiguity:

```bash
# BROKEN: file1.md interpreted as value for --action
script.py --action file1.md file2.md

# WORKAROUND: Had to put files first
script.py file1.md file2.md --action
```

## Solution Implemented

Changed `--action` to **require an explicit level** (no optional value):

```python
# OLD (ambiguous)
parser.add_argument(
    '--action', '-a',
    nargs='?',              # Optional value
    const='warning',        # Default if flag present without value
    default=None,
    choices=['all', 'warning', 'error']
)

# NEW (explicit)
parser.add_argument(
    '--action', '-a',
    type=str,
    default=None,
    choices=['all', 'warning', 'error'],
    help='Output GitHub Actions annotations at specified level'
)
```

## Files Updated

### Python Scripts (3 files)

1. **list-linter-exceptions.py**
   - Removed `nargs='?'` and `const='warning'`
   - Updated help text and examples
   - Location: `/mnt/user-data/outputs/list-linter-exceptions.py`

2. **markdown-survey.py**
   - Removed `nargs='?'` and `const='warning'`
   - Updated help text and examples
   - Location: `/mnt/user-data/outputs/markdown-survey.py`

3. **test-filenames.py**
   - Removed `nargs='?'` and `const='warning'`
   - Updated help text and examples
   - Location: `/mnt/user-data/outputs/test-filenames.py`

### Workflow File (1 file)

4. **pr-validation.yml**
   - Updated all 4 script calls to include explicit level
   - Location: `/mnt/user-data/outputs/pr-validation.yml`

## Migration Required

### Before (old syntax)

```bash
# These will now ERROR
python3 tools/list-linter-exceptions.py --action file.md
python3 tools/markdown-survey.py --action docs/*.md
python3 tools/test-filenames.py --action
```

### After (new syntax)

```bash
# Must specify level explicitly
python3 tools/list-linter-exceptions.py --action warning file.md
python3 tools/markdown-survey.py --action warning docs/*.md
python3 tools/test-filenames.py --action warning
```

## Workflow Changes

**pr-validation.yml** updated in 4 locations:

### Line 238: test-filenames
```yaml
# OLD
run: python3 tools/test-filenames.py --action

# NEW
run: python3 tools/test-filenames.py --action warning
```

### Line 245: list-linter-exceptions
```yaml
# OLD
python3 tools/list-linter-exceptions.py --action $files_space

# NEW
python3 tools/list-linter-exceptions.py --action warning $files_space
```

### Line 252: markdown-survey
```yaml
# OLD
python3 tools/markdown-survey.py --action $files_space

# NEW
python3 tools/markdown-survey.py --action warning $files_space
```

### Line 426: test-api-docs
```yaml
# OLD
if python3 ./tools/test-api-docs.py "$file" --action; then

# NEW
if python3 ./tools/test-api-docs.py "$file" --action warning; then
```

## Benefits

1. **No ambiguity** - Files can be in any order
2. **Explicit intent** - Clear what annotation level is desired
3. **Robust parsing** - No more argparse confusion
4. **Standard pattern** - Matches common CLI conventions

## Usage Examples

### list-linter-exceptions.py

```bash
# Normal mode (no annotations)
python3 tools/list-linter-exceptions.py file1.md file2.md

# GitHub Actions mode - warning level
python3 tools/list-linter-exceptions.py file1.md --action warning

# GitHub Actions mode - all levels
python3 tools/list-linter-exceptions.py file1.md --action all

# GitHub Actions mode - errors only
python3 tools/list-linter-exceptions.py file1.md --action error

# Files can be anywhere
python3 tools/list-linter-exceptions.py --action warning file1.md file2.md
```

### markdown-survey.py

```bash
# Normal mode
python3 tools/markdown-survey.py docs/*.md

# GitHub Actions mode
python3 tools/markdown-survey.py docs/*.md --action warning
python3 tools/markdown-survey.py --action warning docs/*.md  # Also works!
```

### test-filenames.py

```bash
# Normal mode
CHANGED_FILES="file1.md,file2.md" python3 tools/test-filenames.py

# GitHub Actions mode
CHANGED_FILES="file1.md,file2.md" python3 tools/test-filenames.py --action warning
```

## Breaking Changes

### Scripts

Any existing scripts or workflows calling these tools with `--action` alone will break:

```bash
# WILL BREAK
script.py --action file.md

# FIX: Add explicit level
script.py --action warning file.md
```

### Migration Checklist

If you have other workflows or scripts using these tools:

- [ ] Find all calls with `--action` alone
- [ ] Add explicit level: `warning`, `error`, or `all`
- [ ] Test updated calls
- [ ] Update any documentation

## Test Plan

### Manual Testing

```bash
# Test normal mode
python3 tools/list-linter-exceptions.py test.md
python3 tools/markdown-survey.py test.md
CHANGED_FILES="test.md" python3 tools/test-filenames.py

# Test with --action (should error without level)
python3 tools/list-linter-exceptions.py --action test.md  # Should fail

# Test with explicit level
python3 tools/list-linter-exceptions.py --action warning test.md
python3 tools/list-linter-exceptions.py test.md --action warning  # Both orders work

# Test all levels
python3 tools/list-linter-exceptions.py --action all test.md
python3 tools/list-linter-exceptions.py --action warning test.md
python3 tools/list-linter-exceptions.py --action error test.md
```

### Workflow Testing

Create test PR and verify:
- [ ] test-filenames runs with `--action warning`
- [ ] list-linter-exceptions runs with `--action warning`
- [ ] markdown-survey runs with `--action warning`
- [ ] test-api-docs runs with `--action warning`
- [ ] No parsing errors
- [ ] Annotations appear correctly

## Deployment Notes

### Phase 2 Workflow

These changes are part of Phase 2 workflow consolidation and will be deployed together with:
- pr-validation.yml (consolidated workflow)
- Updated Python scripts

### Backward Compatibility

**None** - This is a breaking change. All callers must be updated simultaneously.

### Rollback Plan

If issues arise, rollback both workflow and scripts together:
```bash
# Restore old versions from DISABLED-* workflows
# Or revert Git commit
git revert <commit-hash>
```

## Documentation Updates Needed

Once deployed, update:
- [ ] README.md (if scripts documented there)
- [ ] tools/README.md
- [ ] Any workflow documentation
- [ ] CONTRIBUTING.md (if applicable)

## Questions & Answers

**Q: Why not keep backward compatibility with optional value?**  
A: The `nargs='?'` pattern is fundamentally ambiguous with positional arguments. No clean way to maintain compatibility.

**Q: What if I forget the level?**  
A: argparse will show an error: `error: argument --action: expected one argument`

**Q: Can I still use short form `-a`?**  
A: Yes! `-a warning` works the same as `--action warning`

**Q: What level should I use?**  
A: 
- `warning` - Most common, shows warnings and errors (default choice)
- `error` - Only show critical errors
- `all` - Show notices, warnings, and errors (verbose)

## Related Files

- Phase 2 Implementation Guide: `phase-2-implementation-guide.md`
- Phase 2 Testing Checklist: `phase-2-testing-checklist.md`
- Workflow Analysis: `current-workflow-analysis.md`

---

**Status:** Ready for testing  
**Next Step:** Test in workflow, then deploy with Phase 2
