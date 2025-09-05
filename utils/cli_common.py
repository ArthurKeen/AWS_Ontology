#!/usr/bin/env python3
"""
Common CLI utilities for AWS Ontology tools.
Provides consistent argument parsing and help formatting.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Dict, Any


def create_base_parser(
    tool_name: str,
    description: str,
    version: Optional[str] = None
) -> argparse.ArgumentParser:
    """
    Create a base argument parser with common options.
    
    Args:
        tool_name: Name of the tool
        description: Tool description
        version: Optional version string
        
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog=tool_name,
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  {tool_name} --help          Show this help message
  {tool_name} --verbose       Enable verbose logging
  {tool_name} --version       Show version information

For more information, see docs/ directory.
        """
    )
    
    # Common arguments
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress non-error output'
    )
    
    if version:
        parser.add_argument(
            '--version',
            action='version',
            version=f'{tool_name} {version}'
        )
    
    return parser


def add_database_args(parser: argparse.ArgumentParser) -> None:
    """
    Add common database connection arguments.
    
    Args:
        parser: ArgumentParser to add arguments to
    """
    db_group = parser.add_argument_group('Database Options')
    
    db_group.add_argument(
        '--host',
        default='http://localhost:8529',
        help='ArangoDB host (default: http://localhost:8529)'
    )
    
    db_group.add_argument(
        '--username',
        default='root',
        help='ArangoDB username (default: root)'
    )
    
    db_group.add_argument(
        '--password',
        default=None,
        help='ArangoDB password (default: from ARANGO_PASSWORD env var)'
    )
    
    db_group.add_argument(
        '--database',
        default='aws_ontology',
        help='Database name (default: aws_ontology)'
    )


def add_file_args(parser: argparse.ArgumentParser) -> None:
    """
    Add common file operation arguments.
    
    Args:
        parser: ArgumentParser to add arguments to
    """
    file_group = parser.add_argument_group('File Options')
    
    file_group.add_argument(
        '--output', '-o',
        type=Path,
        help='Output file path'
    )
    
    file_group.add_argument(
        '--format',
        choices=['ttl', 'owl', 'json', 'xml'],
        default='ttl',
        help='Output format (default: ttl)'
    )
    
    file_group.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing files'
    )


def validate_args(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Validate and normalize command line arguments.
    
    Args:
        args: Parsed arguments from ArgumentParser
        
    Returns:
        Dictionary of validated arguments
        
    Raises:
        SystemExit: If validation fails
    """
    validated = vars(args).copy()
    
    # Validate conflicting options
    if getattr(args, 'verbose', False) and getattr(args, 'quiet', False):
        print("Error: --verbose and --quiet are mutually exclusive", file=sys.stderr)
        sys.exit(1)
    
    # Validate file paths
    if hasattr(args, 'output') and args.output:
        output_path = Path(args.output)
        if output_path.exists() and not getattr(args, 'overwrite', False):
            print(f"Error: Output file exists: {output_path}", file=sys.stderr)
            print("Use --overwrite to replace existing files", file=sys.stderr)
            sys.exit(1)
    
    return validated


def print_tool_header(tool_name: str, version: Optional[str] = None) -> None:
    """
    Print a consistent tool header.
    
    Args:
        tool_name: Name of the tool
        version: Optional version string
    """
    header = f"AWS Ontology - {tool_name}"
    if version:
        header += f" v{version}"
    
    print(header)
    print("=" * len(header))
    print()


def handle_keyboard_interrupt(func):
    """
    Decorator to handle KeyboardInterrupt gracefully.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user", file=sys.stderr)
            sys.exit(130)  # Standard exit code for SIGINT
    
    return wrapper
