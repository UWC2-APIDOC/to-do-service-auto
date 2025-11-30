#!/usr/bin/env python3
"""
Count unique markdown notation patterns in a file.
Usage: markdown_char_count.py <filename>
"""

import sys
import re
import argparse
from pathlib import Path

def count_words(content):
    """
    Count words in markdown content, excluding code blocks and HTML.
    
    Algorithm:
    1. Remove fenced code blocks (```...```)
    2. Remove inline code (`...`)
    3. Remove HTML tags
    4. Remove markdown notation characters
    5. Split on whitespace and count non-empty tokens
    """
    # Remove fenced code blocks
    text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove URLs from links but keep link text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # Remove image syntax entirely
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
    
    # Remove markdown notation characters
    text = re.sub(r'[#*_~`\[\]()>|+-]', ' ', text)
    
    # Split and count non-empty words
    words = [w for w in text.split() if w.strip()]
    
    return len(words)

def list_markdown_notations(content):
    """
    Extract and count unique markdown notation patterns.
    
    Patterns assume markdownlint compliance:
    - Headings have space after #
    - Lists have proper spacing
    - Horizontal rules are on their own lines
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
    
    found_notations = list()
    
    for line in content.split('\n'):
        for pattern, notation_name in patterns.items():
            if re.search(pattern, line, re.MULTILINE):
                found_notations.append(notation_name)
    
    return found_notations

def main():
    parser = argparse.ArgumentParser(
        description='Count markdown notation patterns and words in a file.',
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
        help='Path to the markdown file to analyze'
    )
    
    parser.add_argument(
        '--action',
        action='store_true',
        help='Output format for GitHub Actions with annotations'
    )
    
    args = parser.parse_args()
    
    filepath = Path(args.filename)

    if not filepath.exists():
        if (args.action):
            print(f"::error file={filepath.name},title=File not found::File '{filepath}' not found")
        else:
            print(f"Error: File '{filepath}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        if (args.action):
            print(f"::error file={filepath.name},title=Read error::Error reading file: {e}")
        else:
            print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    word_count = count_words(content)
    markdown_notations = list_markdown_notations(content)
    markdown_notation_count = len(markdown_notations)
    unique_notations = set(markdown_notations)
    unique_notation_count = len(set(markdown_notations))
    unique_notation_list = ', '.join(sorted(unique_notations))
    
    # One-line output
    if (args.action):
        print(f"::notice file={filepath.name},title=Markdown summary::{word_count} words, {markdown_notation_count} markdown_symbols, {unique_notation_count} unique_codes: {unique_notation_list}")
    else:
        print(f"{filepath.name}, {word_count} words, {markdown_notation_count} markdown_symbols, {unique_notation_count} unique_codes: {unique_notation_list}")

if __name__ == "__main__":
    main()

"""

**Word count algorithm rationale:**

The algorithm excludes content that isn't "document words":
1. **Code blocks removed** - not prose
2. **Inline code removed** - typically technical identifiers, not words
3. **HTML tags removed** - markup, not content
4. **Link URLs removed** - keep link text (those are words), discard URLs
5. **Images removed entirely** - alt text is often filenames/technical
6. **Markdown notation stripped** - removes #, *, _, etc.

This gives a count of actual prose words in the document.

**Alternative algorithms to consider:**

- **More inclusive**: Keep inline code, alt text → higher counts, includes all visible text
- **More strict**: Remove headings, emphasis entirely → lower counts, only body text
- **Simple split**: Just `len(content.split())` → fastest but counts everything including URLs

The current approach balances "words a human reader would read as prose" while being deterministic and fast.

**Example output:**

README.md: 1247 words: 8 codes: bold_asterisk, code_block, heading, inline_code, link, ordered_list, table_pipe, unordered_list

"""
