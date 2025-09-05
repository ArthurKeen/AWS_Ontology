#!/usr/bin/env python3
"""
Configuration validation utilities for the AWS Ontology project.
Provides schema-based validation for configuration files.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class NotificationConfig:
    """Configuration for email notifications."""
    enabled: bool = False
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    email_from: str = ""
    email_to: List[str] = field(default_factory=list)
    email_password: str = ""
    
    def validate(self) -> List[str]:
        """Validate notification configuration."""
        errors = []
        
        if self.enabled:
            if not self.email_from:
                errors.append("email_from is required when notifications are enabled")
            if not self.email_to:
                errors.append("email_to is required when notifications are enabled")
            if not self.email_password:
                errors.append("email_password is required when notifications are enabled")
            if not (1 <= self.smtp_port <= 65535):
                errors.append("smtp_port must be between 1 and 65535")
        
        return errors


@dataclass
class ScheduleConfig:
    """Configuration for monitoring schedules."""
    daily_monitoring: str = "09:00"
    weekly_report: str = "08:00"
    monthly_quality_check: str = "07:00"
    quarterly_review: str = "06:00"
    
    def validate(self) -> List[str]:
        """Validate schedule configuration."""
        errors = []
        
        time_fields = [
            ("daily_monitoring", self.daily_monitoring),
            ("weekly_report", self.weekly_report),
            ("monthly_quality_check", self.monthly_quality_check),
            ("quarterly_review", self.quarterly_review)
        ]
        
        for field_name, time_str in time_fields:
            if not self._is_valid_time(time_str):
                errors.append(f"{field_name} must be in HH:MM format (24-hour)")
        
        return errors
    
    @staticmethod
    def _is_valid_time(time_str: str) -> bool:
        """Check if time string is in valid HH:MM format."""
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                return False
            
            hour, minute = int(parts[0]), int(parts[1])
            return 0 <= hour <= 23 and 0 <= minute <= 59
        except (ValueError, AttributeError):
            return False


@dataclass
class DatabaseConfig:
    """Configuration for database connections."""
    host: str = "http://localhost:8529"
    username: str = "root"
    password: str = ""
    database: str = "aws_ontology"
    timeout: int = 30
    
    def validate(self) -> List[str]:
        """Validate database configuration."""
        errors = []
        
        if not self.host:
            errors.append("host is required")
        if not self.host.startswith(("http://", "https://")):
            errors.append("host must start with http:// or https://")
        if not self.username:
            errors.append("username is required")
        if not self.database:
            errors.append("database name is required")
        if not (1 <= self.timeout <= 300):
            errors.append("timeout must be between 1 and 300 seconds")
        
        return errors


@dataclass
class MonitoringConfig:
    """Configuration for monitoring settings."""
    interval_hours: int = 24
    log_level: str = "INFO"
    log_dir: str = "automation/logs"
    max_log_files: int = 30
    
    def validate(self) -> List[str]:
        """Validate monitoring configuration."""
        errors = []
        
        if not (1 <= self.interval_hours <= 168):  # 1 hour to 1 week
            errors.append("interval_hours must be between 1 and 168")
        
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level.upper() not in valid_log_levels:
            errors.append(f"log_level must be one of: {', '.join(valid_log_levels)}")
        
        if not self.log_dir:
            errors.append("log_dir is required")
        
        if not (1 <= self.max_log_files <= 365):
            errors.append("max_log_files must be between 1 and 365")
        
        return errors


@dataclass
class AppConfig:
    """Main application configuration."""
    notifications: NotificationConfig = field(default_factory=NotificationConfig)
    schedules: ScheduleConfig = field(default_factory=ScheduleConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    
    def validate(self) -> List[str]:
        """Validate entire configuration."""
        errors = []
        
        errors.extend(self.notifications.validate())
        errors.extend(self.schedules.validate())
        errors.extend(self.database.validate())
        errors.extend(self.monitoring.validate())
        
        return errors
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        """Create configuration from dictionary."""
        config = cls()
        
        if 'notifications' in data:
            notif_data = data['notifications']
            config.notifications = NotificationConfig(
                enabled=notif_data.get('enabled', False),
                smtp_server=notif_data.get('smtp_server', 'smtp.gmail.com'),
                smtp_port=notif_data.get('smtp_port', 587),
                email_from=notif_data.get('email_from', ''),
                email_to=notif_data.get('email_to', []),
                email_password=notif_data.get('email_password', '')
            )
        
        if 'schedules' in data:
            sched_data = data['schedules']
            config.schedules = ScheduleConfig(
                daily_monitoring=sched_data.get('daily_monitoring', '09:00'),
                weekly_report=sched_data.get('weekly_report', '08:00'),
                monthly_quality_check=sched_data.get('monthly_quality_check', '07:00'),
                quarterly_review=sched_data.get('quarterly_review', '06:00')
            )
        
        if 'database' in data:
            db_data = data['database']
            config.database = DatabaseConfig(
                host=db_data.get('host', 'http://localhost:8529'),
                username=db_data.get('username', 'root'),
                password=db_data.get('password', ''),
                database=db_data.get('database', 'aws_ontology'),
                timeout=db_data.get('timeout', 30)
            )
        
        if 'monitoring' in data:
            mon_data = data['monitoring']
            config.monitoring = MonitoringConfig(
                interval_hours=mon_data.get('interval_hours', 24),
                log_level=mon_data.get('log_level', 'INFO'),
                log_dir=mon_data.get('log_dir', 'automation/logs'),
                max_log_files=mon_data.get('max_log_files', 30)
            )
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'notifications': {
                'enabled': self.notifications.enabled,
                'smtp_server': self.notifications.smtp_server,
                'smtp_port': self.notifications.smtp_port,
                'email_from': self.notifications.email_from,
                'email_to': self.notifications.email_to,
                'email_password': self.notifications.email_password
            },
            'schedules': {
                'daily_monitoring': self.schedules.daily_monitoring,
                'weekly_report': self.schedules.weekly_report,
                'monthly_quality_check': self.schedules.monthly_quality_check,
                'quarterly_review': self.schedules.quarterly_review
            },
            'database': {
                'host': self.database.host,
                'username': self.database.username,
                'password': self.database.password,
                'database': self.database.database,
                'timeout': self.database.timeout
            },
            'monitoring': {
                'interval_hours': self.monitoring.interval_hours,
                'log_level': self.monitoring.log_level,
                'log_dir': self.monitoring.log_dir,
                'max_log_files': self.monitoring.max_log_files
            }
        }


def load_and_validate_config(config_path: Path) -> Optional[AppConfig]:
    """
    Load and validate configuration from file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Validated configuration or None if invalid
    """
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        config = AppConfig.from_dict(data)
        errors = config.validate()
        
        if errors:
            logging.error("Configuration validation failed:")
            for error in errors:
                logging.error(f"  - {error}")
            return None
        
        logging.info(f"Configuration loaded successfully from {config_path}")
        return config
        
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in configuration file: {e}")
        return None
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return None


def create_sample_config(output_path: Path) -> bool:
    """
    Create a sample configuration file.
    
    Args:
        output_path: Path where to create the sample config
        
    Returns:
        True if successful, False otherwise
    """
    try:
        sample_config = AppConfig()
        sample_config.notifications.enabled = True
        sample_config.notifications.email_from = "your-email@gmail.com"
        sample_config.notifications.email_to = ["recipient@example.com"]
        sample_config.notifications.email_password = "your-app-password"
        
        with open(output_path, 'w') as f:
            json.dump(sample_config.to_dict(), f, indent=2)
        
        logging.info(f"Sample configuration created: {output_path}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to create sample configuration: {e}")
        return False
