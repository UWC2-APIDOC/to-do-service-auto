#!/usr/bin/env python3
"""
Test API documentation code examples against a running json-server instance.

Usage:
    python test-api-docs.py <markdown_file> [--action] [--annotations LEVEL] [--schema SCHEMA_FILE]
    
Arguments:
    markdown_file: Path to the markdown documentation file to test
    --action: Optional flag to output GitHub Actions annotations
    --annotations: Filter annotations by level (error, warning, all). Default: error
    --schema: Path to JSON schema file for frontmatter validation. Default: .github/schemas/front-matter-schema.json
    
Examples:
    python test-api-docs.py docs/api/users-get-all-users.md
    python test-api-docs.py docs/api/users-get-all-users.md --action
    python test-api-docs.py docs/api/users-get-all-users.md --action --annotations all
    python test-api-docs.py docs/api/users-get-all-users.md --action --annotations warning
"""

import yaml
import re
import subprocess
import json
import sys
import argparse
import os
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError, Draft7Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


def log(message, level="info", file_path=None, use_actions=False, annotation_filter="error", annotation_text=None):
    """
    Print a message to console and optionally as GitHub Actions annotation.
    
    Args:
        message: The message to log
        level: One of 'info', 'warning', 'error', 'success'
        file_path: Optional file path for GitHub Actions annotations
        use_actions: Whether to output GitHub Actions annotations
        annotation_filter: Filter for annotations ('error', 'warning', 'all')
        annotation_text: Optional additional text for the annotations only
    """
    icons = {
        'info': 'ℹ️ ',
        'warning': '⚠️ ',
        'error': '❌',
        'success': '✓'
    }
    
    icon = icons.get(level, '')
    console_msg = f"{icon} {message}" if icon else message
    print(console_msg)
    
    if use_actions and level in ['warning', 'error']:
        # Determine if this annotation should be output based on filter
        should_annotate = False
        if annotation_filter == 'all':
            should_annotate = True
        elif annotation_filter == 'warning' and level in ['warning', 'error']:
            should_annotate = True
        elif annotation_filter == 'error' and level == 'error':
            should_annotate = True
        
        if should_annotate:
            action_level = 'error' if level == 'error' else 'warning'
            if file_path:
                print(f"::{action_level} file={file_path}::{message}::{annotation_text or ''}")
            else:
                print(f"::{action_level}::{message}::{annotation_text or ''}")


def parse_frontmatter(content):
    """Extract and parse YAML frontmatter from markdown content."""
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        return None
    
    try:
        return yaml.safe_load(fm_match.group(1))
    except yaml.YAMLError:
        return None


def validate_frontmatter(metadata, schema_path, file_path, use_actions, annotation_filter):
    """
    Validate frontmatter against JSON schema.
    
    Returns:
        tuple: (is_valid, has_warnings, error_messages, warning_messages)
    """
    if not JSONSCHEMA_AVAILABLE:
        log("jsonschema library not installed. Run: pip install jsonschema", "warning", 
            file_path, use_actions, annotation_filter)
        return True, False, [], []
    
    # Load schema
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
    except FileNotFoundError:
        log(f"Schema file not found: {schema_path}", "warning", 
            file_path, use_actions, annotation_filter)
        return True, False, [], []
    except json.JSONDecodeError as e:
        log(f"Invalid JSON schema: {str(e)}", "warning", 
            file_path, use_actions, annotation_filter)
        return True, False, [], []
    
    validator = Draft7Validator(schema)
    errors = []
    warnings = []
    
    # Collect all validation errors
    for error in validator.iter_errors(metadata):
        # Determine if this is a required field error (critical) or optional field error (warning)
        is_required_error = False
        
        # Check if error is about a required property
        if error.validator == 'required':
            is_required_error = True
            missing_field = error.message.split("'")[1] if "'" in error.message else "unknown"
            errors.append(f"Required field missing: {missing_field}")
        
        # Check if error is about an enum value for a required field
        elif error.validator == 'enum' and len(error.absolute_path) > 0:
            field_name = '.'.join(str(p) for p in error.absolute_path)
            # Check if this field is in the required list
            if error.absolute_path[0] in schema.get('required', []):
                is_required_error = True
                errors.append(f"Invalid value for required field '{field_name}': {error.message}")
            else:
                warnings.append(f"Invalid value for optional field '{field_name}': {error.message}")
        
        # Check if error is about type or format for required fields
        elif error.validator in ['type', 'format', 'pattern', 'minimum', 'maximum', 'minLength', 'maxLength']:
            field_name = '.'.join(str(p) for p in error.absolute_path)
            # Check if this field is in the required list
            if len(error.absolute_path) > 0 and error.absolute_path[0] in schema.get('required', []):
                is_required_error = True
                errors.append(f"Invalid format for required field '{field_name}': {error.message}")
            else:
                warnings.append(f"Invalid format for optional field '{field_name}': {error.message}")
        else:
            # Other errors default to warnings for optional fields
            field_name = '.'.join(str(p) for p in error.absolute_path) if error.absolute_path else "unknown"
            warnings.append(f"Validation issue in '{field_name}': {error.message}")
    
    # Report errors
    if errors:
        log("Frontmatter validation errors found:", "error", file_path, use_actions, annotation_filter)
        for error_msg in errors:
            log(f"  - {error_msg}", "error", file_path, use_actions, annotation_filter)
    
    # Report warnings
    if warnings:
        log("Frontmatter validation warnings:", "warning", file_path, use_actions, annotation_filter)
        for warning_msg in warnings:
            log(f"  - {warning_msg}", "warning", file_path, use_actions, annotation_filter)
    
    if not errors and not warnings:
        log("Frontmatter validation passed", "success")
    
    return len(errors) == 0, len(warnings) > 0, errors, warnings


def parse_testable_entry(entry):
    """
    Parse a testable entry into example name and expected status codes.
    
    Format: "example name / status,codes"
    Examples:
        "GET example" -> ("GET example", [200])
        "POST example / 201" -> ("POST example", [201])
        "PUT example / 200,204" -> ("PUT example", [200, 204])
    """
    parts = entry.split('/')
    example_name = parts[0].strip()
    
    if len(parts) > 1:
        expected_codes = [int(code.strip()) for code in parts[1].split(',')]
    else:
        expected_codes = [200]
    
    return example_name, expected_codes


def extract_curl_command(content, example_name):
    """Extract curl command from the specified example section."""
    # Escape the example name but allow backticks around any part of it
    # This matches headings like "### `GET` example request" when example_name is "GET example"
    escaped_name = re.escape(example_name)
    # Replace spaces in the pattern with \s*`?\s* to allow backticks between words
    pattern_parts = escaped_name.split(r'\ ')  # Split on escaped spaces
    flexible_pattern = r'\s*`?\s*'.join(pattern_parts)
    
    example_pattern = rf'###\s+`?{flexible_pattern}`?\s+.*?request.*?\n```bash\n(.*?)```'
    example_match = re.search(example_pattern, content, re.IGNORECASE | re.DOTALL)
    
    if not example_match:
        return None
    
    return example_match.group(1).strip()


def extract_expected_response(content, example_name):
    """Extract expected JSON response from the specified example section."""
    # Same flexible pattern as extract_curl_command
    escaped_name = re.escape(example_name)
    pattern_parts = escaped_name.split(r'\ ')
    flexible_pattern = r'\s*`?\s*'.join(pattern_parts)
    
    response_pattern = rf'###\s+`?{flexible_pattern}`?\s+.*?response.*?\n```json\n(.*?)```'
    response_match = re.search(response_pattern, content, re.IGNORECASE | re.DOTALL)
    
    if not response_match:
        return None
    
    try:
        return json.loads(response_match.group(1).strip())
    except json.JSONDecodeError:
        return None


def compare_json_objects(actual, expected, path=""):
    """
    Compare two JSON objects and return detailed differences.
    
    Returns:
        tuple: (are_equal, list_of_differences)
    """
    differences = []
    
    # Type mismatch
    if type(actual) != type(expected):
        differences.append(f"{path}: Type mismatch - expected {type(expected).__name__}, got {type(actual).__name__}")
        return False, differences
    
    # Compare dictionaries
    if isinstance(actual, dict):
        # Check for missing keys in actual
        missing_keys = set(expected.keys()) - set(actual.keys())
        for key in missing_keys:
            differences.append(f"{path}.{key}: Missing in actual response")
        
        # Check for extra keys in actual
        extra_keys = set(actual.keys()) - set(expected.keys())
        for key in extra_keys:
            differences.append(f"{path}.{key}: Extra key in actual response (not in documentation)")
        
        # Compare common keys
        for key in set(actual.keys()) & set(expected.keys()):
            new_path = f"{path}.{key}" if path else key
            equal, diffs = compare_json_objects(actual[key], expected[key], new_path)
            differences.extend(diffs)
    
    # Compare lists
    elif isinstance(actual, list):
        if len(actual) != len(expected):
            differences.append(f"{path}: Array length mismatch - expected {len(expected)}, got {len(actual)}")
        
        for i, (actual_item, expected_item) in enumerate(zip(actual, expected)):
            new_path = f"{path}[{i}]"
            equal, diffs = compare_json_objects(actual_item, expected_item, new_path)
            differences.extend(diffs)
    
    # Compare primitives
    else:
        if actual != expected:
            differences.append(f"{path}: Value mismatch - expected {repr(expected)}, got {repr(actual)}")
    
    return len(differences) == 0, differences

def execute_curl(curl_cmd, timeout=10):
    """
    Execute a curl command and return status code, headers, and body.
    
    Returns:
        tuple: (status_code, headers, body) or (None, None, error_message)
    """
    # Add -i flag if not present to get headers
    if '-i' not in curl_cmd and '--include' not in curl_cmd:
        curl_cmd = curl_cmd.replace('curl', 'curl -i', 1)
    
    try:
        result = subprocess.run(
            curl_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode != 0:
            return None, None, f"  -- Curl command failed: {result.stderr}"
        
        # Split headers and body
        output = result.stdout
        if '\r\n\r\n' in output:
            headers, body = output.split('\r\n\r\n', 1)
        elif '\n\n' in output:
            headers, body = output.split('\n\n', 1)
        else:
            return None, None, "Could not parse HTTP response (no header/body separator found)"
        
        # Extract status code
        status_match = re.search(r'HTTP/[\d.]+\s+(\d+)', headers)
        if not status_match:
            return None, None, "Could not find HTTP status code in response"
        
        status_code = int(status_match.group(1))
        
        return status_code, headers, body
        
    except subprocess.TimeoutExpired:
        return None, None, "Request timed out"
    except Exception as e:
        return None, None, f"Unexpected error: {str(e)}"


def test_example(content, example_name, expected_codes, file_path, use_actions, annotation_filter):
    """
    Test a single example from the documentation.
    
    Returns:
        bool: True if test passed, False otherwise
    """
    see_also_the_log =  " See the \"Test changed documentation files\" entry in the log for more info."
    log(f"Testing: {example_name}")
    log(f"  -- Expected status: {', '.join(map(str, expected_codes))}")
    
    # Extract curl command
    curl_cmd = extract_curl_command(content, example_name)
    if not curl_cmd:
        log(f"  -- Could not find example '{example_name}' or it is not formatted correctly", 
            "warning", file_path, use_actions, annotation_filter, see_also_the_log)
        log(f"  -- Expected format: '### {example_name} request' section with bash code block")
        log("   -- For help, visit: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format")
        return False
    
    log(f"  -- Command: {curl_cmd[:80]}...")
    
    # Execute curl command
    status_code, headers, body = execute_curl(curl_cmd)
    
    if status_code is None:
        log(f"  -- Example '{example_name}' failed: {body}", "error", file_path, use_actions, annotation_filter)
        return False
    
    log(f"  -- Status: {status_code}")
    
    # Validate status code
    if status_code not in expected_codes:
        expected_str = ' or '.join(map(str, expected_codes))
        log(f"Example '{example_name}' failed: Expected HTTP {expected_str}, got {status_code}.", 
            "error", file_path, use_actions, annotation_filter, see_also_the_log)
        return False
    
    log(f"  HTTP {status_code} (success)", "success")
    
    # Parse response body as JSON
    try:
        response_json = json.loads(body)
        log("  Valid JSON response received", "success")
    except json.JSONDecodeError:
        log(f"  Example '{example_name}' failed: Response is not valid JSON", 
            "error", file_path, use_actions, annotation_filter, see_also_the_log)
        log(f". Response: {body[:200]}")
        return False
    
    # Extract expected response
    expected_json = extract_expected_response(content, example_name)
    if expected_json is None:
        log(f"-- Could not find documented response for '{example_name}' or it is not formatted correctly", 
            "warning", file_path, use_actions, annotation_filter, see_also_the_log)
        log(f"-- Expected format: '### {example_name} response' section with json code block")
        log("   -- For help, visit: Documentation: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format")
        return False
    
    # Compare actual vs expected
    are_equal, differences = compare_json_objects(response_json, expected_json)
    
    if are_equal:
        log("  -- Response matches documentation exactly", "success")
        log(f"  --✓ Example '{example_name}' PASSED", "success")
        return True
    else:
        log(f"  -- Example '{example_name}' failed: Response does not match documentation", 
            "error", file_path, use_actions, annotation_filter, see_also_the_log)
        log(f"  -- Differences found ({len(differences)}):")
        for diff in differences[:10]:  # Show first 10 differences
            log(f"    • {diff}")
        if len(differences) > 10:
            log(f"  ... and {len(differences) - 10} more differences")
        return False


def test_file(file_path, schema_path, use_actions=False, annotation_filter="error"):
    """
    Test all examples in a documentation file.
    
    Returns:
        tuple: (total_tests, passed_tests, failed_tests)
    """
    log(f"\n{'#'*60}")
    log(f"# Testing file: {file_path}")
    log(f"{'#'*60}")
    
    # Read file content
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        log(f"  File not found: {file_path}", "error", file_path, use_actions, annotation_filter)
        return 0, 0, 0
    except Exception as e:
        log(f". Error reading file: {str(e)}", "error", file_path, use_actions, annotation_filter)
        return 0, 0, 0
    
    # Extract and parse frontmatter
    metadata = parse_frontmatter(content)
    if not metadata:
        log("No frontmatter found", "error", file_path, use_actions, annotation_filter, see_also_the_log)
        log("All documentation files must have YAML frontmatter between --- delimiters")
        log("📖 Documentation: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Frontmatter-Format")
        return 0, 0, 0
    
    # Validate frontmatter against schema
    is_valid, has_warnings, errors, warnings = validate_frontmatter(
        metadata, schema_path, file_path, use_actions, annotation_filter
    )
    
    if not is_valid:
        log("\n. ❌ Frontmatter validation failed. Fix errors before testing examples.", "error")
        return 0, 0, 0
    
    if has_warnings:
        log("\n  ⚠️  Frontmatter has warnings but is valid enough to continue", "warning")
    
    # Check if file has testable examples
    test_config = metadata.get('test', {})
    if not test_config:
        log("  No test configuration found in frontmatter", "info")
        return 0, 0, 0
    
    testable = test_config.get('testable', [])
    if not testable:
        log("  No testable examples marked in frontmatter", "info")
        return 0, 0, 0
    
    log(f"  Testable examples found: {len(testable)}")
    for item in testable:
        log(f"  - {item}")
    
    # Test each example
    total_tests = len(testable)
    passed_tests = 0
    failed_tests = 0
    
    for testable_entry in testable:
        example_name, expected_codes = parse_testable_entry(testable_entry)
        
        if test_example(content, example_name, expected_codes, file_path, use_actions, annotation_filter):
            passed_tests += 1
        else:
            failed_tests += 1
    
    return total_tests, passed_tests, failed_tests


def main():
    parser = argparse.ArgumentParser(
        description='Test API documentation code examples against a running json-server instance.'
    )
    parser.add_argument('file', help='Path to the markdown documentation file to test')
    parser.add_argument('--action', action='store_true', 
                       help='Output GitHub Actions annotations')
    parser.add_argument('--annotations', default='error', choices=['error', 'warning', 'all'],
                       help='Filter annotations by level (default: error)')
    parser.add_argument('--schema', default='.github/schemas/front-matter-schema.json',
                       help='Path to JSON schema file for frontmatter validation')
    
    args = parser.parse_args()
    
    # Check if jsonschema is available
    if not JSONSCHEMA_AVAILABLE:
        print("⚠️  Warning: jsonschema library not installed")
        print("   Frontmatter validation will be skipped")
        print("   Install with: pip install jsonschema")
        print()
    
    # Check if schema file exists
    if not os.path.exists(args.schema):
        print(f"⚠️  Warning: Schema file not found: {args.schema}")
        print("   Frontmatter validation will be skipped")
        print()
    
    # Test the file
    total, passed, failed = test_file(args.file, args.schema, args.action, args.annotations)
    
    # Print summary
    log(f"TEST SUMMARY: {args.file}")
    log(f"  Total tests: {total}")
    if passed > 0:
        log(f"    Passed: {passed}", "success")
    if failed > 0:
        # this is labeled success because it's summary info and not a test result
        log(f"    Failed: {failed}", "success")
    
    # Exit with appropriate code
    if failed > 0:
        sys.exit(1)
    elif total == 0:
        log("  No tests were run", "warning")
        sys.exit(0)
    else:
        log("✓   All tests passed!", "success")
        sys.exit(0)


if __name__ == '__main__':
    main()
