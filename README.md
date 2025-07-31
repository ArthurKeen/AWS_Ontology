# AWS Ontology

This project develops an OWL (Web Ontology Language) ontology for AWS (Amazon Web Services) objects and their relationships. The ontology aims to provide a formal, machine-readable representation of AWS services, resources, and their interconnections, with a particular focus on Identity and Access Management (IAM) configurations.

## Project Overview

The AWS Ontology project creates a comprehensive semantic model of AWS infrastructure and services. This ontology can be used for:
- Knowledge representation of AWS resources and relationships
- Automated reasoning about AWS architectures
- Semantic querying of AWS configurations
- Security analysis and compliance validation
- Graph database transformation and analysis
- Documentation and learning resources

## Repository Structure

```
.
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies for tools
├── docs/
│   └── PRD.md               # Product Requirements Document
├── ontology/
│   ├── aws.owl              # Ontology in OWL/XML format
│   ├── aws.ttl              # Ontology in Turtle format
│   └── examples.ttl         # Example instances in Turtle format
└── tools/
    ├── README.md            # Tools documentation
    └── transform_ontology.py # ArangoRDF transformation script
```

## Ontology Components

### Core Classes
- Infrastructure (Account, Region, AZ)
- Compute Resources (EC2, Lambda)
- Storage Resources (S3, EBS)
- Networking Resources (VPC, Subnet)
- Identity Resources (Users, Roles, Policies)
- Database Resources (RDS, DynamoDB)
- Monitoring Resources (CloudWatch, CloudTrail)

### IAM-Specific Components
- Policy Types
  - Managed Policies (AWS and Customer)
  - Inline Policies
  - Permission Boundaries
  - Trust Policies
  - Service Control Policies
- Policy Elements
  - Statements
  - Effects
  - Actions
  - Resources
  - Conditions

### Relationships
- Structural (contains, attachedTo)
- Access Control (hasPolicyAttachment, memberOf)
- Trust (hasTrustRelationship)
- Infrastructure (belongsToVPC, hasRegion)

## File Formats

The ontology is maintained in two formats:
1. **OWL/XML** (`aws.owl`): Standard format for OWL tools
2. **Turtle** (`aws.ttl`): Human-readable format for easier editing

Both formats are kept in sync and contain identical information. Choose the format that best suits your tools and needs.

## Example Data

The `examples.ttl` file provides comprehensive examples of:
- AWS account structures
- IAM configurations
- Policy definitions
- Resource relationships
- Infrastructure setups

These examples demonstrate how to:
- Model real AWS configurations
- Represent complex relationships
- Define policy documents
- Structure security configurations

## ArangoDB Integration

The project includes tools for transforming the ontology into ArangoDB graph schemas using the ArangoRDF library. Three transformation patterns are supported:

- **RPT (Resource Pattern Transformation)**: Simple graph structure
- **PGT (Property Graph Transformation)**: Balanced RDF and property graph features
- **LPGT (Labeled Property Graph Transformation)**: Full RDF semantics preservation

See `tools/README.md` for detailed usage instructions.

## Getting Started

### Prerequisites
- An OWL ontology editor (e.g., Protégé) for ontology viewing/editing
- Python 3.7+ for transformation tools
- ArangoDB for graph database transformation (optional)
- A SPARQL query engine for semantic queries
- Basic understanding of AWS services

### Using the Ontology
1. Clone the repository
2. Open either `aws.owl` or `aws.ttl` in your ontology editor
3. Review `examples.ttl` for usage patterns
4. Use SPARQL queries to analyze configurations

### Using ArangoDB Transformation
1. Install dependencies: `pip install -r requirements.txt`
2. Install and start ArangoDB
3. Run transformation: `python tools/transform_ontology.py`

## Development

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Maintaining Formats
When making changes:
1. Update both `.owl` and `.ttl` formats
2. Ensure formats remain synchronized
3. Update examples if necessary
4. Document significant changes

## Future Development

Planned enhancements include:
- Additional AWS service coverage
- More example configurations
- AQL query templates for ArangoDB
- SPARQL query templates
- Validation rules and constraints
- Advanced security analysis patterns

## Contact

Project maintained by Arthur Keen
GitHub: [@ArthurKeen](https://github.com/ArthurKeen)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 