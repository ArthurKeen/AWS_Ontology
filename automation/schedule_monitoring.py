#!/usr/bin/env python3
"""
Automated Scheduling Script for AWS Ontology Monitoring

Provides automated scheduling for:
- Daily AWS change monitoring
- Weekly comprehensive reports
- Monthly quality checks
- Periodic ontology testing

Usage:
    python automation/schedule_monitoring.py --start-daemon
    python automation/schedule_monitoring.py --run-once daily
    python automation/schedule_monitoring.py --config config.json
"""

import argparse
import json
import schedule
import time
import subprocess
import logging
import smtplib
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import sys
import os


class OntologyScheduler:
    """Automated scheduler for ontology monitoring and maintenance."""
    
    def __init__(self, config_file: str = None):
        self.project_root = Path(__file__).parent.parent
        self.config = self._load_config(config_file)
        self._setup_logging()
        
    def _load_config(self, config_file: str = None) -> dict:
        """Load configuration from file or use defaults."""
        default_config = {
            "notifications": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "email_from": "",
                "email_to": [],
                "email_password": ""
            },
            "schedules": {
                "daily_monitoring": "09:00",
                "weekly_report": "Monday 08:00",
                "monthly_quality_check": "1st 07:00",
                "quarterly_review": "1st of quarter 06:00"
            },
            "thresholds": {
                "high_priority_notify": True,
                "test_failure_notify": True,
                "performance_degradation_notify": True
            },
            "output_dirs": {
                "reports": "automation/reports",
                "logs": "automation/logs"
            }
        }
        
        if config_file and Path(config_file).exists():
            try:
                with open(config_file, 'r') as f:
                    custom_config = json.load(f)
                # Merge custom config with defaults
                default_config.update(custom_config)
            except Exception as e:
                print(f"Warning: Could not load config file {config_file}: {e}")
        
        return default_config
    
    def _setup_logging(self):
        """Set up logging configuration."""
        log_dir = Path(self.config["output_dirs"]["logs"])
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"scheduler_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def daily_monitoring(self):
        """Run daily AWS change monitoring."""
        self.logger.info("🔍 Starting daily AWS change monitoring...")
        
        try:
            # Generate timestamp for report
            timestamp = datetime.now().strftime("%Y%m%d")
            report_dir = Path(self.config["output_dirs"]["reports"])
            report_dir.mkdir(parents=True, exist_ok=True)
            report_file = report_dir / f"daily_changes_{timestamp}.json"
            
            # Run monitoring
            cmd = [
                "python", "tools/monitor_aws_changes.py",
                "--source", "whats-new",
                "--days", "1",
                "--output", str(report_file)
            ]
            
            result = subprocess.run(
                cmd, cwd=self.project_root, 
                capture_output=True, text=True, timeout=300
            )
            
            if result.returncode == 0:
                self.logger.info(f"✅ Daily monitoring completed. Report: {report_file}")
                
                # Check for high-priority changes
                if report_file.exists():
                    with open(report_file, 'r') as f:
                        report_data = json.load(f)
                    
                    high_priority_changes = report_data.get('changes_by_priority', {}).get('high', 0)
                    
                    if high_priority_changes > 0 and self.config["thresholds"]["high_priority_notify"]:
                        self._send_notification(
                            subject=f"🚨 High Priority AWS Changes Detected ({high_priority_changes})",
                            message=f"Found {high_priority_changes} high-priority AWS changes requiring attention.",
                            attachment=str(report_file)
                        )
                
            else:
                self.logger.error(f"❌ Daily monitoring failed: {result.stderr}")
                self._send_notification(
                    subject="❌ Daily AWS Monitoring Failed",
                    message=f"Daily monitoring failed with error: {result.stderr}"
                )
                
        except Exception as e:
            self.logger.error(f"❌ Daily monitoring error: {e}")
            self._send_notification(
                subject="❌ Daily Monitoring Error",
                message=f"Daily monitoring encountered an error: {str(e)}"
            )
    
    def weekly_report(self):
        """Generate comprehensive weekly report."""
        self.logger.info("📊 Starting weekly comprehensive report...")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d")
            report_dir = Path(self.config["output_dirs"]["reports"])
            report_dir.mkdir(parents=True, exist_ok=True)
            report_file = report_dir / f"weekly_report_{timestamp}.json"
            
            # Run comprehensive monitoring
            cmd = [
                "python", "tools/monitor_aws_changes.py",
                "--source", "all",
                "--days", "7",
                "--compare",
                "--output", str(report_file)
            ]
            
            result = subprocess.run(
                cmd, cwd=self.project_root,
                capture_output=True, text=True, timeout=600
            )
            
            if result.returncode == 0:
                self.logger.info(f"✅ Weekly report completed. Report: {report_file}")
                
                # Always send weekly report
                self._send_notification(
                    subject=f"📊 Weekly AWS Ontology Report - {datetime.now().strftime('%Y-%m-%d')}",
                    message="Weekly comprehensive AWS change report attached.",
                    attachment=str(report_file)
                )
            else:
                self.logger.error(f"❌ Weekly report failed: {result.stderr}")
                
        except Exception as e:
            self.logger.error(f"❌ Weekly report error: {e}")
    
    def monthly_quality_check(self):
        """Run monthly quality and performance checks."""
        self.logger.info("🔍 Starting monthly quality checks...")
        
        try:
            # Run comprehensive test suite
            test_cmd = ["make", "test-all"]
            test_result = subprocess.run(
                test_cmd, cwd=self.project_root,
                capture_output=True, text=True, timeout=1800
            )
            
            # Run performance tests specifically
            perf_cmd = ["make", "test-performance"]
            perf_result = subprocess.run(
                perf_cmd, cwd=self.project_root,
                capture_output=True, text=True, timeout=600
            )
            
            # Compile results
            results = {
                "date": datetime.now().isoformat(),
                "comprehensive_tests": {
                    "passed": test_result.returncode == 0,
                    "output": test_result.stdout,
                    "errors": test_result.stderr
                },
                "performance_tests": {
                    "passed": perf_result.returncode == 0,
                    "output": perf_result.stdout,
                    "errors": perf_result.stderr
                }
            }
            
            # Save results
            report_dir = Path(self.config["output_dirs"]["reports"])
            report_dir.mkdir(parents=True, exist_ok=True)
            report_file = report_dir / f"monthly_quality_{datetime.now().strftime('%Y%m')}.json"
            
            with open(report_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            # Determine notification
            if not results["comprehensive_tests"]["passed"] or not results["performance_tests"]["passed"]:
                subject = "⚠️ Monthly Quality Check Issues Detected"
                message = "Monthly quality checks found issues that require attention."
                
                if self.config["thresholds"]["test_failure_notify"]:
                    self._send_notification(subject, message, str(report_file))
            else:
                self.logger.info("✅ Monthly quality checks passed")
                subject = "✅ Monthly Quality Check - All Passed"
                message = "All monthly quality and performance checks passed successfully."
                self._send_notification(subject, message, str(report_file))
                
        except Exception as e:
            self.logger.error(f"❌ Monthly quality check error: {e}")
    
    def quarterly_review(self):
        """Comprehensive quarterly review."""
        self.logger.info("📋 Starting quarterly comprehensive review...")
        
        try:
            # This would trigger a more comprehensive review process
            # For now, we'll generate a summary report
            
            review_data = {
                "date": datetime.now().isoformat(),
                "quarter": f"Q{((datetime.now().month-1)//3)+1} {datetime.now().year}",
                "action_required": "Manual comprehensive review needed",
                "checklist": [
                    "Review ontology completeness against current AWS services",
                    "Update maintenance strategy based on AWS evolution patterns",
                    "Assess tool performance and optimization needs",
                    "Update documentation and examples",
                    "Plan next quarter's focus areas"
                ]
            }
            
            report_dir = Path(self.config["output_dirs"]["reports"])
            report_dir.mkdir(parents=True, exist_ok=True)
            report_file = report_dir / f"quarterly_review_{datetime.now().strftime('%Y_Q%q')}.json"
            
            with open(report_file, 'w') as f:
                json.dump(review_data, f, indent=2)
            
            self._send_notification(
                subject=f"📋 Quarterly Review Due - {review_data['quarter']}",
                message="Quarterly comprehensive review is due. Manual review checklist attached.",
                attachment=str(report_file)
            )
            
        except Exception as e:
            self.logger.error(f"❌ Quarterly review error: {e}")
    
    def _send_notification(self, subject: str, message: str, attachment: str = None):
        """Send email notification if configured."""
        if not self.config["notifications"]["enabled"]:
            self.logger.info(f"Notification (not sent): {subject}")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["notifications"]["email_from"]
            msg['To'] = ", ".join(self.config["notifications"]["email_to"])
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Add attachment if provided
            if attachment and Path(attachment).exists():
                with open(attachment, "rb") as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {Path(attachment).name}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(
                self.config["notifications"]["smtp_server"],
                self.config["notifications"]["smtp_port"]
            )
            server.starttls()
            server.login(
                self.config["notifications"]["email_from"],
                self.config["notifications"]["email_password"]
            )
            
            server.sendmail(
                self.config["notifications"]["email_from"],
                self.config["notifications"]["email_to"],
                msg.as_string()
            )
            server.quit()
            
            self.logger.info(f"📧 Notification sent: {subject}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to send notification: {e}")
    
    def setup_schedule(self):
        """Set up the monitoring schedule."""
        self.logger.info("⏰ Setting up monitoring schedule...")
        
        # Daily monitoring
        schedule.every().day.at(self.config["schedules"]["daily_monitoring"]).do(self.daily_monitoring)
        
        # Weekly report (e.g., "Monday 08:00")
        weekly_parts = self.config["schedules"]["weekly_report"].split()
        if len(weekly_parts) == 2:
            day, time_str = weekly_parts
            getattr(schedule.every(), day.lower()).at(time_str).do(self.weekly_report)
        
        # Monthly quality check (1st of month)
        schedule.every().month.do(self.monthly_quality_check)
        
        # Quarterly review
        schedule.every(3).months.do(self.quarterly_review)
        
        self.logger.info("✅ Schedule configured successfully")
        
        # Log next run times
        for job in schedule.jobs:
            self.logger.info(f"  Next run: {job.next_run} - {job.job_func.__name__}")
    
    def run_daemon(self):
        """Run the scheduler as a daemon."""
        self.logger.info("🚀 Starting scheduler daemon...")
        self.setup_schedule()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("⏹️ Scheduler stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Scheduler daemon error: {e}")
    
    def run_once(self, task: str):
        """Run a specific task once."""
        self.logger.info(f"▶️ Running task: {task}")
        
        task_map = {
            "daily": self.daily_monitoring,
            "weekly": self.weekly_report,
            "monthly": self.monthly_quality_check,
            "quarterly": self.quarterly_review
        }
        
        if task in task_map:
            task_map[task]()
        else:
            self.logger.error(f"❌ Unknown task: {task}")


def create_sample_config(filename: str):
    """Create a sample configuration file."""
    sample_config = {
        "notifications": {
            "enabled": False,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "email_from": "your-email@gmail.com",
            "email_to": ["recipient@example.com"],
            "email_password": "your-app-password"
        },
        "schedules": {
            "daily_monitoring": "09:00",
            "weekly_report": "monday 08:00",
            "monthly_quality_check": "1st 07:00",
            "quarterly_review": "1st of quarter 06:00"
        },
        "thresholds": {
            "high_priority_notify": True,
            "test_failure_notify": True,
            "performance_degradation_notify": True
        },
        "output_dirs": {
            "reports": "automation/reports",
            "logs": "automation/logs"
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print(f"✅ Sample configuration created: {filename}")
    print("📝 Edit this file to configure notifications and schedules")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Automated AWS Ontology Monitoring Scheduler')
    
    parser.add_argument('--start-daemon', action='store_true',
                       help='Start the scheduler daemon')
    parser.add_argument('--run-once', choices=['daily', 'weekly', 'monthly', 'quarterly'],
                       help='Run a specific task once')
    parser.add_argument('--config', default='automation/config.json',
                       help='Configuration file path')
    parser.add_argument('--create-config', action='store_true',
                       help='Create sample configuration file')
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_config(args.config)
        return 0
    
    scheduler = OntologyScheduler(args.config)
    
    if args.start_daemon:
        scheduler.run_daemon()
    elif args.run_once:
        scheduler.run_once(args.run_once)
    else:
        print("No action specified. Use --help for usage information.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 