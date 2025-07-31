#!/usr/bin/env python3
"""
AWS Change Monitoring Tool

Monitors various AWS sources for changes that might affect the ontology:
- AWS What's New RSS feed
- CloudFormation resource types
- API documentation changes
- Service announcements

Usage:
    python tools/monitor_aws_changes.py --source whats-new --days 7
    python tools/monitor_aws_changes.py --source cloudformation --compare
    python tools/monitor_aws_changes.py --source all --output report.json
"""

import argparse
import json
import requests
import feedparser
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set
import re


class AWSChangeMonitor:
    """Monitor AWS changes from various sources."""
    
    def __init__(self, output_dir: str = "monitoring"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Core services to monitor (from PRD scope)
        self.core_services = {
            'ec2', 'lambda', 's3', 'ebs', 'rds', 'vpc', 'iam', 
            'dynamodb', 'cloudwatch', 'cloudtrail', 'aurora'
        }
        
        # Service aliases and variations
        self.service_aliases = {
            'elastic compute cloud': 'ec2',
            'simple storage service': 's3',
            'elastic block store': 'ebs',
            'relational database service': 'rds',
            'virtual private cloud': 'vpc',
            'identity and access management': 'iam',
            'amazon aurora': 'aurora'
        }

    def monitor_whats_new(self, days: int = 7) -> List[Dict]:
        """Monitor AWS What's New RSS feed for recent changes."""
        print(f"🔍 Monitoring AWS What's New for the last {days} days...")
        
        feed_url = "https://aws.amazon.com/new/feed/"
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"❌ Error fetching RSS feed: {e}")
            return []
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_changes = []
        
        for entry in feed.entries:
            # Parse entry date
            entry_date = datetime(*entry.published_parsed[:6])
            
            if entry_date < cutoff_date:
                continue
            
            # Extract relevant information
            change = {
                'title': entry.title,
                'description': entry.summary,
                'link': entry.link,
                'published': entry_date.isoformat(),
                'services': self._extract_services(entry.title + " " + entry.summary),
                'priority': self._assess_priority(entry.title, entry.summary),
                'source': 'whats-new'
            }
            
            recent_changes.append(change)
        
        print(f"📊 Found {len(recent_changes)} recent changes")
        return recent_changes

    def monitor_cloudformation_resources(self, compare_with_cache: bool = True) -> Dict:
        """Monitor CloudFormation resource types for new services."""
        print("🔍 Monitoring CloudFormation resource types...")
        
        cache_file = self.output_dir / "cf_resources_cache.json"
        
        # Get current resource types
        current_resources = self._get_cf_resource_types()
        
        result = {
            'total_resources': len(current_resources),
            'timestamp': datetime.now().isoformat(),
            'new_resources': [],
            'source': 'cloudformation'
        }
        
        if compare_with_cache and cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                
                cached_resources = set(cached_data.get('resources', []))
                current_resources_set = set(current_resources)
                
                new_resources = current_resources_set - cached_resources
                result['new_resources'] = list(new_resources)
                result['new_count'] = len(new_resources)
                
                print(f"📊 Found {len(new_resources)} new CloudFormation resource types")
            except Exception as e:
                print(f"⚠️  Error comparing with cache: {e}")
        
        # Update cache
        cache_data = {
            'resources': current_resources,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        return result

    def monitor_api_docs(self, services: List[str] = None) -> List[Dict]:
        """Monitor AWS API documentation for changes (placeholder)."""
        print("🔍 Monitoring AWS API documentation...")
        
        if services is None:
            services = list(self.core_services)
        
        # This is a placeholder - actual implementation would require
        # web scraping or API access to AWS documentation
        changes = []
        
        for service in services:
            # Placeholder for API monitoring logic
            change = {
                'service': service,
                'status': 'monitoring_not_implemented',
                'message': f'API monitoring for {service} requires additional implementation',
                'source': 'api-docs'
            }
            changes.append(change)
        
        print("⚠️  API documentation monitoring requires additional implementation")
        return changes

    def generate_report(self, changes: List[Dict], output_file: str = None) -> str:
        """Generate a comprehensive change report."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = str(self.output_dir / f"aws_changes_{timestamp}.json")
        
        # Categorize changes
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_changes': len(changes),
            'changes_by_priority': {},
            'changes_by_service': {},
            'changes_by_source': {},
            'high_priority_summary': [],
            'all_changes': changes
        }
        
        # Analyze changes
        for change in changes:
            # By priority
            priority = change.get('priority', 'medium')
            if priority not in report['changes_by_priority']:
                report['changes_by_priority'][priority] = 0
            report['changes_by_priority'][priority] += 1
            
            # By service
            services = change.get('services', [])
            for service in services:
                if service not in report['changes_by_service']:
                    report['changes_by_service'][service] = 0
                report['changes_by_service'][service] += 1
            
            # By source
            source = change.get('source', 'unknown')
            if source not in report['changes_by_source']:
                report['changes_by_source'][source] = 0
            report['changes_by_source'][source] += 1
            
            # High priority summary
            if priority == 'high':
                summary = {
                    'title': change.get('title', 'Unknown'),
                    'services': services,
                    'link': change.get('link', '')
                }
                report['high_priority_summary'].append(summary)
        
        # Save report
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {output_file}")
        return output_file

    def print_summary(self, changes: List[Dict]):
        """Print a summary of detected changes."""
        if not changes:
            print("✅ No significant changes detected")
            return
        
        print(f"\n📊 Change Summary ({len(changes)} total)")
        print("=" * 50)
        
        # Group by priority
        by_priority = {}
        by_service = {}
        
        for change in changes:
            priority = change.get('priority', 'medium')
            services = change.get('services', [])
            
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append(change)
            
            for service in services:
                if service not in by_service:
                    by_service[service] = []
                by_service[service].append(change)
        
        # Print by priority
        for priority in ['high', 'medium', 'low']:
            if priority in by_priority:
                print(f"\n{priority.upper()} Priority ({len(by_priority[priority])} items):")
                for change in by_priority[priority][:3]:  # Show top 3
                    title = change.get('title', 'Unknown')[:80]
                    services = ', '.join(change.get('services', []))
                    print(f"  • {title}")
                    if services:
                        print(f"    Services: {services}")
        
        # Print by affected service
        if by_service:
            print(f"\nAffected Services:")
            for service, service_changes in sorted(by_service.items()):
                print(f"  • {service}: {len(service_changes)} changes")

    def _extract_services(self, text: str) -> List[str]:
        """Extract AWS service names from text."""
        text_lower = text.lower()
        services = set()
        
        # Direct service name matching
        for service in self.core_services:
            if service in text_lower:
                services.add(service)
        
        # Service alias matching
        for alias, service in self.service_aliases.items():
            if alias in text_lower:
                services.add(service)
        
        # Pattern-based matching
        service_patterns = {
            r'\bec2\b': 'ec2',
            r'\bs3\b': 's3',
            r'\biam\b': 'iam',
            r'\bvpc\b': 'vpc',
            r'\brds\b': 'rds',
            r'\bebs\b': 'ebs',
            r'\blambda\b': 'lambda',
            r'\bcloudwatch\b': 'cloudwatch',
            r'\bcloudtrail\b': 'cloudtrail',
            r'\bdynamodb\b': 'dynamodb'
        }
        
        for pattern, service in service_patterns.items():
            if re.search(pattern, text_lower):
                services.add(service)
        
        return list(services)

    def _assess_priority(self, title: str, description: str) -> str:
        """Assess the priority of a change based on content."""
        text = (title + " " + description).lower()
        
        # High priority keywords
        high_priority_keywords = [
            'security', 'compliance', 'deprecat', 'breaking', 'critical',
            'policy', 'permission', 'access', 'authentication', 'authorization',
            'new service', 'general availability'
        ]
        
        # Medium priority keywords
        medium_priority_keywords = [
            'enhancement', 'feature', 'support', 'integration', 'update',
            'improve', 'launch', 'preview'
        ]
        
        # Check for high priority
        for keyword in high_priority_keywords:
            if keyword in text:
                return 'high'
        
        # Check for medium priority
        for keyword in medium_priority_keywords:
            if keyword in text:
                return 'medium'
        
        return 'low'

    def _get_cf_resource_types(self) -> List[str]:
        """Get current CloudFormation resource types (placeholder)."""
        # This is a simplified placeholder
        # Real implementation would query CloudFormation documentation or APIs
        
        # Common AWS resource types that might be monitored
        sample_resources = [
            "AWS::EC2::Instance",
            "AWS::S3::Bucket",
            "AWS::IAM::Role",
            "AWS::IAM::Policy",
            "AWS::Lambda::Function",
            "AWS::RDS::DBInstance",
            "AWS::DynamoDB::Table"
        ]
        
        return sample_resources


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Monitor AWS changes for ontology updates')
    
    parser.add_argument('--source', choices=['whats-new', 'cloudformation', 'api-docs', 'all'],
                       default='whats-new', help='Source to monitor')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of days to look back (for whats-new)')
    parser.add_argument('--services', nargs='+',
                       help='Specific services to monitor (for api-docs)')
    parser.add_argument('--output', help='Output file for detailed report')
    parser.add_argument('--compare', action='store_true',
                       help='Compare with cached data (for cloudformation)')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress console output')
    
    args = parser.parse_args()
    
    monitor = AWSChangeMonitor()
    all_changes = []
    
    try:
        if args.source in ['whats-new', 'all']:
            changes = monitor.monitor_whats_new(args.days)
            all_changes.extend(changes)
        
        if args.source in ['cloudformation', 'all']:
            cf_result = monitor.monitor_cloudformation_resources(args.compare)
            # Convert CF result to change format
            if cf_result.get('new_resources'):
                cf_change = {
                    'title': f"New CloudFormation Resources Detected",
                    'description': f"Found {len(cf_result['new_resources'])} new resource types",
                    'new_resources': cf_result['new_resources'],
                    'priority': 'medium',
                    'source': 'cloudformation'
                }
                all_changes.append(cf_change)
        
        if args.source in ['api-docs', 'all']:
            api_changes = monitor.monitor_api_docs(args.services)
            all_changes.extend(api_changes)
        
        # Generate report
        if args.output:
            monitor.generate_report(all_changes, args.output)
        
        # Print summary
        if not args.quiet:
            monitor.print_summary(all_changes)
        
    except Exception as e:
        print(f"❌ Error during monitoring: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 