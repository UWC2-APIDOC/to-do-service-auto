#!/usr/bin/env python3
"""
Count unique markdown notation patterns in a file.

Usage:
    markdown-survey.py <filename> [--action [LEVEL]]

This tool analyzes markdown files to count:
- Words (excluding code, HTML, and markdown notation)
- Markdown notation patterns (headings, lists, links, etc.)
- Unique notation types used

Examples:
    markdown-survey.py README.md
    markdown-survey.py --action docs/api.md
    markdown-survey.py --action all docs/api.md
"""

import sys
import re
import argparse
from pathlib import Path

from doc_test_utils import read_markdown_file, log


def count_words(content: str) -> int:
    """
    Count words in markdown content, excluding code blocks and HTML.
    
    Algorithm:
    1. Remove fenced code blocks (```...```)
    2. Remove inline code (`...`)
    3. Remove HTML tags
    4. Remove markdown notation characters
    5. Split on whitespace and count non-empty tokens
    
    Args:
        content: Full markdown file content as string
        
    Returns:
        Number of prose words in the content
        
    Example:
        >>> content = "# Heading\\n\\nThis is **bold** text with `code`."
        >>> count_words(content)
        5
    """
    # Remove fenced code blocks
    text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove image syntax entirely (must be before link removal)
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
    
    # Remove URLs from links but keep link text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # Remove markdown notation characters
    text = re.sub(r'[#*_~`\[\]()>|+-]', ' ', text)
    
    # Split and count non-empty words
    words = [w for w in text.split() if w.strip()]
    
    return len(words)


def list_markdown_notations(content: str) -> list:
    """
    Extract and count markdown notation patterns.
    
    Patterns assume markdownlint compliance:
    - Headings have space after #
    - Lists have proper spacing
    - Horizontal rules are on their own lines
    
    Args:
        content: Full markdown file content as string
        
    Returns:
        List of notation names found (may contain duplicates)
        
    Example:
        >>> content = "# Heading\\n\\n**bold** and `code`"
        >>> notations = list_markdown_notations(content)
        >>> 'heading_1' in notations
        True
        >>> 'bold_asterisk' in notations
        True
    """
    patterns = {
        # Headings (1-6 levels) - must have space after
        r'^#\s': 'heading_1',
        r'^##\s': 'heading_2',
        r'^###\s': 'heading_3',
        r'^####\s': 'heading_4',
        r'^#####\s': 'heading_5',
        r'^######\s': 'heading_6',
        
        # Bold
        r'\*\*': 'bold_asterisk',
        r'__': 'bold_underscore',
        
        # Italic
        r'(?<!\*)\*(?!\*)': 'italic_asterisk',
        r'(?<!_)_(?!_)': 'italic_underscore',
        
        # Code
        r'```': 'code_block',
        r'`': 'inline_code',
        
        # Links and images
        r'!\[.*?\]\(.*?\)': 'image',
        r'(?<!!)\[.*?\]\(.*?\)': 'link',
        
        # Blockquote - must have space after >
        r'^>\s': 'blockquote',
        
        # Lists - markdownlint requires space after marker
        r'^\s*[-*+]\s': 'unordered_list',
        r'^\s*\d+\.\s': 'ordered_list',
        
        # Horizontal rule - must be on own line
        r'^(\*{3,}|-{3,}|_{3,})$': 'horizontal_rule',
        
        # Strikethrough
        r'~~': 'strikethrough',
        
        # Tables
        r'\|': 'table_pipe',
    }
    
    found_notations = []
    
    for line in content.split('\n'):
        for pattern, notation_name in patterns.items():
            if re.search(pattern, line, re.MULTILINE):
                found_notations.append(notation_name)
    
    return found_notations


def main():
    """Main entry point for the markdown survey tool."""
    parser = argparse.ArgumentParser(
        description='Count markdown notation patterns and words in a file.',
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
        help='Path to the markdown file to analyze'
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
    
    # Count words and notations
    word_count = count_words(content)
    markdown_notations = list_markdown_notations(content)
    markdown_notation_count = len(markdown_notations)
    unique_notations = set(markdown_notations)
    unique_notation_count = len(unique_notations)
    unique_notation_list = ', '.join(sorted(unique_notations))
    
    # Format output message
    message = (f"{filepath.name}: {word_count} words, "
               f"{markdown_notation_count} markdown_symbols, "
               f"{unique_notation_count} unique_codes: {unique_notation_list}")
    
    # Output results
    if args.action:
        log(message, "notice", str(filepath), None, True, args.action)
    else:
        log(message, "info")


if __name__ == "__main__":
    main()


"""
Word count algorithm rationale:

The algorithm excludes content that isn't "document words":
1. **Code blocks removed** - not prose
2. **Inline code removed** - typically technical identifiers, not words
3. **HTML tags removed** - markup, not content
4. **Link URLs removed** - keep link text (those are words), discard URLs
5. **Images removed entirely** - alt text is often filenames/technical
6. **Markdown notation stripped** - removes #, *, _, etc.

This gives a count of actual prose words in the document.

Alternative algorithms to consider:

- **More inclusive**: Keep inline code, alt text → higher counts, includes all visible text
- **More strict**: Remove headings, emphasis entirely → lower counts, only body text
- **Simple split**: Just `len(content.split())` → fastest but counts everything including URLs

The current approach balances "words a human reader would read as prose" while being 
deterministic and fast.

Example output:

README.md: 1247 words, 342 markdown_symbols, 8 unique_codes: bold_asterisk, code_block, 
heading_1, heading_2, inline_code, link, ordered_list, table_pipe, unordered_list
"""