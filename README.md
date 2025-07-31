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
├── Makefile                  # Common tasks and commands
├── .githooks/
│   └── pre-commit           # Git pre-commit hook for sync checking
├── docs/
│   └── PRD.md               # Product Requirements Document
├── ontology/
│   ├── aws.owl              # Ontology in OWL/XML format
│   ├── aws.ttl              # Ontology in Turtle format
│   └── examples.ttl         # Example instances in Turtle format
├── tests/
│   └── test_format_sync.py  # Synchronization test suite
└── tools/
    ├── README.md            # Tools documentation
    ├── transform_ontology.py # ArangoRDF transformation script
    ├── sync_formats.py      # Format synchronization utility
    └── setup_git_hooks.py   # Git hooks installation script
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

## Testing and Quality Assurance

The project includes a comprehensive test suite to ensure ontology quality, consistency, and performance:

### Test Categories

#### 1. Format Synchronization Testing
Ensures OWL and TTL formats remain synchronized:

```bash
# Run synchronization tests
make test-sync

# Check synchronization status
make sync-check
```

**Tests include:**
- File existence and parseability
- Semantic equivalence between formats
- Version consistency
- Triple count matching
- Property count matching

#### 2. Ontology Quality Testing
Validates ontology structure, consistency, and completeness:

```bash
# Run quality tests
make test-quality
```

**Tests include:**
- **Metadata Validation**: Proper ontology metadata (labels, comments, version)
- **Class Consistency**: All classes have labels and comments
- **Property Consistency**: All properties have labels and comments
- **Domain/Range Validation**: Properties have appropriate domains and ranges
- **Class Hierarchy**: Proper subclass relationships
- **Inverse Properties**: Correct inverse property declarations
- **Required Classes**: All PRD-specified classes present
- **IAM Structure**: IAM-specific constraints and cardinalities
- **OWL DL Compliance**: Basic OWL DL compliance checks
- **Naming Conventions**: Consistent naming patterns
- **Data Property Ranges**: Appropriate XSD type ranges

#### 3. Example Instance Validation
Validates example instances against the ontology:

```bash
# Run example validation tests
make test-examples
```

**Tests include:**
- **Type Validation**: All instances have proper types
- **Property Usage**: Properties used in examples are defined in ontology
- **IAM Structure**: IAM examples follow proper patterns
- **Policy Documents**: Policy JSON structure validation
- **Regional Structure**: Account/region/AZ hierarchy validation
- **Data Property Values**: Appropriate value ranges and formats
- **Reference Integrity**: No broken references between instances
- **Consistent Labeling**: All instances have proper labels

#### 4. Performance Testing
Measures ontology performance against PRD success metrics:

```bash
# Run performance tests
make test-performance
```

**Tests include:**
- **Loading Performance**: TTL/OWL loading under 5 seconds
- **Memory Usage**: Peak memory usage under 500MB
- **Query Performance**: Simple queries under 1 second
- **Complex Queries**: Complex SPARQL queries under 2 seconds
- **Graph Metrics**: Triple counts and structural metrics
- **Reasoning Performance**: OWL RL reasoning performance (if available)

### Comprehensive Testing

```bash
# Run all tests
make test-all

# Run essential tests only
make test
```

### Git Pre-commit Hooks
Automated synchronization checking via Git hooks prevents committing out-of-sync files:

```bash
# Install Git hooks (one-time setup)
make setup-hooks

# The pre-commit hook will automatically:
# - Check that both OWL and TTL files are staged together
# - Verify semantic equivalence when rdflib is available
# - Block commits if files are out of sync
```

**Hook Features:**
- **Smart Detection**: Only runs when ontology files are being committed
- **Both-File Enforcement**: Requires both OWL and TTL to be staged together
- **Semantic Validation**: Checks actual content equivalence (when rdflib available)
- **Graceful Degradation**: Falls back to basic checks if dependencies unavailable
- **Clear Error Messages**: Provides specific guidance on how to fix issues

### Test Dependencies

The test suite requires Python dependencies:

```bash
# Install test dependencies
make install-deps

# Or manually in virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Required packages:**
- `rdflib>=6.0.0` - Core RDF processing
- `owlready2>=0.45` - OWL ontology handling (optional)
- `owlrl` - OWL RL reasoning (optional, for performance tests)

### Continuous Integration

The test suite is designed for CI/CD integration:
- All tests return appropriate exit codes
- Verbose output for debugging
- Graceful handling of missing dependencies
- Performance metrics reporting

### Quality Metrics

Tests validate against PRD success metrics:
- **Loading Time**: < 5 seconds
- **Memory Usage**: < 500MB peak
- **Query Performance**: < 1-2 seconds
- **Completeness**: All required classes and properties
- **Consistency**: No logical contradictions
- **Usability**: Proper documentation and examples

### Synchronization Tools
Use the included tools to maintain format synchronization:

```bash
# Convert TTL to OWL
make sync-ttl-to-owl

# Convert OWL to TTL
make sync-owl-to-ttl

# Manual synchronization check
python tools/sync_formats.py check
```

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
- Python 3.7+ for transformation tools and testing
- ArangoDB for graph database transformation (optional)
- A SPARQL query engine for semantic queries
- Basic understanding of AWS services

### Using the Ontology
1. Clone the repository
2. Open either `aws.owl` or `aws.ttl` in your ontology editor
3. Review `examples.ttl` for usage patterns
4. Use SPARQL queries to analyze configurations

### Setting Up Development Environment
1. Install dependencies:
   ```bash
   # For macOS with Homebrew-managed Python
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Or use the Makefile (requires virtual environment)
   make install-deps
   ```

2. Set up Git hooks for automatic synchronization checking:
   ```bash
   make setup-hooks
   ```

3. Run tests to verify setup:
   ```bash
   make test
   ```

### Using ArangoDB Transformation
1. Install and start ArangoDB
2. Run transformation: `make transform`

## Development

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Submit a pull request

### Maintaining Formats
When making changes:
1. Update both `.owl` and `.ttl` formats
2. Ensure formats remain synchronized using `make test-sync`
3. Update examples if necessary
4. Document significant changes

**Important**: The pre-commit hook will automatically check synchronization and prevent commits if files are out of sync.

### Quality Assurance
- **Automated**: Pre-commit hooks check synchronization automatically
- **Manual**: Run synchronization tests before committing: `make test-sync`
- **Recovery**: Use format conversion tools when needed: `make sync-ttl-to-owl` or `make sync-owl-to-ttl`
- **Validation**: Validate OWL compliance with standard reasoners

### Working with Git Hooks
- **Install**: `make setup-hooks` (one-time setup per clone)
- **Test**: Try committing only one ontology file to see the hook in action
- **Disable temporarily**: Rename `.git/hooks/pre-commit` to `.git/hooks/pre-commit.disabled`
- **Remove**: `rm .git/hooks/pre-commit`

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