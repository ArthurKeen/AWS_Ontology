# AWS Object and Relationship Ontology Development - Product Requirements Document

**Document Version:** 1.2
**Date:** July 2026

> **Requirement identifiers.** Every testable requirement in this document carries a stable
> `REQ-NNN` identifier. Drift tooling (`/prd-sync`) audits the implementation against these IDs
> and records gaps in the shared `drift_alerts` collection keyed as `aws-ontology_REQ-NNN`.
> IDs are never renumbered; retired requirements are marked **RETIRED** in place.

## 1. Introduction

This document outlines the requirements for an ontology of Amazon Web Services (AWS) objects and
their interrelationships. The goal is a machine-readable model that ensures consistent data
representation, facilitates advanced querying, and enables comprehensive analysis of AWS
configurations.

## 2. Objective

Define a comprehensive and semantically rich ontology of AWS resources and their operational,
structural, and logical connections, serving as a foundational knowledge base for understanding
complex AWS environments.

## 3. Scope

The ontology primarily covers core and widely used AWS services:

- **Compute:** EC2 (Instances, AMIs, Security Groups, Load Balancers, Auto Scaling Groups), Lambda
- **Containers:** ECS, EKS, Fargate, ECR
- **Storage:** S3 (Buckets, Objects), EBS (Volumes, Snapshots), EFS, RDS (Instances, Databases)
- **Networking:** VPC (Subnets, Route Tables, Internet Gateways, NAT Gateways), Security Groups,
  Network ACLs, CloudFront
- **Identity & Access Management (IAM):** Users, Roles, Policies, Groups
- **Databases:** DynamoDB, Aurora (as part of RDS), DocumentDB, Redshift
- **Integration:** API Gateway, Step Functions, EventBridge, SNS, SQS
- **Security:** KMS, Secrets Manager
- **Monitoring & Logging:** CloudWatch, CloudTrail

### Future scope (roadmap, not yet requirements)

The following 2023+ service areas are candidates for promotion to requirements in a future PRD
revision: Bedrock/GenAI, SageMaker, analytics (Glue, Athena, Kinesis, EMR, OpenSearch),
IAM Identity Center, Organizations/Control Tower, Cognito, security services (GuardDuty,
Security Hub, WAF, Config), Route 53, Transit Gateway/Direct Connect, ElastiCache,
CloudFormation/IaC, CodePipeline, Systems Manager.

## 4. Key Entities (Classes)

| ID | Requirement |
|----|-------------|
| REQ-001 | Infrastructure classes MUST exist: `AWSAccount`, `AWSRegion`, `AvailabilityZone` |
| REQ-002 | Compute classes MUST exist: `EC2Instance`, `EC2AMI`, `EC2SecurityGroup`, `EC2LoadBalancer`, `LambdaFunction` |
| REQ-003 | Storage classes MUST exist: `S3Bucket`, `S3Object`, `EBSVolume`, `EBSSnapshot`, `RDSInstance`, `RDSDatabase` |
| REQ-004 | Identity classes MUST exist: `IAMUser`, `IAMRole`, `IAMPolicy`, `IAMGroup` |
| REQ-005 | Networking classes MUST exist: `VPC`, `Subnet`, `RouteTable`, `InternetGateway`, `NATGateway` |
| REQ-006 | Monitoring classes MUST exist: `CloudWatchMetric`, `CloudWatchAlarm`, `CloudTrailLog` |
| REQ-007 | Database classes MUST cover DynamoDB (`DynamoDBTable`) and Aurora (as part of the RDS class family) |

Additional classes may be added as necessary to represent the AWS ecosystem accurately; the
implemented ontology may exceed this list.

## 5. Relationships (Properties)

| ID | Requirement |
|----|-------------|
| REQ-008 | Structural/compositional properties MUST exist: `hasRegion`, `hasAvailabilityZone`, `contains`, `attachedTo`, `belongsToVPC` |
| REQ-009 | `canAssumeRole` MUST relate IAM principals (users/roles) to IAM roles they may assume |
| REQ-010 | `hasPolicy` MUST relate IAM entities (users/roles/groups) to attached policies (the equivalent `hasPolicyAttachment` satisfies this via an `owl:equivalentProperty` axiom) |
| REQ-011 | `appliesTo` MUST relate security groups to the resources they protect |
| REQ-012 | Operational/functional properties MUST exist: `uses`, `manages`, `monitors`, `logsActivityOf`, `routesTrafficThrough` |
| REQ-013 | Dependency properties MUST exist: `dependsOn` (general), `isSourceFor` (e.g., snapshot → volume) |
| REQ-014 | Inverse properties MUST be defined where semantically meaningful |

## 6. Output Format

| ID | Requirement |
|----|-------------|
| REQ-015 | The ontology MUST adhere to OWL 2 DL (validated with standard OWL reasoners/tools) |
| REQ-016 | Properties MUST specify `rdfs:domain` and `rdfs:range`, EXCEPT deliberately generic properties (`contains`, `uses`, `dependsOn`, and similar cross-cutting relations) where broad applicability is intended |
| REQ-017 | Every class and property MUST have an `rdfs:label` and `rdfs:comment` |
| REQ-018 | The ontology MUST ship with at least 50 example instances spanning all major service categories |
| REQ-019 | The ontology MUST be published in two synchronized serializations (Turtle and OWL/XML) verified semantically identical |

## 7. Data Sources

AWS Service Documentation, AWS Whitepapers, and AWS API Reference documentation
(publicly available information only).

## 8. Quality Criteria

Consistency (no contradictions), completeness (coverage of specified scope), accuracy
(faithful to AWS behavior), expressiveness (effective OWL constructs), usability
(querying/reasoning/integration), modularity (structured for extension).

## 9. Integration and Performance

| ID | Requirement |
|----|-------------|
| REQ-020 | The ontology MUST be transformable into at least one graph database (ArangoDB via ArangoRDF), with a working import tool |
| REQ-021 | Performance budgets: complete ontology loads in <5s in standard tools; common SPARQL/AQL queries respond in <1s; ArangoDB transformation completes in <30s; reasoning stays under 500MB RAM |

### Coverage targets (informational)

- Service coverage: >90% of the services listed in §3
- Relationship coverage: >80% of critical service relationships
- IAM coverage: 100% of core IAM concepts (Users, Roles, Policies, Groups)
- Tool compatibility: minimum 3 major ontology tools (Protégé, Apache Jena, rdflib)

## 10. Maintenance and Versioning Strategy

### Version Control
- **Semantic Versioning:** MAJOR (breaking structure changes) / MINOR (new services,
  non-breaking additions) / PATCH (bug fixes, documentation, examples)
- `owl:versionInfo` MUST match the latest CHANGELOG release

### Update Schedule
- **Quarterly Reviews:** assessment of new AWS services and features
- **Annual Major Updates:** comprehensive review and potential restructuring
- **On-Demand Updates:** critical security-related updates as needed

### Backward Compatibility
- Maintain backward compatibility for existing relationships and classes
- 6-month notice period for deprecated concepts (mark with `owl:deprecated`)
- Provide transformation scripts for major version updates

### Change Management
- All modifications documented in CHANGELOG with rationale
- All changes validated against the test suite and example instances
- Major changes reviewed by project stakeholders before implementation

## 11. Security and Privacy Considerations

- **Public information only:** based exclusively on publicly available AWS documentation;
  no proprietary AWS architecture or internal information
- **Sanitized examples:** fictional or anonymized data only; no PII; generic resource names
- **License compliance:** all dependencies and tools comply with project licensing
- **No credentials in code:** database and service credentials come from environment
  variables, never hardcoded defaults

## 12. Constraints and Assumptions

- Based on publicly available information only
- Represents a conceptual model of AWS resources
- Prioritizes common and general relationships over edge cases
- No access to internal AWS system diagrams or proprietary information
