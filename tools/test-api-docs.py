#!/usr/bin/env python3
"""
Test API documentation code examples against a running json-server instance.

Usage:
    test-api-docs.py <markdown_file> [--action [LEVEL]] [--schema SCHEMA_FILE]
    
Arguments:
    markdown_file: Path to the markdown documentation file to test
    --action: Optional flag to output GitHub Actions annotations
              Optional LEVEL: all, warning (default), error
    --schema: Path to JSON schema file for front matter validation
              Default: .github/schemas/front-matter-schema.json
    
Examples:
    test-api-docs.py docs/api/users-get-all-users.md --schema .schemas/front-matter-schema.json
    test-api-docs.py docs/api/users-get-all-users.md --action --schema .schemas/front-matter-schema.json
    test-api-docs.py docs/api/users-get-all-users.md --action all --schema .schemas/front-matter-schema.json
    test-api-docs.py docs/api/users-get-all-users.md --action error --schema .schemas/front-matter-schema.json
"""

import re
import subprocess
import json
import sys
import argparse
from pathlib import Path

from doc_test_utils import read_markdown_file, parse_front_matter, log
from schema_validator import validate_front_matter_schema


def parse_testable_entry(entry):
    """
    Parse a testable entry into example name and expected status codes.
    
    Format: "example name / status,codes"
    
    Args:
        entry: Testable entry string from front matter
        
    Returns:
        tuple: (example_name, expected_codes)
        
    Examples:
        >>> parse_testable_entry("GET example")
        ('GET example', [200])
        >>> parse_testable_entry("POST example / 201")
        ('POST example', [201])
        >>> parse_testable_entry("PUT example / 200,204")
        ('PUT example', [200, 204])
    """
    parts = entry.split('/')
    example_name = parts[0].strip()
    
    if len(parts) > 1:
        expected_codes = [int(code.strip()) for code in parts[1].split(',')]
    else:
        expected_codes = [200]
    
    return example_name, expected_codes


def extract_curl_command(content, example_name):
    """
    Extract curl command from the specified example section.
    
    Args:
        content: Full markdown file content
        example_name: Name of the example to find
        
    Returns:
        str: The curl command, or None if not found
    """
    # Escape the example name but allow backticks around words
    # Pattern like "GET example" should match "`GET` example", "GET `example`", or "`GET` `example`"
    escaped_name = re.escape(example_name)
    # Split on spaces and wrap each word to allow optional backticks
    words = escaped_name.split(r'\ ')
    flexible_words = [rf'`?{word}`?' for word in words]
    flexible_pattern = r'\s+'.join(flexible_words)
    
    # Look for heading with "request" (h3 or h4)
    heading_pattern = rf'^###\#?\s+{flexible_pattern}\s+request'
    
    lines = content.split('\n')
    in_example = False
    in_code_block = False
    curl_cmd_elements = []
    curl_cmd_string = ""
    
    for i, line in enumerate(lines):
        # Check if we found the heading
        if re.search(heading_pattern, line, re.IGNORECASE):
            in_example = True
            continue
        
        # If we're in the example section
        if in_example:
            # Look for bash code block
            if line.strip().startswith('```bash') or line.strip().startswith('```sh'):
                in_code_block = True
                continue
            
            # End of code block
            if in_code_block and line.strip() == '```':
                break
            
            # Collect curl command lines
            if in_code_block:
                curl_cmd_elements.append(line)
            
            # Stop if we hit another heading
            if line.startswith('#'):
                break
    
    if curl_cmd_elements:
        curl_cmd_string = '\n'.join(curl_cmd_elements).strip()
        # Add -i flag if not present to get headers
        if '-i' not in curl_cmd_string and '--include' not in curl_cmd_string:
            curl_cmd_string = curl_cmd_string.replace('curl', 'curl -i', 1)
        return curl_cmd_string
    
    return None


def extract_expected_response(content, example_name):
    """
    Extract expected JSON response from the specified example section.
    
    Args:
        content: Full markdown file content
        example_name: Name of the example to find
        
    Returns:
        dict: Parsed JSON response, or None if not found
    """
    # Similar flexible pattern as curl extraction
    escaped_name = re.escape(example_name)
    words = escaped_name.split(r'\ ')
    flexible_words = [rf'`?{word}`?' for word in words]
    flexible_pattern = r'\s+'.join(flexible_words)
    
    # Look for heading with "response" (h3 or h4)
    heading_pattern = rf'^###\#?\s+{flexible_pattern}\s+response'
    
    lines = content.split('\n')
    in_example = False
    in_code_block = False
    json_lines = []
    
    for i, line in enumerate(lines):
        # Check if we found the heading
        if re.search(heading_pattern, line, re.IGNORECASE):
            in_example = True
            continue
        
        # If we're in the example section
        if in_example:
            # Look for json code block
            if line.strip().startswith('```json'):
                in_code_block = True
                continue
            
            # End of code block
            if in_code_block and line.strip() == '```':
                break
            
            # Collect JSON lines
            if in_code_block:
                json_lines.append(line)
            
            # Stop if we hit another heading
            if line.startswith('#'):
                break
    
    if json_lines:
        try:
            return json.loads('\n'.join(json_lines))
        except json.JSONDecodeError:
            return None
    
    return None


def execute_curl(curl_command):
    """
    Execute a curl command and return the response.
    
    Args:
        curl_command: The curl command to execute
        
    Returns:
        tuple: (status_code, headers, body) or (None, None, error_message)
    """
    try:
        # Run curl with -i to get headers
        result = subprocess.run(
            ['bash', '-c', curl_command],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return None, None, result.stderr or "Command failed"
        
        # Parse response
        output = result.stdout
        
        # Split headers and body
        parts = output.split('\n\n', 1)
        if len(parts) < 2:
            # Try with \r\n\r\n
            parts = output.split('\r\n\r\n', 1)
        
        if len(parts) < 2:
            print (f"ERROR in response buffer:\n{result.stdout}")  
            return None, None, "Could not parse response"
        
        headers_text = parts[0]
        body = parts[1] if len(parts) > 1 else ""
        
        # Extract status code from first line
        status_line = headers_text.split('\n')[0]
        status_match = re.search(r'HTTP/[\d.]+ (\d+)', status_line)
        
        if not status_match:
            return None, None, "Could not parse status code"
        
        status_code = int(status_match.group(1))
        
        return status_code, headers_text, body
        
    except subprocess.TimeoutExpired:
        return None, None, "Request timed out"
    except Exception as e:
        return None, None, str(e)


def compare_json_objects(actual, expected, path=""):
    """
    Compare two JSON objects and return differences.
    
    Args:
        actual: Actual JSON object
        expected: Expected JSON object
        path: Current path in the object (for error messages)
        
    Returns:
        tuple: (are_equal, differences_list)
    """
    differences = []
    
    # Check types match
    if type(actual) != type(expected):
        differences.append(f"{path}: Type mismatch - expected {type(expected).__name__}, got {type(actual).__name__}")
        return False, differences
    
    # Compare based on type
    if isinstance(expected, dict):
        # Check all expected keys exist
        for key in expected:
            if key not in actual:
                differences.append(f"{path}.{key}: Missing in actual response")
            else:
                are_equal, subdiffs = compare_json_objects(
                    actual[key], expected[key], f"{path}.{key}" if path else key
                )
                differences.extend(subdiffs)
        
        # Check for extra keys in actual
        for key in actual:
            if key not in expected:
                differences.append(f"{path}.{key}: Extra key in actual response (not in documentation)")
    
    elif isinstance(expected, list):
        if len(actual) != len(expected):
            differences.append(f"{path}: Array length mismatch - expected {len(expected)}, got {len(actual)}")
        else:
            for i, (actual_item, expected_item) in enumerate(zip(actual, expected)):
                are_equal, subdiffs = compare_json_objects(
                    actual_item, expected_item, f"{path}[{i}]"
                )
                differences.extend(subdiffs)
    
    else:
        # Primitive types - direct comparison
        if actual != expected:
            differences.append(f"{path}: Value mismatch - expected {expected}, got {actual}")
    
    return len(differences) == 0, differences


def test_example(content, example_name, expected_codes, file_path, use_actions, action_level):
    """
    Test a single example from the documentation.
    
    Args:
        content: Full markdown file content
        example_name: Name of the example to test
        expected_codes: List of acceptable HTTP status codes
        file_path: Path to the markdown file
        use_actions: Whether to output GitHub Actions annotations
        action_level: Annotation level filter
        
    Returns:
        bool: True if test passed, False otherwise
    """
    see_also_the_log = " See the 'Test changed documentation files' entry in the log for more info."
    
    log(f"Testing: {example_name}")
    log(f"  -- Expected status: {', '.join(map(str, expected_codes))}")
    
    # Extract curl command
    curl_cmd = extract_curl_command(content, example_name)
    if not curl_cmd:
        log(f"  -- Could not find example '{example_name}' or it is not formatted correctly", 
            "warning", file_path, None, use_actions, action_level)
        log(f"  -- Expected format: '### {example_name} request' section with bash code block")
        log("   -- For help, visit: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format")
        return False
    
    log(f"  -- Command: {curl_cmd[:80]}...")
    
    # Execute curl command
    status_code, headers, body = execute_curl(curl_cmd)
    
    if status_code is None:
        log(f"  -- Example '{example_name}' failed: {body}", 
            "error", file_path, None, use_actions, action_level)
        return False
    
    log(f"  -- Status: {status_code}")
    
    # Validate status code
    if status_code not in expected_codes:
        expected_str = ' or '.join(map(str, expected_codes))
        log(f"Example '{example_name}' failed: Expected HTTP {expected_str}, got {status_code}.", 
            "error", file_path, None, use_actions, action_level)
        return False
    
    log(f"  HTTP {status_code} (success)", "success")
    
    # Parse response body as JSON
    try:
        response_json = json.loads(body)
        log("  Valid JSON response received", "success")
    except json.JSONDecodeError:
        log(f"  Example '{example_name}' failed: Response is not valid JSON", 
            "error", file_path, None, use_actions, action_level)
        log(f"  Response: {body[:200]}")
        return False
    
    # Extract expected response
    expected_json = extract_expected_response(content, example_name)
    if expected_json is None:
        log(f"  -- Could not find documented response for '{example_name}' or it is not formatted correctly", 
            "warning", file_path, None, use_actions, action_level)
        log(f"  -- Expected format: '### {example_name} response' section with json code block")
        log("   -- For help, visit: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format")
        return False
    
    # Compare actual vs expected
    are_equal, differences = compare_json_objects(response_json, expected_json)
    
    if are_equal:
        log("  -- Response matches documentation exactly", "success")
        log(f"  -- ✓ Example '{example_name}' PASSED", "success")
        return True
    else:
        log(f"  -- Example '{example_name}' failed: Response does not match documentation", 
            "error", file_path, None, use_actions, action_level)
        log(f"  -- Differences found ({len(differences)}):")
        for diff in differences[:10]:  # Show first 10 differences
            log(f"    • {diff}")
        if len(differences) > 10:
            log(f"  ... and {len(differences) - 10} more differences")
        return False


def test_file(file_path, schema_path, use_actions=False, action_level="warning"):
    """
    Test all examples in a documentation file.
    
    Args:
        file_path: Path to the markdown file to test
        schema_path: Path to JSON schema file for validation
        use_actions: Whether to output GitHub Actions annotations
        action_level: Annotation level filter (all, warning, error)
        
    Returns:
        tuple: (total_tests, passed_tests, failed_tests)
    """
    log(f"\n{'#'*60}")
    log(f"# Testing file: {file_path}")
    log(f"{'#'*60}")
    
    # Read file content using shared utility
    content = read_markdown_file(Path(file_path))
    if content is None:
        log(f"  File not found or unreadable: {file_path}", 
            "error", file_path, None, use_actions, action_level)
        return 0, 0, 0
    
    # Extract and parse front matter
    metadata = parse_front_matter(content)
    if not metadata:
        log("No front matter found", "error", file_path, None, use_actions, action_level)
        log("All documentation files must have YAML front matter between --- delimiters")
        log("📖 Documentation: https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Frontmatter-Format")
        return 0, 0, 0
    
    # Validate front matter against schema
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path, file_path, use_actions, action_level
    )
    
    if not is_valid:
        log("\n  ❌ Front matter validation failed. Fix errors before testing examples.", "error")
        return 0, 0, 0
    
    if has_warnings:
        log("\n  ⚠️  Front matter has warnings but is valid enough to continue", "warning")
    
    # Check if file has testable examples
    test_config = metadata.get('test', {})
    if not test_config:
        log("  No test configuration found in front matter", "info")
        return 0, 0, 0
    
    testable = test_config.get('testable', [])
    if not testable:
        log("  No testable examples marked in front matter", "info")
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
        
        if test_example(content, example_name, expected_codes, file_path, use_actions, action_level):
            passed_tests += 1
        else:
            failed_tests += 1
    
    return total_tests, passed_tests, failed_tests


def main():
    """Main entry point for the test-api-docs tool."""
    parser = argparse.ArgumentParser(
        description='Test API documentation code examples against a running json-server instance.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s docs/api.md                    # Normal output
  %(prog)s --action docs/api.md           # GitHub Actions output (warnings and errors)
  %(prog)s --action all docs/api.md       # GitHub Actions output (all levels)
  %(prog)s --action error docs/api.md     # GitHub Actions output (errors only)
        """
    )
    
    parser.add_argument(
        'file',
        type=str,
        help='Path to the markdown documentation file to test'
    )
    
    parser.add_argument(
        '--action', '-a',
        type=str,
        nargs='?',
        const='warning',
        default=None,
        choices=['all', 'warning', 'error'],
        metavar='LEVEL',
        help='Output GitHub Actions annotations. Optional LEVEL: all, warning (default), error'
    )
    
    parser.add_argument(
        '--schema',
        default='.github/schemas/front-matter-schema.json',
        help='Path to JSON schema file for front matter validation'
    )
    
    args = parser.parse_args()
    
    
    # Test the file
    total, passed, failed = test_file(
        args.file, 
        args.schema, 
        args.action is not None, 
        args.action or 'warning'
    )
    
    # Print summary
    log(f"TEST SUMMARY: {args.file}")
    log(f"  Total tests: {total}")
    if passed > 0:
        log(f"    Passed: {passed}", "success")
    if failed > 0:
        log(f"    Failed: {failed}", "success")
    
    # Exit with appropriate code
    if failed > 0:
        sys.exit(1)
    elif total == 0:
        log("  No tests were run", "warning")
        sys.exit(0)
    else:
        log("✓ All tests passed!", "success")
        sys.exit(0)


if __name__ == '__main__':
    main()
