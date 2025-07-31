# AWS Ontology

A comprehensive semantic ontology for Amazon Web Services (AWS) resources and their relationships. This project provides a formal OWL ontology that models AWS infrastructure, services, and their complex interdependencies for advanced analysis, compliance monitoring, and automation.

## 🎯 Overview

The AWS Ontology is a production-ready semantic web resource that:

- **Models 70+ AWS resource types** across compute, storage, networking, containers, API services, and integration
- **Defines 150+ relationships** including temporal, cost, and compliance associations
- **Provides comprehensive examples** with real-world AWS configurations
- **Supports multiple formats** (OWL/XML, Turtle, with format synchronization)
- **Includes semantic constraints** (cardinality, disjoint classes, property characteristics)
- **Offers testing framework** for quality assurance and validation

## 📊 Current Metrics

| Metric | Count | Growth |
|--------|-------|--------|
| **Total Triples** | 1,095 | +84% |
| **Classes** | 71 | +103% |
| **Object Properties** | 93 | +107% |
| **Data Properties** | 62 | +148% |
| **Example Instances** | 390+ | New |

## 🏗️ Ontology Structure

### Core Service Categories
- **🔧 Container Services**: ECS, EKS, Fargate, ECR
- **🔗 API & Integration**: API Gateway, Step Functions, EventBridge, SNS, SQS
- **💻 Compute**: EC2, Lambda, Auto Scaling
- **💾 Storage**: S3, EBS, RDS
- **🌐 Networking**: VPC, Security Groups, Load Balancers
- **🔐 Identity & Access**: IAM Users, Roles, Policies
- **📊 Monitoring**: CloudWatch, CloudTrail

### Advanced Relationship Types
- **⏰ Temporal**: `createdBefore`, `replacedBy`, `migratedFrom`
- **💰 Cost**: `incursChargeFor`, `optimizedBy`, `allocatesCostTo`
- **🛡️ Compliance**: `compliesWith`, `auditedBy`, `controlledBy`

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- RDF processing tools (rdflib)
- Optional: Protégé for visual exploration

### Installation

```bash
# Clone the repository
git clone https://github.com/ArthurKeen/AWS_Ontology.git
cd AWS_Ontology

# Install dependencies
pip install -r requirements.txt

# Verify ontology integrity
python tools/sync_formats.py check

# Run quality tests
python -m unittest tests.test_ontology_quality -v
```

## 📁 Repository Structure

```
AWS_Ontology/
├── ontology/
│   ├── aws.owl           # Main ontology (OWL/XML format)
│   ├── aws.ttl           # Turtle format (human-readable)
│   └── examples.ttl      # Real-world example instances
├── docs/
│   ├── PRD.md           # Product Requirements Document
│   ├── PROTEGE_GUIDE.md # Protégé exploration guide
│   ├── SPARQL_EXAMPLES.md # 22 ready-to-use SPARQL queries
│   └── USAGE_GUIDE.md   # Comprehensive usage documentation
├── tests/               # Comprehensive test suite
├── tools/               # Format synchronization utilities
└── automation/         # AWS change monitoring tools
```

## 🔍 Protégé Integration

Open the ontology in Protégé for visual exploration:

```bash
# Method 1: Direct open
open ontology/aws.owl

# Method 2: Manual open in Protégé
# File → Open → ontology/aws.owl
```

**Key Protégé Features:**
- **Class Hierarchy**: Browse 71 AWS resource classes
- **Object Properties**: Explore 93 relationship types
- **Reasoning**: Validate with HermiT reasoner
- **OntoGraf**: Visualize relationships graphically
- **SPARQL**: Test queries from our examples

See [`docs/PROTEGE_GUIDE.md`](docs/PROTEGE_GUIDE.md) for detailed exploration instructions.

## 🧪 SPARQL Querying

The ontology supports rich SPARQL queries for analysis:

```sparql
# Find all container services
PREFIX : <http://www.semanticweb.org/aws-ontology#>
SELECT ?service ?label WHERE {
  ?service rdfs:subClassOf* :ComputeResource .
  ?service rdfs:label ?label .
  FILTER(CONTAINS(?label, "ECS") || CONTAINS(?label, "EKS"))
}

# Find services that can trigger Step Functions
SELECT ?service ?stepFunction WHERE {
  ?service :triggersStepFunction ?stepFunction
}
```

See [`docs/SPARQL_EXAMPLES.md`](docs/SPARQL_EXAMPLES.md) for 22 ready-to-use queries.

## 🔧 Tools & Utilities

### Format Synchronization
```bash
# Check OWL ↔ TTL synchronization
python tools/sync_formats.py check

# Convert OWL to TTL
python tools/sync_formats.py owl-to-ttl

# Convert TTL to OWL
python tools/sync_formats.py ttl-to-owl
```

### Quality Assurance
```bash
# Run all quality tests
make test

# Test specific aspects
python -m unittest tests.test_ontology_quality -v
python -m unittest tests.test_examples_validation -v
python -m unittest tests.test_format_sync -v
```

### AWS Change Monitoring
```bash
# Monitor AWS service changes
python tools/monitor_aws_changes.py

# Schedule automated monitoring
make schedule-setup
```

## 🎯 Use Cases

### 1. Infrastructure Analysis
- Model complex AWS architectures
- Analyze service dependencies
- Identify optimization opportunities

### 2. Compliance Monitoring
- Track compliance status across resources
- Audit relationships and governance
- Monitor policy adherence

### 3. Cost Optimization
- Analyze cost allocation relationships
- Identify shared resources
- Model optimization scenarios

### 4. Security Analysis
- Map IAM relationships and permissions
- Analyze access patterns
- Identify security risks

### 5. Migration Planning
- Model current and target states
- Track migration relationships
- Plan temporal sequences

## 🧪 Testing Framework

Comprehensive testing ensures ontology quality:

- **Format Synchronization**: OWL ↔ TTL consistency
- **Ontology Quality**: Class/property validation
- **Example Validation**: Instance integrity
- **Performance**: Loading and query benchmarks

```bash
# Run all tests
make test

# Test categories
make test-sync     # Format synchronization
make test-quality  # Ontology structure
make test-examples # Example validation
make test-performance # Performance benchmarks
```

## 📈 Development Workflow

### Adding New Services
1. Define classes in `ontology/aws.owl`
2. Add relationships and properties
3. Create examples in `ontology/examples.ttl`
4. Sync formats: `python tools/sync_formats.py sync`
5. Run tests: `make test`
6. Update documentation

### Contributing
1. Fork the repository
2. Create feature branch
3. Add ontology enhancements
4. Include comprehensive tests
5. Update documentation
6. Submit pull request

## 🔗 Integration

### Graph Database Transformations
The ontology supports multiple graph database representations:
- **RDF Triplestores**: Direct loading as RDF/OWL with full semantic reasoning support
- **Labeled Property Graphs (LPG)**: Transform to property graph format with labeled nodes and edges for modern graph databases
- **Property Graphs (PG)**: Convert to property graph structures optimized for performance and graph analytics
- **Custom Transformations**: Flexible transformation patterns for domain-specific use cases and requirements

### Analysis Tools
- **Python**: rdflib, owlready2, networkx
- **Java**: Apache Jena, RDF4J, OWL API, JGraphT
- **JavaScript**: rdflib.js, cytoscape.js
- **R**: rdflib for R, igraph
- **SPARQL**: Standard RDF query language support

## 📚 Documentation

- **[PRD](docs/PRD.md)**: Product Requirements Document
- **[Protégé Guide](docs/PROTEGE_GUIDE.md)**: Visual exploration
- **[SPARQL Examples](docs/SPARQL_EXAMPLES.md)**: Query collection
- **[Usage Guide](docs/USAGE_GUIDE.md)**: Comprehensive usage
- **[Maintenance Strategy](docs/MAINTENANCE_STRATEGY.md)**: Update processes

## 🤝 Community

### Questions & Support
- Create GitHub issues for questions
- Check existing documentation first
- Provide minimal reproduction examples

### Feature Requests
- Submit detailed GitHub issues
- Explain use case and benefits
- Consider contributing implementation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

### Latest Enhancements (v0.3.0)
- ✅ Container Services (ECS, EKS, Fargate, ECR)
- ✅ API & Integration Services (API Gateway, Step Functions, EventBridge)
- ✅ Enhanced Relationships (temporal, cost, compliance)
- ✅ Semantic Axioms (cardinality constraints, disjoint classes)
- ✅ Protégé Integration & Documentation

---

**Note**: This is the core open-source AWS Ontology designed for flexible integration with various graph databases and analytics platforms through standard RDF/OWL interfaces and custom transformation patterns.