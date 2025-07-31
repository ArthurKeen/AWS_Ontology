#!/usr/bin/env python3
"""
Setup script for Git hooks in the AWS Ontology project.
"""

import os
import shutil
import stat
import sys
from pathlib import Path


def setup_git_hooks():
    """Set up Git hooks for the project."""
    project_root = Path(__file__).parent.parent
    hooks_source_dir = project_root / ".githooks"
    git_hooks_dir = project_root / ".git" / "hooks"
    
    # Check if we're in a Git repository
    if not git_hooks_dir.parent.exists():
        print("❌ Not in a Git repository. Please run this from the project root.")
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
                    
                    print(f"✅ Installed {hook_file.name} hook")
                    hooks_installed += 1
                    
                except Exception as e:
                    print(f"❌ Failed to install {hook_file.name}: {e}")
                    return False
    
    if hooks_installed == 0:
        print("ℹ️  No hooks found to install")
        return True
    
    print(f"\n🎉 Successfully installed {hooks_installed} Git hook(s)")
    print("\nHooks installed:")
    print("  - pre-commit: Checks ontology file synchronization")
    print("\nTo disable a hook temporarily, rename it (e.g., pre-commit -> pre-commit.disabled)")
    print("To remove all hooks, run: rm .git/hooks/*")
    
    return True


def main():
    """Main function."""
    print("Setting up Git hooks for AWS Ontology project...")
    print("=" * 50)
    
    success = setup_git_hooks()
    
    if success:
        print("\n✅ Git hooks setup completed successfully!")
        
        # Suggest testing the hooks
        print("\nTo test the pre-commit hook:")
        print("  1. Make a change to one ontology file (not both)")
        print("  2. Stage it: git add ontology/aws.ttl")
        print("  3. Try to commit: git commit -m 'test'")
        print("  4. The hook should prevent the commit")
        
        sys.exit(0)
    else:
        print("\n❌ Git hooks setup failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 