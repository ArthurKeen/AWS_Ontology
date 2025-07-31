# AWS Ontology Project Makefile

.PHONY: help test test-all test-sync test-quality test-examples test-performance sync-check sync-ttl-to-owl sync-owl-to-ttl install-deps setup-hooks monitor-changes clean

# Default target
help:
	@echo "AWS Ontology Project - Available Commands:"
	@echo ""
	@echo "Testing:"
	@echo "  test           - Run essential tests"
	@echo "  test-all       - Run comprehensive test suite"
	@echo "  test-sync      - Test OWL/TTL format synchronization"
	@echo "  test-quality   - Test ontology quality and structure"
	@echo "  test-examples  - Test example instances validation"
	@echo "  test-performance - Test ontology performance metrics"
	@echo ""
	@echo "Synchronization:"
	@echo "  sync-check     - Check if OWL and TTL files are synchronized"
	@echo "  sync-ttl-to-owl - Convert TTL to OWL format"
	@echo "  sync-owl-to-ttl - Convert OWL to TTL format"
	@echo ""
	@echo "Development:"
	@echo "  install-deps   - Install Python dependencies"
	@echo "  setup-hooks    - Install Git pre-commit hooks"
	@echo "  transform      - Run ArangoDB transformation (requires ArangoDB)"
	@echo ""
	@echo "Monitoring:"
	@echo "  monitor-changes - Monitor AWS changes (last 7 days)"
	@echo "  monitor-weekly  - Generate weekly AWS change report"
	@echo "  monitor-all     - Monitor all sources and generate report"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean          - Clean temporary files"
	@echo ""

# Install Python dependencies
install-deps:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

# Set up Git hooks
setup-hooks:
	@echo "Setting up Git hooks..."
	python3 tools/setup_git_hooks.py

# Run essential tests
test: test-sync
	@echo "Essential tests completed!"

# Run comprehensive test suite
test-all: test-sync test-quality test-examples test-performance
	@echo "All tests completed!"

# Test format synchronization
test-sync:
	@echo "Testing OWL/TTL synchronization..."
	python tests/test_format_sync.py

# Test ontology quality
test-quality:
	@echo "Testing ontology quality..."
	python tests/test_ontology_quality.py

# Test examples validation
test-examples:
	@echo "Testing example instances..."
	python tests/test_examples_validation.py

# Test performance
test-performance:
	@echo "Testing ontology performance..."
	python tests/test_performance.py

# Check synchronization status
sync-check:
	@echo "Checking synchronization status..."
	python tools/sync_formats.py check

# Convert TTL to OWL
sync-ttl-to-owl:
	@echo "Converting TTL to OWL..."
	python tools/sync_formats.py ttl-to-owl

# Convert OWL to TTL
sync-owl-to-ttl:
	@echo "Converting OWL to TTL..."
	python tools/sync_formats.py owl-to-ttl

# Monitor AWS changes (last 7 days)
monitor-changes:
	@echo "Monitoring AWS changes (last 7 days)..."
	python tools/monitor_aws_changes.py --source whats-new --days 7

# Generate weekly change report
monitor-weekly:
	@echo "Generating weekly AWS change report..."
	python tools/monitor_aws_changes.py --source all --days 7 --output monitoring/weekly_report.json

# Monitor all sources with detailed report
monitor-all:
	@echo "Monitoring all AWS sources..."
	python tools/monitor_aws_changes.py --source all --compare --output monitoring/comprehensive_report.json

# Run ArangoDB transformation
transform:
	@echo "Running ArangoDB transformation..."
	python tools/transform_ontology.py

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.tmp" -delete
	@echo "Creating monitoring directory..."
	mkdir -p monitoring 