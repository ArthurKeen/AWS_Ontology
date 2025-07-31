# ArangoDB Transformation Tools

This directory contains tools for transforming the AWS Ontology into ArangoDB graph databases.

## Main Tool: `transform_ontology.py`

Converts the AWS Ontology into ArangoDB using three different transformation patterns.

### Basic Usage

```bash
# Transform using PGT pattern (recommended)
python tools/transform_ontology.py --pattern pgt --include-examples

# Transform using RPT pattern (simple)
python tools/transform_ontology.py --pattern rpt

# Transform using LPGT pattern (full semantics)
python tools/transform_ontology.py --pattern lpgt --include-examples
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--pattern` | Transformation pattern (rpt/pgt/lpgt) | *Required* |
| `--ontology-path` | Path to ontology file | `../AWS_Ontology/ontology/aws.ttl` |
| `--include-examples` | Include example instances | `False` |
| `--host` | ArangoDB host | `localhost` |
| `--port` | ArangoDB port | `8529` |
| `--username` | ArangoDB username | `root` |
| `--password` | ArangoDB password | *(empty)* |
| `--database` | Target database name | `aws_ontology` |
| `--export-schema` | Export schema to JSON file | *(none)* |
| `--verbose` | Enable verbose logging | `False` |

### Transformation Patterns

- **RPT**: Simple graph structure, fastest queries
- **PGT**: Balanced features and performance (recommended)
- **LPGT**: Full RDF semantics, complex reasoning

### Examples

```bash
# Custom database connection
python tools/transform_ontology.py \
    --pattern pgt \
    --host my-server \
    --database my_aws_db \
    --include-examples \
    --export-schema schemas/schema.json

# Verbose transformation
python tools/transform_ontology.py \
    --pattern lpgt \
    --verbose
```

## Requirements

- ArangoDB 3.8+ running
- Python dependencies: `pip install -r requirements.txt`
- AWS Ontology repository available at `../AWS_Ontology/`

For detailed documentation and troubleshooting, see the main README.md. 