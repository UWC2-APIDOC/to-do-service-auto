#!/usr/bin/env python3
"""
Tests for get-database-path.py

Covers:
- Extracting database path from front matter
- Handling files with no database path
- Handling files with no front matter
- Handling files with no test section
- Handling invalid YAML
- Handling missing files
- Stripping leading slashes from paths

Run with:
    python3 test_get_database_path.py
    pytest test_get_database_path.py -v
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the module we're testing
# We import the function directly, not running as subprocess
# This allows us to test the function logic directly
import importlib.util
spec = importlib.util.spec_from_file_location(
    "get_database_path",
    Path(__file__).parent.parent / "get-database-path.py"
)
get_database_path_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(get_database_path_module)

get_database_path_from_metadata = get_database_path_module.get_database_path_from_metadata
DEFAULT_DATABASE_PATH = get_database_path_module.DEFAULT_DATABASE_PATH


def test_extract_database_path_with_leading_slash():
    """Test extracting database path that has a leading slash."""
    print("\n" + "="*60)
    print("TEST: extract database path with leading slash")
    print("="*60)
    
    # Create test file with leading slash in database path
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "sample.md"
    
    # This file should have: local_database: /api/to-do-db-source.json
    db_path = get_database_path_from_metadata(test_file)
    
    assert db_path is not None, "Should extract database path"
    assert not db_path.startswith('/'), f"Should strip leading slash, got: {db_path}"
    print(f"  SUCCESS: Extracted path without leading slash: {db_path}")
    
    print("  ✓ Database path extraction with slash stripping passed")


def test_extract_database_path_without_leading_slash():
    """Test extracting database path that has no leading slash."""
    print("\n" + "="*60)
    print("TEST: extract database path without leading slash")
    print("="*60)
    
    # Create test content with no leading slash
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "temp_no_slash.md"
    test_content = """---
test:
  local_database: api/custom-db.json
---
# Test
"""
    test_file.write_text(test_content)
    
    try:
        db_path = get_database_path_from_metadata(test_file)
        
        assert db_path is not None, "Should extract database path"
        assert db_path == "api/custom-db.json", f"Expected 'api/custom-db.json', got: {db_path}"
        print(f"  SUCCESS: Extracted path correctly: {db_path}")
        
        print("  ✓ Database path without leading slash passed")
    finally:
        test_file.unlink()


def test_file_with_no_database_path():
    """Test file with test section but no local_database field."""
    print("\n" + "="*60)
    print("TEST: file with no database path")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "temp_no_db.md"
    test_content = """---
test:
  testable:
    - GET /api/users
  server_url: localhost:3000
---
# Test
"""
    test_file.write_text(test_content)
    
    try:
        db_path = get_database_path_from_metadata(test_file)
        
        assert db_path is None, "Should return None when no database path present"
        print("  SUCCESS: Correctly returned None for missing database path")
        
        print("  ✓ No database path handling passed")
    finally:
        test_file.unlink()


def test_file_with_no_test_section():
    """Test file with front matter but no test section."""
    print("\n" + "="*60)
    print("TEST: file with no test section")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "temp_no_test.md"
    test_content = """---
title: Some Document
layout: default
---
# Test
"""
    test_file.write_text(test_content)
    
    try:
        db_path = get_database_path_from_metadata(test_file)
        
        assert db_path is None, "Should return None when no test section present"
        print("  SUCCESS: Correctly returned None for missing test section")
        
        print("  ✓ No test section handling passed")
    finally:
        test_file.unlink()


def test_file_with_no_front_matter():
    """Test file with no front matter at all."""
    print("\n" + "="*60)
    print("TEST: file with no front matter")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "temp_no_fm.md"
    test_content = "# Just a heading\n\nNo front matter here."
    test_file.write_text(test_content)
    
    try:
        db_path = get_database_path_from_metadata(test_file)
        
        assert db_path is None, "Should return None when no front matter present"
        print("  SUCCESS: Correctly returned None for missing front matter")
        
        print("  ✓ No front matter handling passed")
    finally:
        test_file.unlink()


def test_file_with_invalid_yaml():
    """Test file with malformed YAML in front matter."""
    print("\n" + "="*60)
    print("TEST: file with invalid YAML")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "temp_bad_yaml.md"
    test_content = """---
test: [unclosed list
  local_database: /api/db.json
---
# Test
"""
    test_file.write_text(test_content)
    
    try:
        db_path = get_database_path_from_metadata(test_file)
        
        assert db_path is None, "Should return None for invalid YAML"
        print("  SUCCESS: Correctly returned None for invalid YAML")
        
        print("  ✓ Invalid YAML handling passed")
    finally:
        test_file.unlink()


def test_nonexistent_file():
    """Test handling of file that doesn't exist."""
    print("\n" + "="*60)
    print("TEST: nonexistent file")
    print("="*60)
    
    test_file = Path("/nonexistent/file/path.md")
    
    db_path = get_database_path_from_metadata(test_file)
    
    assert db_path is None, "Should return None for nonexistent file"
    print("  SUCCESS: Correctly returned None for nonexistent file")
    
    print("  ✓ Nonexistent file handling passed")


def test_database_path_with_multiple_slashes():
    """Test database path with multiple leading slashes."""
    print("\n" + "="*60)
    print("TEST: database path with multiple leading slashes")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "temp_multi_slash.md"
    test_content = """---
test:
  local_database: ///api/db.json
---
# Test
"""
    test_file.write_text(test_content)
    
    try:
        db_path = get_database_path_from_metadata(test_file)
        
        assert db_path is not None, "Should extract database path"
        assert db_path == "api/db.json", f"Should strip all leading slashes, got: {db_path}"
        print(f"  SUCCESS: Correctly stripped multiple slashes: {db_path}")
        
        print("  ✓ Multiple slash handling passed")
    finally:
        test_file.unlink()


def test_database_path_as_non_string():
    """Test handling when local_database is not a string."""
    print("\n" + "="*60)
    print("TEST: database path as non-string type")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "temp_non_string.md"
    test_content = """---
test:
  local_database: 123
---
# Test
"""
    test_file.write_text(test_content)
    
    try:
        db_path = get_database_path_from_metadata(test_file)
        
        assert db_path is None, "Should return None for non-string database path"
        print("  SUCCESS: Correctly returned None for non-string value")
        
        print("  ✓ Non-string type handling passed")
    finally:
        test_file.unlink()


def test_default_constant_value():
    """Test that the DEFAULT_DATABASE_PATH constant is correct."""
    print("\n" + "="*60)
    print("TEST: default database path constant")
    print("="*60)
    
    expected = "api/to-do-db-source.json"
    assert DEFAULT_DATABASE_PATH == expected, \
        f"Default should be '{expected}', got: {DEFAULT_DATABASE_PATH}"
    
    print(f"  SUCCESS: Default constant is correct: {DEFAULT_DATABASE_PATH}")
    print("  ✓ Default constant test passed")


def run_all_tests():
    """Run all test functions and report results."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR get-database-path.py")
    print("="*70)
    
    tests = [
        test_extract_database_path_with_leading_slash,
        test_extract_database_path_without_leading_slash,
        test_file_with_no_database_path,
        test_file_with_no_test_section,
        test_file_with_no_front_matter,
        test_file_with_invalid_yaml,
        test_nonexistent_file,
        test_database_path_with_multiple_slashes,
        test_database_path_as_non_string,
        test_default_constant_value,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"\n  ✗ FAILED: {test_func.__name__}")
            print(f"    {str(e)}")
        except Exception as e:
            failed += 1
            print(f"\n  ✗ ERROR: {test_func.__name__}")
            print(f"    {type(e).__name__}: {str(e)}")
    
    print("\n" + "="*70)
    print(f" TEST SUMMARY: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
# end of file tools/tests/test_get_database_path.py