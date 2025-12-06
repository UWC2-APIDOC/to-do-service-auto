#!/usr/bin/env python3
"""
Scan Markdown files for Vale and markdownlint exception tags.

Usage:
    list-linter-exceptions.py <filename> [--action [LEVEL]]

Note: Does not test front matter sections.
"""

import sys
import re
import argparse
from pathlib import Path

# Import shared utilities
from doc_test_utils import read_markdown_file, log


def list_vale_exceptions(content):
    """
    Scan for Vale and markdownlint exception tags.
    
    Args:
        content: Markdown file content as string
    
    Returns:
        dict: {
            'vale': [{'line': int, 'rule': str, 'full_match': str}, ...],
            'markdownlint': [{'line': int, 'rule': str, 'full_match': str}, ...]
        }
    """
    exceptions = {
        'vale': [],
        'markdownlint': []
    }
    
    # Patterns
    # Vale: <!-- vale RuleName = NO -->
    vale_pattern = r'<!--\s*vale\s+([A-Za-z0-9.]+)\s*=\s*NO\s*-->'
    
    # Markdownlint: <!-- markdownlint-disable MD### -->
    markdown_pattern = r'<!--\s*markdownlint-disable\s+(MD\d{3})\s*-->'
    
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        # Check for Vale exceptions
        vale_match = re.search(vale_pattern, line)
        if vale_match:
            exceptions['vale'].append({
                'line': line_num,
                'rule': vale_match.group(1),
                'full_match': line.strip()
            })
        
        # Check for markdownlint exceptions
        md_match = re.search(markdown_pattern, line)
        if md_match:
            exceptions['markdownlint'].append({
                'line': line_num,
                'rule': md_match.group(1),
                'full_match': line.strip()
            })
    
    return exceptions


def output_normal(filepath, exceptions):
    """Output in normal format for interactive use."""
    vale_count = len(exceptions['vale'])
    md_count = len(exceptions['markdownlint'])
    
    log(f"{filepath.name}: {vale_count} Vale exceptions, {md_count} markdownlint exceptions", "info")
    
    # If no exceptions, add a notice
    if vale_count == 0 and md_count == 0:
        log("No Vale or markdownlint exceptions found.", "info")
        return
    
    if vale_count > 0:
        log("Vale exceptions:", "info")
        for exc in exceptions['vale']:
            log(f"  Line {exc['line']}: {exc['rule']}", "info")
    else:
        log("No Vale exceptions found.", "info")
    
    if md_count > 0:
        log("Markdownlint exceptions:", "info")
        for exc in exceptions['markdownlint']:
            log(f"  Line {exc['line']}: {exc['rule']}", "info")
    else:
        log("No markdownlint exceptions found.", "info")


def output_action(filepath, exceptions, action_level):
    """Output in GitHub Actions format with annotations."""
    vale_count = len(exceptions['vale'])
    md_count = len(exceptions['markdownlint'])
    
    # Summary line to console (always shown)
    log(f"{filepath.name}: {vale_count} Vale exceptions, {md_count} markdownlint exceptions", 
        "info")
    
    # If no exceptions, add a notice
    if vale_count == 0 and md_count == 0:
        log("No Vale or markdownlint exceptions found.",
            "notice",
            str(filepath),
            None,
            True,
            action_level)
        return
    
    if vale_count > 0:
        # Annotate each exception
        for exc in exceptions['vale']:
            log(f"Vale exception: {exc['rule']}",
                "warning",
                str(filepath),
                exc['line'],
                True,
                action_level)
    else:
        log("No Vale exceptions found.",
            "notice",
            str(filepath),
            None,
            True,
            action_level)
    
    if md_count > 0:
        # Annotate each exception
        for exc in exceptions['markdownlint']:
            log(f"Markdownlint exception: {exc['rule']}",
                "warning",
                str(filepath),
                exc['line'],
                True,
                action_level)
    else:
        log("No markdownlint exceptions found.",
            "notice",
            str(filepath),
            None,
            True,
            action_level)
    
    # Overall summary annotation
    if vale_count + md_count > 0:
        log(f"Found {vale_count} Vale and {md_count} markdownlint exceptions",
            "notice",
            str(filepath),
            None,
            True,
            action_level)


def main():
    parser = argparse.ArgumentParser(
        description='Scan Markdown files for Vale and markdownlint exception tags.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md                    # Normal output
  %(prog)s --action docs/api.md         # GitHub Actions output (warnings and errors)
  %(prog)s --action all docs/api.md     # GitHub Actions output (all levels)
  %(prog)s --action error docs/api.md   # GitHub Actions output (errors only)
        """
    )
    
    parser.add_argument(
        'filename',
        type=str,
        help='Path to the Markdown file to scan'
    )
    
    parser.add_argument(
        '--action', '-a',
        type=str,
        nargs='?',
        const='warning',
        default=None,
        choices=['all', 'warning', 'error'],
        metavar='LEVEL',
        help='Output GitHub Actions annotations. Optional LEVEL: all, warning (default if flag present), error'
    )
    
    args = parser.parse_args()
    
    filepath = Path(args.filename)
    
    # Read file using shared utility
    content = read_markdown_file(filepath)
    if content is None:
        log("File not found or unreadable",
            "error",
            str(filepath),
            None,
            args.action is not None,
            args.action or 'warning')
        sys.exit(1)
    
    # Scan for exceptions
    exceptions = list_vale_exceptions(content)
    
    # Output results
    if args.action:
        output_action(filepath, exceptions, args.action)
    else:
        output_normal(filepath, exceptions)


if __name__ == "__main__":
    main()
# End of file tools/list-linter-exceptions.py