# Changelog

All notable changes to the AWS Ontology project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite for ontology quality assurance
- Performance testing with PRD success metrics validation
- Example instance validation tests
- Git pre-commit hooks for format synchronization
- AWS change monitoring tool for tracking service updates
- Maintenance strategy documentation
- ArangoDB transformation tools with RPT, PGT, and LPGT patterns

### Changed
- Enhanced README with detailed testing documentation
- Updated requirements.txt with optional testing dependencies

## [0.2.0] - 2024-12-XX

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

## [0.1.0] - 2024-12-XX

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

- **v0.2.0**: Enhanced IAM focus, dual-format support, comprehensive testing
- **v0.1.0**: Initial ontology with core AWS service coverage

## Migration Notes

### From v0.1.0 to v0.2.0
- No breaking changes
- All v0.1.0 queries remain compatible
- New IAM capabilities available
- Examples significantly expanded

## Links
- [GitHub Releases](https://github.com/ArthurKeen/AWS_Ontology/releases)
- [Contributing Guide](README.md#development)
- [Maintenance Strategy](docs/MAINTENANCE_STRATEGY.md) 