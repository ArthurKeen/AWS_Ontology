# AWS Ontology Project Makefile

.PHONY: help test test-sync sync-check sync-ttl-to-owl sync-owl-to-ttl install-deps clean

# Default target
help:
	@echo "AWS Ontology Project - Available Commands:"
	@echo ""
	@echo "  test           - Run all tests"
	@echo "  test-sync      - Test OWL/TTL format synchronization"
	@echo "  sync-check     - Check if OWL and TTL files are synchronized"
	@echo "  sync-ttl-to-owl - Convert TTL to OWL format"
	@echo "  sync-owl-to-ttl - Convert OWL to TTL format"
	@echo "  install-deps   - Install Python dependencies"
	@echo "  transform      - Run ArangoDB transformation (requires ArangoDB)"
	@echo "  clean          - Clean temporary files"
	@echo ""

# Install Python dependencies
install-deps:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

# Run all tests
test: test-sync
	@echo "All tests completed!"

# Test format synchronization
test-sync:
	@echo "Testing OWL/TTL synchronization..."
	python tests/test_format_sync.py

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