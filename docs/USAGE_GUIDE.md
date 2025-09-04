# AWS Ontology Usage Guide

This guide provides step-by-step instructions for using all the tools and features in the AWS Ontology project.

## Quick Start

### 1. Initial Setup

```bash
# Clone the repository (if not already done)
git clone https://github.com/ArthurKeen/AWS_Ontology.git
cd AWS_Ontology

# Set up Python virtual environment (required)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install core dependencies
pip install rdflib owlready2 feedparser

# Install ArangoRDF from local clone (if available)
pip install -e ~/code/ArangoRDF

# OR install remaining dependencies manually
pip install python-arango

# Set up Git hooks
make setup-hooks
```

### 2. Verify Installation

```bash
# Check that core files exist
ls ontology/aws.owl ontology/aws.ttl ontology/examples.ttl

# Run basic tests
make test

# Show available commands
make help
```

## Working with the Ontology

### Viewing and Editing

**Recommended Tools:**
- **Protégé**: For graphical OWL editing (`aws.owl`)
- **Text Editor**: For TTL editing (`aws.ttl`) 
- **VS Code**: With Turtle/RDF extensions

**File Formats:**
- `ontology/aws.owl` - Standard OWL/XML format
- `ontology/aws.ttl` - Human-readable Turtle format
- `ontology/examples.ttl` - Example instances

### Making Changes

```bash
# Before making changes, ensure formats are synchronized
make sync-check

# After editing either format, sync the other
make sync-ttl-to-owl  # If you edited the TTL file
make sync-owl-to-ttl  # If you edited the OWL file

# Run tests to validate changes
make test-all

# Commit changes (pre-commit hook will check sync)
git add ontology/
git commit -m "Description of changes"
```

## Testing

### Test Categories

```bash
# Essential tests (format synchronization)
make test

# Comprehensive test suite
make test-all

# Individual test categories
make test-sync        # Format synchronization
make test-quality     # Ontology structure and consistency
make test-examples    # Example instance validation
make test-performance # Performance metrics
```

### Understanding Test Results

**Synchronization Tests:**
- Ensures OWL and TTL files contain identical semantic content
- Validates version consistency
- Checks triple count matching

**Quality Tests:**
- Validates ontology structure and completeness
- Checks all classes and properties have documentation
- Verifies proper domain/range declarations
- Tests OWL DL compliance

**Example Tests:**
- Validates example instances against ontology
- Checks policy document formats
- Verifies reference integrity

**Performance Tests:**
- Measures loading time (target: <5 seconds)
- Monitors memory usage (target: <500MB)
- Tests query performance (target: <1-2 seconds)

## Monitoring AWS Changes

### Basic Monitoring

```bash
# Monitor AWS What's New for last 7 days (quick check)
make monitor-changes

# Generate weekly comprehensive report
make monitor-weekly

# Full analysis across all sources
make monitor-all
```

### Advanced Monitoring

```bash
# Monitor specific timeframe
python tools/monitor_aws_changes.py --source whats-new --days 14

# Check CloudFormation resources for new services
python tools/monitor_aws_changes.py --source cloudformation --compare

# Generate custom report
python tools/monitor_aws_changes.py --source all --output my_report.json

# Quiet mode (no console output)
python tools/monitor_aws_changes.py --source whats-new --quiet --output changes.json
```

### Interpreting Monitoring Results

**Priority Levels:**
- **High**: Security changes, new core services, deprecations
- **Medium**: Service enhancements, new features, integrations
- **Low**: UI changes, documentation updates, pricing

**Example Output:**
```
📊 Change Summary (15 total)
HIGH Priority (3 items):
  • New IAM Access Analyzer features for policy validation
    Services: iam
  • Amazon S3 introduces new security controls
    Services: s3

Affected Services:
  • iam: 3 changes
  • s3: 2 changes
  • ec2: 1 change
```

## ArangoDB Integration

### Prerequisites

```bash
# Install and start ArangoDB
# See: https://www.arangodb.com/download/

# macOS (using Homebrew)
brew install arangodb

# Ubuntu/Debian
curl -OL https://download.arangodb.com/arangodb310/DEBIAN/Release.key
sudo apt-key add - < Release.key
echo 'deb https://download.arangodb.com/arangodb310/DEBIAN/ /' | sudo tee /etc/apt/sources.list.d/arangodb.list
sudo apt-get update
sudo apt-get install arangodb3

# Docker
docker run -p 8529:8529 -e ARANGO_ROOT_PASSWORD=openSesame arangodb/arangodb:latest

# Start ArangoDB service
sudo systemctl start arangodb3  # Linux
# Or start manually: arangod

# Verify ArangoDB is running (default: localhost:8529)
curl http://localhost:8529/_api/version
```

### Installing ArangoRDF Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install ArangoDB Python driver
pip install python-arango

# ArangoRDF should already be installed from local clone
# If not available, install from source:
# git clone https://github.com/arangoml/arango-rdf.git ~/code/ArangoRDF
# pip install -e ~/code/ArangoRDF
```

### Importing AWS Ontology into ArangoDB

```bash
# Basic import (ontology + examples)
python tools/import_to_arangodb.py

# Import with custom settings
python tools/import_to_arangodb.py --host http://localhost:8529 --username root --password openSesame --database aws_ontology

# Import only ontology (no examples)
python tools/import_to_arangodb.py --no-examples

# Import without overwriting existing data
python tools/import_to_arangodb.py --no-overwrite

# Import and run test queries
python tools/import_to_arangodb.py --test-queries
```

### Querying the Imported Data

Once imported, you can query the ontology using AQL (ArangoDB Query Language):

```python
from arango import ArangoClient

# Connect to database
client = ArangoClient(hosts='http://localhost:8529')
db = client.db('aws_ontology', username='root', password='openSesame')

# Query all AWS service classes
aql = """
FOR doc IN statements
    FILTER doc.predicate == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    FILTER doc.object == "http://www.w3.org/2002/07/owl#Class"
    FILTER CONTAINS(doc.subject, "aws-ontology")
    RETURN doc.subject
"""

cursor = db.aql.execute(aql)
aws_classes = [doc for doc in cursor]
print(f"Found {len(aws_classes)} AWS classes")
```

### Advanced ArangoDB Usage

For comprehensive ArangoDB integration documentation, including:
- Graph traversal queries
- Performance optimization
- Custom collection mapping
- SPARQL-to-AQL conversion
- Troubleshooting

See: **[docs/ARANGODB_INTEGRATION.md](ARANGODB_INTEGRATION.md)**

## Development Workflow

### Making Ontology Updates

1. **Check Current State**
   ```bash
   make test-all
   make sync-check
   ```

2. **Make Changes**
   - Edit `ontology/aws.ttl` (recommended) or `ontology/aws.owl`
   - Update `ontology/examples.ttl` if needed

3. **Synchronize Formats**
   ```bash
   make sync-ttl-to-owl  # If you edited TTL
   make sync-owl-to-ttl  # If you edited OWL
   ```

4. **Test Changes**
   ```bash
   make test-all
   ```

5. **Update Documentation**
   - Update version in ontology files
   - Add entry to `CHANGELOG.md`
   - Update README if needed

6. **Commit and Push**
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   git push origin main
   ```

### Responding to AWS Changes

1. **Monitor Changes**
   ```bash
   make monitor-weekly
   ```

2. **Assess Impact**
   - Review high-priority changes
   - Determine if ontology updates needed

3. **Plan Updates**
   - Identify affected classes/properties
   - Plan example updates

4. **Implement Changes**
   - Follow development workflow above
   - Focus on changed services

5. **Document Changes**
   - Update CHANGELOG.md
   - Note AWS announcement references

## Troubleshooting

### Common Issues

**Test Failures:**
```bash
# If sync tests fail
make sync-check  # Check current status
make sync-ttl-to-owl  # Try resync

# If quality tests fail
# Review error messages for specific issues
# Common: missing labels, invalid domains/ranges

# If performance tests fail
# Check if ontology size has grown significantly
# Review query complexity
```

**Import Errors:**
```bash
# If Python modules not found
source venv/bin/activate  # Activate virtual environment
make install-deps  # Reinstall dependencies
```

**Git Hook Issues:**
```bash
# If pre-commit hook prevents commits
make sync-check  # Identify sync issues
make test-sync   # Run detailed sync tests

# Temporarily disable hooks (if needed)
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
```

**Monitoring Tool Issues:**
```bash
# If feedparser not found
pip install feedparser requests

# If no changes detected
python tools/monitor_aws_changes.py --source whats-new --days 30  # Longer timeframe
```

**ArangoDB Integration Issues:**
```bash
# If ArangoDB connection fails
# Check if ArangoDB is running
curl http://localhost:8529/_api/version

# If ArangoRDF import fails
# Ensure ArangoRDF is installed from local clone
pip install -e ~/code/ArangoRDF

# If authentication fails
# Check username/password (default: root/openSesame)
python tools/import_to_arangodb.py --username root --password YOUR_PASSWORD

# If import is slow
# Try importing without examples first
python tools/import_to_arangodb.py --no-examples
```

### Getting Help

1. **Check Documentation**
   - README.md for project overview
   - This guide for usage instructions
   - docs/MAINTENANCE_STRATEGY.md for maintenance processes

2. **Run Diagnostics**
   ```bash
   make help         # Show available commands
   make test-all     # Run comprehensive tests
   make sync-check   # Check synchronization
   ```

3. **Check Logs**
   - Test output shows specific failures
   - Monitoring reports show detected changes
   - Git commit messages for recent changes

## Advanced Usage

### Custom SPARQL Queries

```bash
# Load ontology in Python
python3 -c "
from rdflib import Graph
g = Graph()
g.parse('ontology/aws.ttl', format='turtle')
print(f'Loaded {len(g)} triples')
"

# Example SPARQL query
python3 -c "
from rdflib import Graph
g = Graph()
g.parse('ontology/aws.ttl', format='turtle')
result = g.query('''
PREFIX aws: <http://www.semanticweb.org/aws-ontology#>
SELECT ?class ?label WHERE {
    ?class a owl:Class ;
           rdfs:label ?label .
    FILTER(CONTAINS(LCASE(?label), \"iam\"))
}
''')
for row in result:
    print(f'{row.class}: {row.label}')
"
```

### Extending the Monitoring

```bash
# Create custom monitoring script
# See tools/monitor_aws_changes.py as template
# Add new sources or modify priority assessment
```

### Performance Optimization

```bash
# Monitor ontology growth
python3 -c "
from rdflib import Graph
g = Graph()
g.parse('ontology/aws.ttl', format='turtle')
print(f'Total triples: {len(g)}')
classes = len(list(g.subjects(RDF.type, OWL.Class)))
print(f'Classes: {classes}')
"

# Run performance tests regularly
make test-performance
```

## Best Practices

1. **Always use virtual environment** for Python dependencies
2. **Run tests before committing** to catch issues early
3. **Keep both OWL and TTL synchronized** using provided tools
4. **Monitor AWS changes regularly** to stay current
5. **Document all changes** in CHANGELOG.md
6. **Use semantic versioning** for ontology updates
7. **Test performance** when adding significant content
8. **Backup before major changes** using Git branches 