#!/usr/bin/env python3
"""
Extract test database path from markdown file's front matter.

This script reads a markdown file, extracts the YAML front matter,
and outputs the test database path for use in API testing workflows.

Usage:
    get-database-path.py <markdown-file>

Output:
    Prints the database path (with leading slash removed) to stdout.
    If no database path is found, prints the default path.

Example:
    DB_PATH=$(python3 tools/get-database-path.py docs/api.md)
    echo "Using database: $DB_PATH"
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

# Import shared utilities
from doc_test_utils import read_markdown_file, parse_front_matter, log


# Default database path if not specified in front matter
DEFAULT_DATABASE_PATH = "api/to-do-db-source.json"


def get_database_path_from_metadata(filepath: Path) -> Optional[str]:
    """
    Extract test database path from a markdown file's front matter.
    
    Reads the file, parses front matter, extracts the test.local_database
    value, and strips leading slashes.
    
    Args:
        filepath: Path to the markdown file to process
        
    Returns:
        Database path with leading slash removed, or None if file cannot
        be read or front matter is invalid
        
    Example:
        >>> # File with front matter:
        >>> # ---
        >>> # test:
        >>> #   local_database: /api/test-db.json
        >>> # ---
        >>> path = get_database_path_from_metadata(Path('test.md'))
        >>> path
        'api/test-db.json'
    """
    # Read markdown file
    content = read_markdown_file(filepath)
    if content is None:
        return None
    
    # Parse front matter
    metadata = parse_front_matter(content)
    if metadata is None:
        return None
    
    # Extract test configuration
    test_config = metadata.get('test', {})
    if not isinstance(test_config, dict):
        return None
    
    # Get database path
    db_path = test_config.get('local_database')
    if db_path is None:
        return None
    
    # Strip leading slash and return
    if isinstance(db_path, str):
        return db_path.lstrip('/')
    
    return None


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Extract test database path from markdown front matter.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s docs/api-reference.md
  
  # In a shell script:
  DB_PATH=$(%(prog)s docs/api-reference.md)
  echo "Database: $DB_PATH"
  
  # With default fallback:
  DB_PATH=$(%(prog)s docs/api.md || echo "api/default.json")

Output:
  Prints database path to stdout (with leading slash removed).
  Prints to stderr if file cannot be read or has no database path.
  
Exit Codes:
  0 - Success (database path found and printed)
  1 - Error (file not found, invalid front matter, or no database path)
        """
    )
    
    parser.add_argument(
        'filepath',
        type=str,
        help='Path to the markdown file to process'
    )
    
    args = parser.parse_args()
    
    filepath = Path(args.filepath)
    
    # Extract database path
    db_path = get_database_path_from_metadata(filepath)
    
    if db_path:
        # Success - print to stdout
        print(db_path)
        sys.exit(0)
    else:
        # No database path found - print default to stdout
        # (This allows workflow to continue with default)
        print(DEFAULT_DATABASE_PATH)
        sys.exit(0)


if __name__ == "__main__":
    main()
# End of file tools/get-database-path.py