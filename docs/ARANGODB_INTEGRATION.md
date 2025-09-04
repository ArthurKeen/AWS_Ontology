# ArangoDB Integration Guide

This guide explains how to import the AWS Ontology into ArangoDB using ArangoRDF, enabling graph database operations and advanced querying capabilities.

## Overview

ArangoRDF is a Python library that bridges RDF data and ArangoDB's multi-model database. It allows you to:
- Import RDF ontologies into ArangoDB as graph collections
- Query RDF data using AQL (ArangoDB Query Language)
- Leverage ArangoDB's graph algorithms and analytics
- Combine ontology data with other data models (documents, key-value)

## Prerequisites

### 1. ArangoDB Installation

Install ArangoDB on your system:

```bash
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
```

### 2. Start ArangoDB Service

```bash
# macOS/Linux service
sudo systemctl start arangodb3

# Or start manually
arangod

# Docker (if using container)
# ArangoDB will start automatically in the container
```

Access the ArangoDB web interface at `http://localhost:8529`

### 3. Python Dependencies

Ensure you have the required dependencies installed:

```bash
# Activate your virtual environment
source venv/bin/activate

# Install core dependencies (should already be installed)
pip install rdflib owlready2

# Install ArangoRDF from local clone (as per project setup)
# Note: ArangoRDF is installed from ~/code/ArangoRDF due to PyPI unavailability
```

## Basic Import Process

### 1. Create Import Script

Create a script to import the AWS ontology:

```python
#!/usr/bin/env python3
"""
Import AWS Ontology into ArangoDB using ArangoRDF.
"""

import sys
from pathlib import Path
from arango import ArangoClient
from arango_rdf import ArangoRDF
from rdflib import Graph

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.common import get_ontology_files, load_ontology_graph, TTL_FORMAT

def import_aws_ontology():
    """Import AWS ontology into ArangoDB."""
    
    # 1. Load the ontology
    ttl_file, owl_file, examples_file = get_ontology_files()
    
    print("📊 Loading AWS ontology...")
    ontology_graph = load_ontology_graph(ttl_file, TTL_FORMAT)
    if ontology_graph is None:
        print("❌ Failed to load ontology")
        return False
    
    examples_graph = load_ontology_graph(examples_file, TTL_FORMAT)
    if examples_graph is None:
        print("❌ Failed to load examples")
        return False
    
    # Combine ontology and examples
    combined_graph = Graph()
    combined_graph += ontology_graph
    combined_graph += examples_graph
    
    print(f"✅ Loaded {len(combined_graph)} triples")
    
    # 2. Connect to ArangoDB
    print("🔌 Connecting to ArangoDB...")
    client = ArangoClient(hosts='http://localhost:8529')
    
    # Create or connect to database
    db_name = 'aws_ontology'
    try:
        # Try to create database (will fail if exists)
        sys_db = client.db('_system', username='root', password='openSesame')
        db = sys_db.create_database(db_name)
        print(f"✅ Created database: {db_name}")
    except:
        # Database exists, connect to it
        db = client.db(db_name, username='root', password='openSesame')
        print(f"✅ Connected to existing database: {db_name}")
    
    # 3. Initialize ArangoRDF
    print("🔧 Initializing ArangoRDF...")
    arango_rdf = ArangoRDF(db)
    
    # 4. Import RDF data
    print("📥 Importing RDF data into ArangoDB...")
    try:
        # Import the combined graph
        arango_rdf.insert_rdf(combined_graph, overwrite=True)
        print("✅ Successfully imported AWS ontology into ArangoDB")
        
        # Print statistics
        collections = db.collections()
        for collection in collections:
            if not collection['name'].startswith('_'):
                count = db.collection(collection['name']).count()
                print(f"  📁 {collection['name']}: {count} documents")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to import RDF data: {e}")
        return False

if __name__ == "__main__":
    success = import_aws_ontology()
    sys.exit(0 if success else 1)
```

### 2. Run the Import

```bash
# Make sure ArangoDB is running
python tools/import_to_arangodb.py
```

## Querying the Imported Data

### 1. Basic AQL Queries

Once imported, you can query the ontology using AQL:

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

### 2. Graph Traversal Queries

```python
# Find all resources in a specific VPC
aql = """
FOR vpc IN statements
    FILTER vpc.predicate == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    FILTER vpc.object == "http://www.semanticweb.org/aws-ontology#VPC"
    
    FOR resource IN 1..3 INBOUND vpc.subject statements
        FILTER resource.predicate == "http://www.semanticweb.org/aws-ontology#belongsToVPC"
        RETURN {
            vpc: vpc.subject,
            resource: resource.subject,
            type: resource.object
        }
"""

cursor = db.aql.execute(aql)
vpc_resources = [doc for doc in cursor]
```

### 3. SPARQL-like Queries

```python
# Find EC2 instances and their properties
aql = """
FOR instance IN statements
    FILTER instance.predicate == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    FILTER instance.object == "http://www.semanticweb.org/aws-ontology#EC2Instance"
    
    LET properties = (
        FOR prop IN statements
            FILTER prop.subject == instance.subject
            FILTER prop.predicate != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
            RETURN {
                property: prop.predicate,
                value: prop.object
            }
    )
    
    RETURN {
        instance: instance.subject,
        properties: properties
    }
"""
```

## Advanced Usage

### 1. Custom Graph Collections

You can organize the ontology into specific collections:

```python
# Create separate collections for different AWS services
arango_rdf.insert_rdf(
    ontology_graph, 
    overwrite=True,
    collection_mapping={
        "http://www.semanticweb.org/aws-ontology#EC2Instance": "ec2_instances",
        "http://www.semanticweb.org/aws-ontology#S3Bucket": "s3_buckets",
        "http://www.semanticweb.org/aws-ontology#VPC": "vpcs"
    }
)
```

### 2. Incremental Updates

```python
# Update only specific parts of the ontology
new_triples = Graph()
# ... add new triples ...

arango_rdf.insert_rdf(new_triples, overwrite=False)
```

### 3. Graph Analytics

Leverage ArangoDB's graph algorithms:

```python
# Create a named graph for analysis
graph_name = "aws_infrastructure"
db.create_graph(
    graph_name,
    edge_definitions=[
        {
            'edge_collection': 'statements',
            'from_vertex_collections': ['subjects'],
            'to_vertex_collections': ['objects']
        }
    ]
)

# Run graph algorithms
result = db.graph(graph_name).traverse(
    start_vertex='subjects/vpc-12345',
    direction='outbound',
    max_depth=3
)
```

## Performance Optimization

### 1. Indexing

Create indexes for better query performance:

```python
# Create indexes on frequently queried fields
db.collection('statements').add_index({
    'type': 'persistent',
    'fields': ['predicate', 'object']
})

db.collection('statements').add_index({
    'type': 'persistent', 
    'fields': ['subject']
})
```

### 2. Batch Operations

For large ontologies, use batch operations:

```python
# Process in batches
batch_size = 1000
triples = list(combined_graph)

for i in range(0, len(triples), batch_size):
    batch = Graph()
    for triple in triples[i:i+batch_size]:
        batch.add(triple)
    arango_rdf.insert_rdf(batch, overwrite=False)
    print(f"Processed batch {i//batch_size + 1}")
```

## Troubleshooting

### Common Issues

1. **Connection Failed**: Ensure ArangoDB is running and accessible
2. **Authentication Error**: Check username/password (default: root/openSesame)
3. **Memory Issues**: Use batch processing for large ontologies
4. **Import Errors**: Verify RDF syntax and ArangoRDF compatibility

### Debugging

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# ArangoRDF will now provide detailed logs
arango_rdf.insert_rdf(graph, overwrite=True)
```

## Integration with Existing Tools

### 1. Monitoring Integration

Combine with the AWS change monitoring:

```python
# In tools/monitor_aws_changes.py
def update_arangodb_ontology(changes):
    """Update ArangoDB when ontology changes."""
    # Import new changes to ArangoDB
    # ... implementation ...
```

### 2. SPARQL Bridge

Create a SPARQL-to-AQL bridge for familiar querying:

```python
def sparql_to_aql(sparql_query):
    """Convert SPARQL queries to AQL (simplified)."""
    # Basic conversion logic
    # ... implementation ...
```

## Next Steps

1. **Explore ArangoDB Features**: Graph algorithms, full-text search, geospatial queries
2. **Build Applications**: Use ArangoDB drivers for your preferred language
3. **Scale**: Consider ArangoDB cluster setup for production use
4. **Monitor**: Set up monitoring and backup strategies

For more information, see:
- [ArangoDB Documentation](https://www.arangodb.com/docs/)
- [ArangoRDF GitHub Repository](https://github.com/arangoml/arango-rdf)
- [AQL Tutorial](https://www.arangodb.com/docs/stable/aql/)
