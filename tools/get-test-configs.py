#!/usr/bin/env python3
"""
Group markdown files by test configuration.

This utility scans markdown files for test configurations in their front matter
and groups them by identical (test_apps, server_url, local_database) properties.
This allows GitHub Actions workflows to efficiently run tests by starting each
unique server configuration once and testing all files that use it.

Usage:
    get-test-configs.py <file1.md> [file2.md ...] [--action [LEVEL]] [--output FORMAT]

Arguments:
    files: One or more markdown files to process
    --action: Optional flag to output GitHub Actions annotations
              Optional LEVEL: all, warning (default), error
    --output: Output format (json or shell, default: json)

Examples:
    get-test-configs.py docs/api/*.md
    get-test-configs.py docs/api/*.md --output json
    get-test-configs.py docs/api/*.md --output shell
    get-test-configs.py --action docs/api/*.md
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

from doc_test_utils import read_markdown_file, parse_front_matter, get_server_database_key, log


def group_files_by_config(filepaths: List[Path], use_actions: bool = False, 
                         action_level: str = "warning") -> Dict[Tuple, List[str]]:
    """
    Group files by their test configuration.
    
    Args:
        filepaths: List of markdown file paths to process
        use_actions: Whether to output GitHub Actions annotations
        action_level: Minimum severity level for annotations
        
    Returns:
        Dictionary mapping (test_apps, server_url, local_database) tuples to file lists
        
    Example:
        >>> groups = group_files_by_config([Path('api1.md'), Path('api2.md')])
        >>> for config, files in groups.items():
        ...     print(f"Config: {config}")
        ...     print(f"Files: {files}")
    """
    groups: Dict[Tuple, List[str]] = {}
    skipped_files: List[str] = []
    error_files: List[str] = []
    
    for filepath in filepaths:
        # Read file
        content = read_markdown_file(filepath)
        if content is None:
            error_files.append(str(filepath))
            log(f"Skipping {filepath.name}: Unable to read file",
                "error", str(filepath), None, use_actions, action_level)
            continue
        
        # Parse front matter
        metadata = parse_front_matter(content)
        if metadata is None:
            skipped_files.append(str(filepath))
            log(f"Skipping {filepath.name}: No front matter found",
                "notice", str(filepath), None, use_actions, action_level)
            continue
        
        # Check for test configuration
        test_config = metadata.get('test', {})
        if not test_config:
            skipped_files.append(str(filepath))
            log(f"Skipping {filepath.name}: No test configuration",
                "notice", str(filepath), None, use_actions, action_level)
            continue
        
        # Get configuration key
        config_key = get_server_database_key(metadata)
        
        # Check if configuration is complete
        test_apps, server_url, local_database = config_key
        if not test_apps or not server_url or not local_database:
            skipped_files.append(str(filepath))
            missing = []
            if not test_apps:
                missing.append("test_apps")
            if not server_url:
                missing.append("server_url")
            if not local_database:
                missing.append("local_database")
            
            log(f"Skipping {filepath.name}: Incomplete test config (missing: {', '.join(missing)})",
                "warning", str(filepath), None, use_actions, action_level)
            continue
        
        # Add to appropriate group
        if config_key not in groups:
            groups[config_key] = []
        groups[config_key].append(str(filepath))
    
    # Summary logging
    total_files = len(filepaths)
    grouped_files = sum(len(files) for files in groups.values())
    
    log(f"Processed {total_files} file(s)", "info")
    log(f"Grouped {grouped_files} testable file(s) into {len(groups)} configuration(s)", "info")
    
    if skipped_files:
        log(f"Skipped {len(skipped_files)} file(s) without complete test config", "info")
    
    if error_files:
        log(f"Failed to read {len(error_files)} file(s)", "error", 
            None, None, use_actions, action_level)
    
    return groups


def output_json(groups: Dict[Tuple, List[str]]) -> None:
    """
    Output groups as JSON.
    
    Format:
    {
        "groups": [
            {
                "test_apps": ["json-server@0.17.4"],
                "server_url": "localhost:3000",
                "local_database": "/api/test.json",
                "files": ["file1.md", "file2.md"]
            }
        ]
    }
    """
    output = {"groups": []}
    
    for config_key, files in groups.items():
        test_apps, server_url, local_database = config_key
        
        # Convert test_apps back to list
        test_apps_list = test_apps.split(',') if test_apps else []
        
        output["groups"].append({
            "test_apps": test_apps_list,
            "server_url": server_url,
            "local_database": local_database,
            "files": files
        })
    
    print(json.dumps(output, indent=2))


def output_shell(groups: Dict[Tuple, List[str]]) -> None:
    """
    Output groups as shell variables.
    
    Format for GitHub Actions:
    GROUP_1_TEST_APPS=json-server@0.17.4
    GROUP_1_SERVER_URL=localhost:3000
    GROUP_1_LOCAL_DATABASE=/api/test.json
    GROUP_1_FILES=file1.md file2.md
    GROUP_COUNT=1
    """
    group_num = 0
    
    for config_key, files in groups.items():
        group_num += 1
        test_apps, server_url, local_database = config_key
        
        print(f"GROUP_{group_num}_TEST_APPS={test_apps}")
        print(f"GROUP_{group_num}_SERVER_URL={server_url}")
        print(f"GROUP_{group_num}_LOCAL_DATABASE={local_database}")
        print(f"GROUP_{group_num}_FILES={' '.join(files)}")
    
    print(f"GROUP_COUNT={group_num}")


def main():
    parser = argparse.ArgumentParser(
        description='Group markdown files by test configuration.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s docs/api/*.md                    # JSON output
  %(prog)s docs/api/*.md --output shell     # Shell variables
  %(prog)s --action docs/api/*.md           # GitHub Actions mode
        """
    )
    
    parser.add_argument(
        'files',
        type=str,
        nargs='+',
        help='Markdown files to process'
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
        '--output', '-o',
        type=str,
        default='json',
        choices=['json', 'shell'],
        help='Output format (default: json)'
    )
    
    args = parser.parse_args()
    
    # Convert file arguments to Path objects
    filepaths = [Path(f) for f in args.files]
    
    # Group files
    use_actions = args.action is not None
    groups = group_files_by_config(filepaths, use_actions, args.action or 'warning')
    
    # Check if any groups were found
    if not groups:
        log("No testable files found with complete test configurations",
            "warning", None, None, use_actions, args.action or 'warning')
        
        # Output empty result
        if args.output == 'json':
            print(json.dumps({"groups": []}, indent=2))
        else:
            print("GROUP_COUNT=0")
        
        sys.exit(0)
    
    # Output results
    if args.output == 'json':
        output_json(groups)
    else:
        output_shell(groups)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
