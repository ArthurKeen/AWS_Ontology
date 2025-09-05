#!/usr/bin/env python3
"""
Logging configuration utilities for the AWS Ontology project.
Provides consistent logging setup across all modules.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up structured logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file to write logs to
        format_string: Custom format string for log messages
        
    Returns:
        Configured logger instance
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=[]
    )
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(format_string))
    
    # Add file handler if specified
    handlers = [console_handler]
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(format_string))
        handlers.append(file_handler)
    
    # Configure root logger with handlers
    root_logger = logging.getLogger()
    root_logger.handlers = handlers
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def setup_tool_logging(tool_name: str, verbose: bool = False) -> logging.Logger:
    """
    Set up logging for command-line tools with appropriate formatting.
    
    Args:
        tool_name: Name of the tool for log identification
        verbose: Enable verbose (DEBUG) logging
        
    Returns:
        Configured logger for the tool
    """
    level = "DEBUG" if verbose else "INFO"
    format_string = f"[{tool_name}] %(levelname)s: %(message)s"
    
    setup_logging(level=level, format_string=format_string)
    return get_logger(tool_name)
