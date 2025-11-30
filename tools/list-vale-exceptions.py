#!/usr/bin/env python3
"""
Scan markdown files for Vale and markdownlint exception tags.
Usage: list_vale_exceptions.py [--action] <filename>

Note: does not test front matter sections.

"""

import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict

def list_vale_exceptions(content):
    """
    Scan for Vale and markdownlint exception tags.
    
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

def annotate(level, message, filename=None, line=None, col=None, title=None):
    """Output a GitHub Actions annotation."""
    show=False
    level_options=list(['notice', 'warning', 'error'])

    # Check if the annotation should be shown based on specified level
    if level not in level_options:
        # default to display the message
        show=True
    elif (level_options.index(level) >= level_options.index(args.annotation)):
        # if the message level is equal or higher than the set annotation level,
        show=True

    if not show:
        return
    
    # else continue to output the annotation
    parts = [f"::{level}"]

    properties = []
    if filename:
        properties.append(f"file={filename}")
    if line:
        properties.append(f"line={line}")
    if col:
        properties.append(f"col={col}")
    if title:
        properties.append(f"title={title}")
    
    if properties:
        parts[0] += " " + ",".join(properties)
    
    parts.append(f"::{message}")
    print("".join(parts))

def output_normal(filepath, exceptions):
    """Output in normal format for interactive use."""
    # these messages are also written to the log file

    vale_count = len(exceptions['vale'])
    md_count = len(exceptions['markdownlint'])
    
    print(f"{filepath.name}: {vale_count} Vale exceptions, {md_count} markdownlint exceptions")

    # If no exceptions, add a notice
    if vale_count == 0 and md_count == 0:
        print("No Vale or markdownlint exceptions found.")
        return
    
    if vale_count > 0:
        print("\nVale exceptions:")
        for exc in exceptions['vale']:
            print(f"  Line {exc['line']}: {exc['rule']}")
    else:
        print("\nNo Vale exceptions found.")
    
    if md_count > 0:
        print("\nMarkdownlint exceptions:")
        for exc in exceptions['markdownlint']:
            print(f"  Line {exc['line']}: {exc['rule']}")
    else:
        print("\nNo markdownlint exceptions found.")

def output_action(filepath, exceptions):
    """Output in GitHub Actions format with annotations."""
    vale_count = len(exceptions['vale'])
    md_count = len(exceptions['markdownlint'])
    
    # Summary line to log file
    print(f"{filepath.name}: {vale_count} Vale exceptions, {md_count} markdownlint exceptions")
    
    # If no exceptions, add a notice
    if vale_count == 0 and md_count == 0:
        annotate("notice",
                 "No Vale or markdownlint exceptions found.",
                 filename=str(filepath),
                 title="No lint exceptions")
        return
    
    if vale_count > 0:
        # Annotate each exception
        for exc in exceptions['vale']:
            annotate("warning",
                    f"Vale exception: {exc['rule']}",
                    filename=str(filepath),
                    line=exc['line'],
                    title="Vale exception")
    else:
        annotate("notice",
            "No Vale exceptions found.",
            filename=str(filepath),
            title="No Vale exceptions")

    if md_count > 0:
        # Annotate each exception
        for exc in exceptions['markdownlint']:
            annotate("warning",
                    f"Markdownlint exception: {exc['rule']}",
                    filename=str(filepath),
                    line=exc['line'],
                    title="Markdownlint Exception")
    else:
        annotate("notice",
            "No markdownlint exceptions found.",
            filename=str(filepath),
            title="No markdownlint exceptions")
    
    # Overall summary annotation
    if vale_count + md_count > 0:
        annotate("notice",
                 f"Found {vale_count} Vale and {md_count} markdownlint exceptions",
                 filename=str(filepath),
                 title="Exception Summary")

def main():
    filepath = Path(args.filename)
    
    if not filepath.exists():
        print(f"Error: File '{filepath}' not found", file=sys.stderr)
        annotate("error",
            f"File not found",
            filename=str(filepath),
            title="File not found")

        sys.exit(1)
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        annotate("error",
            f"Unable to read file: {e}",
            filename=str(filepath),
            title="File not found")
        sys.exit(1)
    
    exceptions = list_vale_exceptions(content)
    
    if args.action:
        output_action(filepath, exceptions)
    else:
        output_normal(filepath, exceptions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Scan markdown files for Vale and markdownlint exception tags.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md                 # Normal output
  %(prog)s --action docs/api.md      # GitHub Actions output with annotations
        """
    )

    parser.add_argument(
        'filename',
        type=str,
        help='Path to the markdown file to scan'
    )
    
    parser.add_argument(
        '--action','-a',
        action='store_true',
        help='Output format for GitHub Actions with annotations'
    )
       
    parser.add_argument(
        '--annotation','-l',
        choices=['notice', 'warning', 'error'],
        default='warning',
        action='store',
        help='Minimum message level to send an annotation to GitHub Actions (default: warning)'
    )
    
    args = parser.parse_args()
    main()
# End of file tools/list-vale-exceptions.py