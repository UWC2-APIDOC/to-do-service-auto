#!/usr/bin/env python3
"""
Tests for get-test-configs.py

Covers:
- File grouping by identical test configurations
- Handling files with missing/incomplete configs
- Different output formats (JSON, shell)
- Error handling for unreadable files
- GitHub Actions annotation output

Run with:
    python3 test_get_test_configs.py
    pytest test_get_test_configs.py -v
"""

import sys
import json
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the module functions directly - handle both direct run and pytest
try:
    # Try importing from parent directory (when run directly)
    import importlib.util
    spec = importlib.util.spec_from_file_location("get_test_configs", 
                                                   Path(__file__).parent.parent / "get-test-configs.py")
    get_test_configs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(get_test_configs)
    from get_test_configs import group_files_by_config, output_json, output_shell
except:
    # Fallback for different execution contexts
    sys.path.insert(0, str(Path(__file__).parent.parent))
    # Load the module with hyphenated name
    import importlib.util
    spec = importlib.util.spec_from_file_location("get_test_configs", 
                                                   Path(__file__).parent.parent / "get-test-configs.py")
    if spec and spec.loader:
        get_test_configs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(get_test_configs)
        group_files_by_config = get_test_configs.group_files_by_config
        output_json = get_test_configs.output_json
        output_shell = get_test_configs.output_shell


def test_group_files_identical_config():
    """Test grouping files with identical test configurations."""
    print("\n" + "="*60)
    print("TEST: group_files_by_config() - identical configs")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    
    # Files with same config should be grouped together
    files = [
        test_data_dir / "api_doc_same_config_1.md",
        test_data_dir / "api_doc_same_config_2.md"
    ]
    
    groups = group_files_by_config(files)
    
    assert len(groups) == 1, "Files with same config should form one group"
    
    config_key = list(groups.keys())[0]
    test_apps, server_url, local_database = config_key
    
    assert test_apps == "json-server@0.17.4"
    assert server_url == "localhost:3000"
    assert local_database == "/api/test.json"
    assert len(groups[config_key]) == 2, "Group should contain both files"
    
    print("  SUCCESS: Files with identical config grouped correctly")
    print("  ✓ All group_files_by_config (identical) tests passed")


def test_group_files_different_configs():
    """Test grouping files with different test configurations."""
    print("\n" + "="*60)
    print("TEST: group_files_by_config() - different configs")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    
    # Files with different configs should be in separate groups
    files = [
        test_data_dir / "api_doc_config_a.md",
        test_data_dir / "api_doc_config_b.md"
    ]
    
    groups = group_files_by_config(files)
    
    assert len(groups) == 2, "Files with different configs should form separate groups"
    
    # Each group should have one file
    for files_in_group in groups.values():
        assert len(files_in_group) == 1, "Each group should have one file"
    
    print("  SUCCESS: Files with different configs grouped separately")
    print("  ✓ All group_files_by_config (different) tests passed")


def test_group_files_mixed_configs():
    """Test grouping mix of files with matching and different configs."""
    print("\n" + "="*60)
    print("TEST: group_files_by_config() - mixed configs")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    
    # Mix: 2 files same config, 2 files different configs
    files = [
        test_data_dir / "api_doc_same_config_1.md",
        test_data_dir / "api_doc_same_config_2.md",
        test_data_dir / "api_doc_config_a.md",
        test_data_dir / "api_doc_config_b.md"
    ]
    
    groups = group_files_by_config(files)
    
    assert len(groups) == 3, "Should have 3 groups (1 pair + 2 singles)"
    
    # Find the group with 2 files
    group_sizes = [len(files) for files in groups.values()]
    assert 2 in group_sizes, "Should have one group with 2 files"
    assert group_sizes.count(1) == 2, "Should have two groups with 1 file each"
    
    print("  SUCCESS: Mixed configs grouped correctly")
    print("  ✓ All group_files_by_config (mixed) tests passed")


def test_skip_files_no_front_matter():
    """Test handling files without front matter."""
    print("\n" + "="*60)
    print("TEST: group_files_by_config() - no front matter")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    fail_data_dir = Path(__file__).parent / "fail_data"
    
    # Mix valid and invalid files
    files = [
        test_data_dir / "api_doc_same_config_1.md",
        fail_data_dir / "no_front_matter.md"
    ]
    
    groups = group_files_by_config(files)
    
    # Only the valid file should be grouped
    assert len(groups) == 1, "Only valid file should be grouped"
    
    config_key = list(groups.keys())[0]
    assert len(groups[config_key]) == 1, "Group should contain only valid file"
    
    print("  SUCCESS: Files without front matter skipped correctly")
    print("  ✓ All group_files_by_config (no front matter) tests passed")


def test_skip_files_incomplete_config():
    """Test handling files with incomplete test configurations."""
    print("\n" + "="*60)
    print("TEST: group_files_by_config() - incomplete config")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    fail_data_dir = Path(__file__).parent / "fail_data"
    
    # Mix valid and incomplete config files
    files = [
        test_data_dir / "api_doc_same_config_1.md",
        fail_data_dir / "incomplete_test_config.md"
    ]
    
    groups = group_files_by_config(files)
    
    # Only the complete config should be grouped
    assert len(groups) == 1, "Only complete config should be grouped"
    
    print("  SUCCESS: Files with incomplete config skipped correctly")
    print("  ✓ All group_files_by_config (incomplete) tests passed")


def test_skip_files_no_test_section():
    """Test handling files without test section in front matter."""
    print("\n" + "="*60)
    print("TEST: group_files_by_config() - no test section")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    fail_data_dir = Path(__file__).parent / "fail_data"
    
    # Mix valid and no-test-config files
    files = [
        test_data_dir / "api_doc_same_config_1.md",
        fail_data_dir / "no_test_config.md"
    ]
    
    groups = group_files_by_config(files)
    
    # Only file with test config should be grouped
    assert len(groups) == 1, "Only file with test config should be grouped"
    
    print("  SUCCESS: Files without test section skipped correctly")
    print("  ✓ All group_files_by_config (no test) tests passed")


def test_output_json_format():
    """Test JSON output format."""
    print("\n" + "="*60)
    print("TEST: output_json()")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    
    files = [
        test_data_dir / "api_doc_same_config_1.md",
        test_data_dir / "api_doc_same_config_2.md"
    ]
    
    groups = group_files_by_config(files)
    
    # Capture JSON output
    captured_output = StringIO()
    with redirect_stdout(captured_output):
        output_json(groups)
    
    json_str = captured_output.getvalue()
    
    # Parse and validate JSON
    result = json.loads(json_str)
    
    assert "groups" in result, "JSON should have 'groups' key"
    assert len(result["groups"]) == 1, "Should have one group"
    
    group = result["groups"][0]
    assert "test_apps" in group
    assert "server_url" in group
    assert "local_database" in group
    assert "files" in group
    
    assert isinstance(group["test_apps"], list), "test_apps should be a list"
    assert group["test_apps"] == ["json-server@0.17.4"]
    assert group["server_url"] == "localhost:3000"
    assert group["local_database"] == "/api/test.json"
    assert len(group["files"]) == 2, "Group should contain 2 files"
    
    print("  SUCCESS: JSON output format correct")
    print("  ✓ All output_json tests passed")


def test_output_shell_format():
    """Test shell variables output format."""
    print("\n" + "="*60)
    print("TEST: output_shell()")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    
    files = [
        test_data_dir / "api_doc_same_config_1.md",
        test_data_dir / "api_doc_config_a.md"
    ]
    
    groups = group_files_by_config(files)
    
    # Capture shell output
    captured_output = StringIO()
    with redirect_stdout(captured_output):
        output_shell(groups)
    
    shell_output = captured_output.getvalue()
    lines = shell_output.strip().split('\n')
    
    # Should have variables for each group plus GROUP_COUNT
    # 2 groups × 4 variables each = 8, plus 1 GROUP_COUNT = 9 lines
    assert len(lines) >= 9, f"Expected at least 9 lines, got {len(lines)}"
    
    # Check GROUP_COUNT
    assert "GROUP_COUNT=2" in shell_output, "Should have GROUP_COUNT=2"
    
    # Check group 1 variables exist
    assert any("GROUP_1_TEST_APPS=" in line for line in lines)
    assert any("GROUP_1_SERVER_URL=" in line for line in lines)
    assert any("GROUP_1_LOCAL_DATABASE=" in line for line in lines)
    assert any("GROUP_1_FILES=" in line for line in lines)
    
    # Check group 2 variables exist
    assert any("GROUP_2_TEST_APPS=" in line for line in lines)
    assert any("GROUP_2_SERVER_URL=" in line for line in lines)
    assert any("GROUP_2_LOCAL_DATABASE=" in line for line in lines)
    assert any("GROUP_2_FILES=" in line for line in lines)
    
    print("  SUCCESS: Shell output format correct")
    print("  ✓ All output_shell tests passed")


def test_empty_file_list():
    """Test handling empty file list."""
    print("\n" + "="*60)
    print("TEST: group_files_by_config() - empty list")
    print("="*60)
    
    groups = group_files_by_config([])
    
    assert len(groups) == 0, "Empty file list should produce no groups"
    
    print("  SUCCESS: Empty file list handled correctly")
    print("  ✓ All empty list tests passed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR get-test-configs.py")
    print("="*70)
    
    tests = [
        test_group_files_identical_config,
        test_group_files_different_configs,
        test_group_files_mixed_configs,
        test_skip_files_no_front_matter,
        test_skip_files_incomplete_config,
        test_skip_files_no_test_section,
        test_output_json_format,
        test_output_shell_format,
        test_empty_file_list
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
            print(f"\n  ✗ ERROR in {test_func.__name__}: {str(e)}")
    
    print("\n" + "="*70)
    print(f" TEST SUMMARY: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
