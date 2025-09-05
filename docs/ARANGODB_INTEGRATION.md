# ArangoDB Integration Guide

This guide explains how to import the AWS Ontology into ArangoDB using ArangoRDF, enabling graph database operations and advanced querying capabilities.

## Overview

ArangoRDF is a Python library that bridges RDF data and ArangoDB's multi-model database. It allows you to:
- Import RDF ontologies into ArangoDB as graph collections
- Query RDF data using AQL (ArangoDB Query Language)
- Leverage ArangoDB's graph algorithms and analytics
- Combine ontology data with other data models (documents, key-value)

### Why Use ArangoDB Integration?

The ArangoDB integration provides significant advantages for working with the AWS Ontology:

**Flexible Physical Schema Options**: ArangoRDF can generate different physical schemas in ArangoDB to match your specific use case:
- **Labeled Property Graphs (LPG)**: Industry-standard graph format compatible with most graph databases
- **ArangoDB-native Property Graphs (PG)**: Optimized for ArangoDB's native graph capabilities and performance
- **RDF Graph Physical Schemas**: Maintains semantic web standards while leveraging ArangoDB's multi-model features

**Accelerated Project Development**: This flexibility gives you a "leg up" when starting projects involving AWS graph use cases such as:
- Infrastructure dependency mapping and impact analysis
- Security policy validation and compliance checking
- Cost optimization through resource relationship analysis
- Multi-account governance and resource discovery
- Automated architecture documentation and visualization

By providing multiple schema options, you can choose the most appropriate representation for your specific AWS infrastructure analysis needs without being locked into a single graph model.

## Getting Started

## Prerequisites

### 1. ArangoDB Installation

**Note**: ArangoDB no longer provides native packages for macOS and Windows. The recommended installation method is Docker.

For comprehensive installation instructions and additional deployment options, including Kubernetes and Linux installations, see the [official ArangoDB Installation Guide](https://docs.arangodb.com/3.12/operations/installation/).

#### Option 1: Docker Community Edition

```bash
# Run ArangoDB Community Edition with Docker
docker run -d \
  --name arangodb \
  -p 8529:8529 \
  -e ARANGO_ROOT_PASSWORD=${ARANGO_PASSWORD:-openSesame} \
  arangodb/arangodb:latest

# Verify ArangoDB is running
docker logs arangodb
```

#### Option 2: ArangoDB Enterprise Edition

For enterprise features, you can use the Enterprise Edition:

```bash
# Enterprise Edition (requires license)
docker run -d \
  --name arangodb-ee \
  -p 8529:8529 \
  -e ARANGO_ROOT_PASSWORD=${ARANGO_PASSWORD:-openSesame} \
  -e ARANGO_LICENSE_KEY=your-license-key \
  arangodb/enterprise:latest
```

**Note**: Enterprise Edition requires a valid license from ArangoDB. Contact [ArangoDB](https://www.arangodb.com/enterprise/) for licensing information.

#### Option 3: ArangoGraph (Managed Service)

For production use or if you prefer a managed service:

1. Visit [cloud.arangodb.com](https://cloud.arangodb.com) to access ArangoGraph
2. Create an account and set up a deployment
3. **Free Trial Available**: ArangoGraph offers a free trial to get started
4. Use the provided connection details in your import script
5. Benefits: Automatic backups, scaling, monitoring, and maintenance

```bash
# Example with ArangoGraph
python tools/import_to_arangodb.py \
  --host https://your-deployment.arangodb.cloud:8529 \
  --username your-username \
  --password your-password
```

### 2. Access ArangoDB

```bash
# Check if Docker container is running
docker ps | grep arangodb

# Start container if stopped
docker start arangodb

# Stop container when done
docker stop arangodb

# Remove container (data will be lost unless using volumes)
docker rm arangodb
```

**Web Interface**: Access ArangoDB at `http://localhost:8529`
- **Username**: `root`
- **Password**: Set via `ARANGO_PASSWORD` environment variable (default: `openSesame`)

#### Persistent Data Storage

To persist data across container restarts:

```bash
# Create a volume for data persistence
docker volume create arangodb_data

# Run with persistent storage
docker run -d \
  --name arangodb \
  -p 8529:8529 \
  -e ARANGO_ROOT_PASSWORD=${ARANGO_PASSWORD:-openSesame} \
  -v arangodb_data:/var/lib/arangodb3 \
  arangodb/arangodb:latest
```

### 3. Python Dependencies

Ensure you have the required dependencies installed:

```bash
# Activate your virtual environment
source venv/bin/activate

# Install core dependencies (should already be installed)
pip install rdflib owlready2

# Install ArangoRDF from PyPI
pip install arango-rdf
```

## Basic Import Process

### 1. Create Import Script

The following script imports the AWS ontology using the **RDF Graph Schema** (default). This creates a triple-based structure in ArangoDB where each RDF statement becomes a document in the `statements` collection.

For other graph types (LPG or PG), see the configuration examples at the end of this section.

```python
#!/usr/bin/env python3
"""
Import AWS Ontology into ArangoDB using ArangoRDF.
"""

import sys
import os
from pathlib import Path
from arango import ArangoClient
from arango_rdf import ArangoRDF
from rdflib import Graph

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
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
        sys_db = client.db('_system', username='root', password=os.getenv('ARANGO_PASSWORD', 'openSesame'))
        db = sys_db.create_database(db_name)
        print(f"✅ Created database: {db_name}")
    except:
        # Database exists, connect to it
        db = client.db(db_name, username='root', password=os.getenv('ARANGO_PASSWORD', 'openSesame'))
        print(f"✅ Connected to existing database: {db_name}")
    
    # 3. Initialize ArangoRDF
    print("🔧 Initializing ArangoRDF...")
    arango_rdf = ArangoRDF(db)
    
    # 4. Import RDF data (creates RDF Graph Schema by default)
    print("📥 Importing RDF data into ArangoDB as RDF Graph Schema...")
    try:
        # Import the combined graph - creates triple-based structure
        arango_rdf.insert_rdf(combined_graph, overwrite=True)
        print("✅ Successfully imported AWS ontology as RDF Graph Schema")
        print("   📋 Structure: Triple-based with statements collection")
        
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

def import_as_lpg():
    """Import AWS ontology as Labeled Property Graph (LPG)."""
    ttl_file, owl_file, examples_file = get_ontology_files()
    
    # Load and combine graphs
    ontology_graph = load_ontology_graph(ttl_file, TTL_FORMAT)
    examples_graph = load_ontology_graph(examples_file, TTL_FORMAT)
    combined_graph = Graph()
    combined_graph += ontology_graph
    combined_graph += examples_graph
    
    # Connect to ArangoDB
    client = ArangoClient(hosts='http://localhost:8529')
    db = client.db('aws_ontology_lpg', username='root', password=os.getenv('ARANGO_PASSWORD', 'openSesame'))
    arango_rdf = ArangoRDF(db)
    
    # Import as LPG
    arango_rdf.insert_rdf(
        combined_graph, 
        overwrite=True,
        schema_type="lpg",
        vertex_collections=["vertices"],
        edge_collections=["edges"]
    )
    print("✅ Successfully imported AWS ontology as Labeled Property Graph")
    print("   📋 Structure: Vertices and edges collections")

def import_as_pg():
    """Import AWS ontology as ArangoDB Property Graph (PG)."""
    ttl_file, owl_file, examples_file = get_ontology_files()
    
    # Load and combine graphs
    ontology_graph = load_ontology_graph(ttl_file, TTL_FORMAT)
    examples_graph = load_ontology_graph(examples_file, TTL_FORMAT)
    combined_graph = Graph()
    combined_graph += ontology_graph
    combined_graph += examples_graph
    
    # Connect to ArangoDB
    client = ArangoClient(hosts='http://localhost:8529')
    db = client.db('aws_ontology_pg', username='root', password=os.getenv('ARANGO_PASSWORD', 'openSesame'))
    arango_rdf = ArangoRDF(db)
    
    # Import as native Property Graph
    arango_rdf.insert_rdf(
        combined_graph,
        overwrite=True,
        schema_type="pg",
        collection_mapping={
            "http://www.semanticweb.org/aws-ontology#EC2Instance": "ec2_instances",
            "http://www.semanticweb.org/aws-ontology#S3Bucket": "s3_buckets",
            "http://www.semanticweb.org/aws-ontology#VPC": "vpcs",
            "http://www.semanticweb.org/aws-ontology#RDSInstance": "rds_instances",
            "http://www.semanticweb.org/aws-ontology#belongsToVPC": "belongs_to_vpc",
            "http://www.semanticweb.org/aws-ontology#routesTo": "routes_to",
            "http://www.semanticweb.org/aws-ontology#connectsTo": "connects_to"
        }
    )
    print("✅ Successfully imported AWS ontology as ArangoDB Property Graph")
    print("   📋 Structure: Native collections (ec2_instances, vpcs, etc.)")

if __name__ == "__main__":
    import sys
    import os
    
    # Default: RDF Graph Schema
    if len(sys.argv) == 1 or sys.argv[1] == "rdf":
        success = import_aws_ontology()
    elif sys.argv[1] == "lpg":
        success = import_as_lpg()
    elif sys.argv[1] == "pg":
        success = import_as_pg()
    else:
        print("Usage: python import_script.py [rdf|lpg|pg]")
        print("  rdf: RDF Graph Schema (default) - triple-based structure")
        print("  lpg: Labeled Property Graph - vertices and edges")
        print("  pg:  ArangoDB Property Graph - native collections")
        sys.exit(1)
    
    sys.exit(0 if success else 1)
```

### 2. Run the Import

```bash
# Make sure ArangoDB is running

# Import as RDF Graph Schema (default - triple-based)
python tools/import_to_arangodb.py
# or explicitly:
python tools/import_to_arangodb.py rdf

# Import as Labeled Property Graph (LPG)
python tools/import_to_arangodb.py lpg

# Import as ArangoDB Property Graph (PG)
python tools/import_to_arangodb.py pg
```

**Graph Type Comparison:**
- **RDF**: Creates `statements` collection with subject-predicate-object triples
- **LPG**: Creates `vertices` and `edges` collections with labeled relationships
- **PG**: Creates native collections like `ec2_instances`, `vpcs`, `belongs_to_vpc` edges

## Querying the Imported Data

ArangoRDF supports multiple physical graph representations. The query approach depends on which schema type you choose during import:

- **RDF Graph Schema**: Maintains triple-based structure (subject-predicate-object)
- **Labeled Property Graph (LPG)**: Industry-standard property graph format
- **ArangoDB Property Graph (PG)**: Native ArangoDB graph structure

### RDF Graph Queries

The following examples demonstrate querying RDF-structured data (the default ArangoRDF import format):

```python
from arango import ArangoClient

# Connect to database
client = ArangoClient(hosts='http://localhost:8529')
db = client.db('aws_ontology', username='root', password=os.getenv('ARANGO_PASSWORD', 'openSesame'))

# Query all AWS service classes (RDF format)
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

#### RDF Graph Traversal

```python
# Find all resources in a specific VPC (RDF format)
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

#### RDF Property Queries

```python
# Find EC2 instances and their properties (RDF format)
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

### Labeled Property Graph (LPG) Queries

When using LPG format, AWS resources become vertices with properties, and relationships become labeled edges:

```python
# Import with LPG schema (requires ArangoRDF configuration)
# arango_rdf.insert_rdf(graph, schema_type="lpg")

# Query EC2 instances in LPG format
aql = """
FOR instance IN vertices
    FILTER instance.type == "EC2Instance"
    RETURN {
        id: instance._key,
        instanceType: instance.instanceType,
        state: instance.state,
        availabilityZone: instance.availabilityZone
    }
"""

# Find VPC and its connected resources using edge traversal
aql = """
FOR vpc IN vertices
    FILTER vpc.type == "VPC"
    FILTER vpc.vpcId == "vpc-12345"
    
    FOR vertex, edge IN 1..2 OUTBOUND vpc edges
        RETURN {
            vpc: vpc.vpcId,
            resource: vertex._key,
            resourceType: vertex.type,
            relationship: edge.label
        }
"""
```

### ArangoDB Property Graph (PG) Queries

Native ArangoDB property graphs optimize for performance and leverage ArangoDB's graph capabilities:

```python
# Import with native PG schema
# arango_rdf.insert_rdf(graph, schema_type="pg")

# Query using native graph collections
aql = """
FOR instance IN ec2_instances
    FILTER instance.state == "running"
    
    FOR vpc IN 1..1 OUTBOUND instance belongs_to_vpc
        RETURN {
            instance: instance.instanceId,
            vpc: vpc.vpcId,
            subnet: instance.subnetId
        }
"""

# Complex traversal with multiple edge types
aql = """
FOR loadbalancer IN load_balancers
    FILTER loadbalancer.scheme == "internet-facing"
    
    FOR target IN 2..3 OUTBOUND loadbalancer 
        routes_to, targets
        FILTER target.type == "EC2Instance"
        
        RETURN {
            loadBalancer: loadbalancer.name,
            targetInstance: target.instanceId,
            path: CONCAT_SEPARATOR(" -> ", 
                loadbalancer.name, 
                target.instanceId
            )
        }
"""

# Aggregate queries for infrastructure analysis
aql = """
FOR vpc IN vpcs
    LET instanceCount = LENGTH(
        FOR instance IN 1..2 OUTBOUND vpc contains, runs_in
            FILTER instance.type == "EC2Instance"
            RETURN instance
    )
    
    LET totalCost = SUM(
        FOR resource IN 1..3 OUTBOUND vpc contains, runs_in, uses
            RETURN resource.monthlyCost || 0
    )
    
    RETURN {
        vpc: vpc.vpcId,
        instanceCount: instanceCount,
        estimatedMonthlyCost: totalCost
    }
"""
```

### Choosing the Right Schema Type

**RDF Graph Schema** - Best for:
- Semantic web applications
- SPARQL-like queries
- Maintaining ontology semantics
- Research and analysis requiring RDF standards

**Labeled Property Graph (LPG)** - Best for:
- Cross-platform compatibility
- Integration with other graph databases
- Standard graph algorithms
- Familiar property graph patterns

**ArangoDB Property Graph (PG)** - Best for:
- Maximum performance
- Native ArangoDB features
- Complex multi-model queries
- Production applications requiring speed

## Advanced Usage

### 1. Schema-Specific Import Options

Configure ArangoRDF for different schema types:

```python
# RDF Graph Schema (default)
arango_rdf.insert_rdf(
    combined_graph,
    overwrite=True,
    # Uses statements collection for triples
)

# Labeled Property Graph (LPG)
arango_rdf.insert_rdf(
    combined_graph,
    overwrite=True,
    schema_type="lpg",
    vertex_collections=["vertices"],
    edge_collections=["edges"]
)

# ArangoDB Property Graph (PG)
arango_rdf.insert_rdf(
    combined_graph,
    overwrite=True,
    schema_type="pg",
    collection_mapping={
        "http://www.semanticweb.org/aws-ontology#EC2Instance": "ec2_instances",
        "http://www.semanticweb.org/aws-ontology#S3Bucket": "s3_buckets",
        "http://www.semanticweb.org/aws-ontology#VPC": "vpcs",
        "http://www.semanticweb.org/aws-ontology#belongsToVPC": "belongs_to_vpc",
        "http://www.semanticweb.org/aws-ontology#routesTo": "routes_to"
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
2. **Authentication Error**: Check username/password (set ARANGO_PASSWORD environment variable)
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
