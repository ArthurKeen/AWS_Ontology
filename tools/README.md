# AWS Ontology Tools

This directory contains tools for working with the AWS Ontology.

## Ontology Transformation Tool

The `transform_ontology.py` script transforms the AWS ontology into ArangoDB graph schemas using different transformation patterns from the ArangoRDF library.

### Transformation Patterns

1. **RPT (Resource Pattern Transformation)**
   - Creates a simple graph where each RDF resource becomes a vertex
   - Preserves basic structure but loses some RDF semantics
   - Best for simple querying and visualization

2. **PGT (Property Graph Transformation)**
   - Creates a property graph with RDF properties as edge attributes
   - Balances RDF semantics with property graph features
   - Good for general-purpose graph analysis

3. **LPGT (Labeled Property Graph Transformation)**
   - Creates a labeled property graph preserving RDF semantics
   - Maintains most RDF features while utilizing graph database capabilities
   - Best for advanced querying that requires RDF semantics

### Prerequisites

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Install and start ArangoDB:
   ```bash
   # Example for macOS using Homebrew
   brew install arangodb
   brew services start arangodb
   ```

### Usage

Basic usage with default settings:
```bash
python tools/transform_ontology.py
```

Specify transformation patterns:
```bash
python tools/transform_ontology.py --patterns rpt lpgt
```

Custom database connection:
```bash
python tools/transform_ontology.py --host localhost --port 8529 --username root --password mypassword --database my_aws_db
```

Custom file paths:
```bash
python tools/transform_ontology.py --owl path/to/ontology.owl --ttl path/to/examples.ttl
```

### Arguments

- `--host`: ArangoDB host (default: localhost)
- `--port`: ArangoDB port (default: 8529)
- `--username`: ArangoDB username (default: root)
- `--password`: ArangoDB password (default: empty)
- `--database`: Database name (default: aws_ontology)
- `--owl`: Path to OWL file (default: ontology/aws.owl)
- `--ttl`: Path to TTL examples file (default: ontology/examples.ttl)
- `--patterns`: Transformation patterns to apply (choices: rpt, pgt, lpgt) 