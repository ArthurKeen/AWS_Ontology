#!/usr/bin/env python3
"""
Setup script for Git hooks in the AWS Ontology project.
"""

import os
import shutil
import stat
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.cli_common import create_base_parser, handle_keyboard_interrupt
from utils.logging_config import setup_tool_logging


def setup_git_hooks():
    """Set up Git hooks for the project."""
    project_root = Path(__file__).parent.parent
    hooks_source_dir = project_root / ".githooks"
    git_hooks_dir = project_root / ".git" / "hooks"
    
    # Check if we're in a Git repository
    if not git_hooks_dir.parent.exists():
        logging.error("Not in a Git repository. Please run this from the project root.")
        return False
    
    # Create hooks directory if it doesn't exist
    git_hooks_dir.mkdir(exist_ok=True)
    
    # Copy hooks from .githooks to .git/hooks
    hooks_installed = 0
    
    if hooks_source_dir.exists():
        for hook_file in hooks_source_dir.iterdir():
            if hook_file.is_file():
                dest_file = git_hooks_dir / hook_file.name
                
                try:
                    # Copy the hook file
                    shutil.copy2(hook_file, dest_file)
                    
                    # Make it executable
                    current_permissions = dest_file.stat().st_mode
                    dest_file.chmod(current_permissions | stat.S_IEXEC)
                    
                    logging.info(f"Installed {hook_file.name} hook")
                    hooks_installed += 1
                    
                except Exception as e:
                    logging.error(f"Failed to install {hook_file.name}: {e}")
                    return False
    
    if hooks_installed == 0:
        logging.info("No hooks found to install")
        return True
    
    logging.info(f"Successfully installed {hooks_installed} Git hook(s)")
    logging.info("Hooks installed:")
    logging.info("  - pre-commit: Checks ontology file synchronization")
    logging.info("To disable a hook temporarily, rename it (e.g., pre-commit -> pre-commit.disabled)")
    logging.info("To remove all hooks, run: rm .git/hooks/*")
    
    return True


@handle_keyboard_interrupt
def main():
    """Main function."""
    parser = create_base_parser(
        "setup_git_hooks",
        "Setup Git hooks for the AWS Ontology project",
        version="0.4.0"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_tool_logging("setup_git_hooks", args.verbose)
    
    logging.info("Setting up Git hooks for AWS Ontology project...")
    
    success = setup_git_hooks()
    
    if success:
        logging.info("Git hooks setup completed successfully!")
        
        # Suggest testing the hooks
        logging.info("To test the pre-commit hook:")
        logging.info("  1. Make a change to one ontology file (not both)")
        logging.info("  2. Stage it: git add ontology/aws.ttl")
        logging.info("  3. Try to commit: git commit -m 'test'")
        logging.info("  4. The hook should prevent the commit")
        
        sys.exit(0)
    else:
        logging.error("Git hooks setup failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 