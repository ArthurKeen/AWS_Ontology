# Changelog

All notable changes to the AWS Ontology project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Modern Python toolchain**: `pyproject.toml` (PEP 621) as the canonical dependency
  manifest with a `uv.lock` lockfile; ruff replaces black/isort/flake8/mypy; pytest runs
  the suite (`make test`, `make lint`, `make format`)
- **GitHub Actions CI**: lint + test matrix (Python 3.11/3.14) + TTL/OWL sync verification
  on every push and pull request
- **CLI smoke tests** (`tests/test_tools_smoke.py`): every tool must answer `--help` and
  byte-compile — guards against the argparse-crash class of bug
- **OWL 2 DL compliance tests** (`tests/test_dl_compliance.py`): undeclared-term references
  and illegal axiom constructs (e.g. inverse-functional datatype properties) now fail CI

### Removed
- Dead code: `utils/config_validation.py` (296 lines, never imported), `mypy.ini`,
  `.coveragerc` (coverage config folded into `pyproject.toml`)
- **PRD-required IAM properties** (closes drift alerts REQ-009/REQ-010): `canAssumeRole`
  (IAM principal → assumable role) and `hasPolicy` (declared `owl:equivalentProperty` to the
  existing `hasPolicyAttachment`)
- **PRD v1.2**: all testable requirements now carry stable `REQ-NNN` identifiers used by
  drift tooling; scope updated to reflect implemented service coverage, with 2023+ services
  listed as roadmap

### Fixed
- **Ontology axioms**: Declared previously-missing `belongsToRegion` object property
  (was referenced only by VPC's cardinality restriction)
- **OWL 2 DL compliance**: Removed illegal `owl:InverseFunctionalProperty` typing from the
  `arn` datatype property; ARN uniqueness is now expressed with a DL-legal `owl:hasKey`
  axiom on `AWSResource`
- **Version metadata**: `owl:versionInfo` synchronized with CHANGELOG (0.4.0 → 0.4.2)
- **Documentation accuracy**: Corrected example-instance count (115 typed individuals, not
  535+), fixed README quick-example to use the real `encrypted` property, refreshed stale
  class/property counts, and corrected CHANGELOG release dates to match git history
- **Tooling**: Fixed `--quiet` argparse crash in `tools/monitor_aws_changes.py`; removed
  hardcoded ArangoDB password fallback in `tools/import_to_arangodb.py`

### Changed
- **README.md**: Enhanced project introduction and value proposition
  - Added "Why Use the AWS Ontology?" section explaining project development benefits
  - Included Protégé visualization showing ontology class hierarchy and relationships
- **ArangoDB Documentation**: Comprehensive enhancement of integration guide
  - **Query Examples by Schema Type**: Added distinct query examples for RDF, LPG, and PG formats
  - **Import Script Clarity**: Enhanced import script to clearly specify graph schema types (RDF default, LPG, PG options)
  - **Schema Selection Guidance**: Added detailed comparison of when to use each graph type
  - **Multi-Format Support**: Complete examples for all three physical graph representations
  - Added detailed explanation of flexible physical schema options (LPG, PG, RDF)
  - Highlighted accelerated project development advantages for AWS graph use cases
  - Updated installation instructions to focus on Docker deployment
  - Added ArangoGraph free trial information
  - Included reference to official ArangoDB installation guide with Kubernetes and Linux coverage

## [0.4.2] - 2025-09-04

### Added
- **ArangoDB Integration**: Complete graph database integration using ArangoRDF
  - New comprehensive integration guide: `docs/ARANGODB_INTEGRATION.md`
  - Production-ready import tool: `tools/import_to_arangodb.py`
  - AQL query examples and performance optimization guidance
  - Troubleshooting documentation for common integration issues
- **Code Quality Improvements**: Comprehensive refactoring to eliminate code duplication
  - New shared utilities module: `utils/common.py` with centralized RDF operations
  - Base test class: `tests/base_test.py` reducing test setup duplication by 60%
  - Updated all test files to use common utilities and base classes
  - Enhanced error handling and validation across all tools

### Changed
- **Documentation**: Updated `README.md` and `docs/USAGE_GUIDE.md` with ArangoDB integration instructions
- **Testing Framework**: Refactored test suite with improved maintainability and consistency
- **Development Environment**: Enhanced with better code organization and shared utilities

### Fixed
- **Code Duplication**: Eliminated 6 instances of duplicate code patterns across test files
- **Build Artifacts**: Cleaned up all `__pycache__` directories and `.pyc` files
- **Test Reliability**: Fixed test compatibility issues with new base class structure

## [0.4.1] - 2025-09-04

### Fixed
- **Dependencies**: Installed missing `feedparser` dependency for AWS change monitoring tool
- **Virtual Environment**: Set up proper Python virtual environment with all required dependencies
- **Documentation**: Updated README.md metrics to reflect accurate example instance count (535+)
- **Monitoring**: AWS change monitoring tool now fully functional, tracking 52 recent changes across 11 services

### Changed
- **Development Environment**: Enhanced with complete dependency management and virtual environment setup
- **Testing**: All quality tests continue to pass with updated environment

## [0.4.0] - 2025-09-04

### Added
- **Missing AWS Services**: Comprehensive addition of 17 new AWS service classes to complete ontology coverage
  - **Compute Services**: `AutoScalingGroup`, `ECSContainerInstance`
  - **Storage Services**: `EFSFileSystem`, `RDSCluster`, `RDSSnapshot`
  - **Database Services**: `DynamoDBTable`, `DocumentDBCluster`, `RedshiftCluster`
  - **Networking Services**: `ElasticIP`, `ELBv2TargetGroup`, `NetworkInterface`, `NetworkACL`, `VPCEndpoint`
  - **Security Services**: `KMSKey`, `KMSAlias`, `SecretsManagerSecret`, `SecurityGroupRule`
  - **Identity Services**: `IAMInstanceProfile`
  - **Content Delivery**: `CloudFrontDistribution`
- **Comprehensive Examples**: 143+ new example instances covering all newly added services with realistic configurations
- **Enhanced Service Coverage**: Complete mapping support for common AWS node labels and resource types

### Changed
- **Ontology Growth**: 6.3% increase in triples (1,095 → 1,169), 24% increase in classes (71 → 88)
- **Example Growth**: 37% increase in example instances (390+ → 533+)
- **Complete Service Coverage**: Now supports all major AWS services for infrastructure modeling

### Fixed
- **Property Domain/Range Issues**: Fixed missing domain and range declarations for inverse properties (`approvesUseOf`, `attachmentOf`, `audits`, `availabilityZoneOf`)
- **Format Synchronization**: Maintained OWL ↔ TTL consistency throughout all additions
- **Quality Assurance**: All ontology quality tests passing after enhancements

## [0.3.0] - 2025-07-31

### Added
- **Container Services**: Complete ECS, EKS, Fargate, and ECR modeling (10 classes, 18 properties)
- **API & Integration Services**: API Gateway, Step Functions, EventBridge, SNS, SQS (12 classes, 38 properties)
- **Enhanced Relationships**: Temporal (`createdBefore`, `replacedBy`), cost (`incursChargeFor`, `optimizedBy`), and compliance (`compliesWith`, `auditedBy`) modeling (23 object properties, 18 data properties)
- **Semantic Axioms**: Cardinality constraints, disjoint class declarations, property characteristics (functional, transitive, symmetric)
- **Protégé Integration**: Complete visual exploration guide and 22 SPARQL query examples
- **Format Import Statements**: Examples file now properly imports the main ontology
- **Comprehensive Documentation**: Protégé guide, SPARQL examples, usage documentation

### Changed
- **Ontology Growth**: 84% increase in triples (596 → 1,095), doubled classes (35 → 71), tripled properties (45 → 155)
- **Enhanced Examples**: 390+ example instances with container, API, and integration scenarios
- **Improved Testing**: Extended test suite for container services, API services, and relationship validation

### Fixed
- **Format Synchronization**: Robust OWL ↔ TTL conversion and validation
- **Import Dependencies**: Proper ontology imports in examples file
- **Test Coverage**: Comprehensive validation across all new service categories
- Updated requirements.txt with optional testing dependencies

## [0.2.0] - 2025-07-30

### Added
- Comprehensive IAM classes and properties
- Data properties for all resource types
- OWL axioms and cardinality constraints
- Extensive example instances in TTL format
- Dual-format support (OWL and TTL)
- Format synchronization tools and tests
- IAM policy document structures
- Trust relationships and permission boundaries

### Changed
- Fixed class hierarchy inconsistencies
- Enhanced property domains and ranges
- Improved inverse property declarations
- Updated version info to 0.2.0

### Fixed
- AWSAccount now properly subclass of AWSResource
- Corrected cardinality constraints for IAM entities
- Fixed property inheritance issues

## [0.1.0] - 2025-07-30

### Added
- Initial ontology structure with core AWS classes
- Basic class hierarchy for AWS resources
- Fundamental object and data properties
- Project documentation (README, PRD, LICENSE)
- Git repository setup
- Initial examples for core services

### Infrastructure
- Project repository structure
- Development tooling setup
- Documentation framework

## Template for Future Releases

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New service classes: ServiceX, ServiceY
- New properties: hasFeatureZ, supportsPatternW
- New example instances for ServiceX

### Changed
- Updated IAMPolicy to support new condition types
- Enhanced EC2Instance with new instance types
- Improved documentation for PropertyABC

### Deprecated
- OldServiceClass (will be removed in vX.0.0)
- Use NewServiceClass instead

### Removed
- UnsupportedFeature (deprecated in vX.Y.0)

### Fixed
- Corrected domain/range for propertyABC
- Fixed cardinality constraint for ClassXYZ

### Security
- Updated IAM policy patterns for new security features
```

## Version History Summary

- **v0.4.2**: ArangoDB integration, code quality improvements
- **v0.4.1**: Documentation and metrics corrections
- **v0.4.0**: Expanded service coverage (security, analytics-adjacent, storage), new properties
- **v0.3.0**: Container services, API integration, Protégé support
- **v0.2.0**: Enhanced IAM focus, dual-format support, comprehensive testing
- **v0.1.0**: Initial ontology with core AWS service coverage

## Migration Notes

### From v0.1.0 to v0.2.0
- No breaking changes
- All v0.1.0 queries remain compatible
- New IAM capabilities available
- Examples significantly expanded

## Links
- [GitHub Releases](https://github.com/YOUR_USERNAME/AWS_Ontology/releases)
- [Contributing Guide](README.md#development)
- [Maintenance Strategy](docs/MAINTENANCE_STRATEGY.md) 