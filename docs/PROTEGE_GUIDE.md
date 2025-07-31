# Protégé Exploration Guide for AWS Ontology

## 🎯 Overview

This guide helps you explore the enhanced AWS Ontology using Protégé, the premier OWL ontology editor. Your ontology contains **1,095 triples** across **71 classes** and **155 properties**.

## 🚀 Getting Started

### Opening the Ontology

**Method 1: Direct Open (Recommended)**
```bash
open ontology/aws.owl
```

**Method 2: Via Protégé Menu**
1. Launch Protégé
2. File → Open
3. Navigate to: `/Users/arthurkeen/code/AWS_Ontology/ontology/aws.owl`

## 📊 What You'll Find

### Class Hierarchy (71 Classes)
- **Base Resources**: `ComputeResource`, `StorageResource`, `NetworkingResource`, `IntegrationResource`
- **Container Services**: `ECSCluster`, `EKSCluster`, `FargateService`, `ECRRepository`
- **API & Integration**: `APIGateway`, `StepFunction`, `EventBridge`, `SNSTopic`, `SQSQueue`
- **Enhanced IAM**: `IAMUser`, `IAMRole`, `IAMPolicy` with subtypes

### Object Properties (93 Properties)
- **Container Relationships**: `runsOnCluster`, `hasTaskDefinition`, `usesContainerImage`
- **API Relationships**: `hasStage`, `triggersStepFunction`, `publishesToTopic`
- **Temporal Relationships**: `createdBefore`, `replacedBy`, `migratedFrom`, `succeeds`
- **Cost Relationships**: `incursChargeFor`, `optimizedBy`, `allocatesCostTo`
- **Compliance Relationships**: `compliesWith`, `auditedBy`, `controlledBy`

### Data Properties (62 Properties)
- **Temporal**: `lastModifiedDate`, `deprecatedDate`, `retentionPeriodDays`
- **Cost**: `monthlyCostUSD`, `costCenter`, `billingMode`, `budgetAllocated`
- **Compliance**: `complianceStatus`, `dataClassification`, `encryptionRequired`

## 🔧 Essential Protégé Workflows

### 1. Validation & Reasoning

**Start the Reasoner:**
1. Tools → Reasoner → HermiT
2. Click "Start reasoner"
3. Check for consistency errors

**View Inferred Relationships:**
1. Window → Reasoner → Explain inferences
2. Browse inferred class hierarchy
3. Check property assertions

### 2. Explore Class Structure

**Class Hierarchy Tab:**
- Expand `AWSResource` to see all categories
- Notice strict hierarchy: `ComputeResource` → `ECSCluster`
- Check disjoint classes (they can't overlap)

**Individual Classes:**
- Select `APIGateway` → see cardinality constraint "≥ 1 hasStage"
- Select `ECSService` → see "exactly 1 hasTaskDefinition"
- Select `ContainerImage` → see "exactly 1 storedInRepository"

### 3. Object Properties Analysis

**Key Properties to Examine:**
- `triggersStepFunction`: API Gateway → Step Functions integration
- `publishesToTopic`: SNS pub/sub messaging
- `createdBefore`: Temporal ordering relationships
- `incursChargeFor`: Cost allocation relationships

**Property Characteristics:**
- **Functional**: `arn`, `creationDate` (unique values)
- **Symmetric**: `sharesResourcesWith`
- **Transitive**: `controls`, `dependsOn`, `createdBefore`
- **Inverse**: Most properties have inverses (e.g., `contains` ↔ `isContainedIn`)

### 4. Advanced Features

**OntoGraf Visualization:**
1. Window → Tabs → OntoGraf
2. Select a class (e.g., `APIGateway`)
3. Right-click → "Add connected classes"
4. Visualize the relationship network

**SPARQL Queries:**
1. Window → Tabs → SPARQL Query
2. Try these example queries:

```sparql
# Find all container services
PREFIX : <http://www.semanticweb.org/aws-ontology#>
SELECT ?service WHERE {
  ?service rdfs:subClassOf* :ComputeResource .
  ?service rdfs:label ?label .
  FILTER(CONTAINS(?label, "ECS") || CONTAINS(?label, "EKS") || CONTAINS(?label, "Fargate"))
}

# Find services that can trigger Step Functions
PREFIX : <http://www.semanticweb.org/aws-ontology#>
SELECT ?service ?stepFunction WHERE {
  ?service :triggersStepFunction ?stepFunction
}

# Find all cost-related properties
PREFIX : <http://www.semanticweb.org/aws-ontology#>
SELECT ?property WHERE {
  ?property rdfs:label ?label .
  FILTER(CONTAINS(LCASE(?label), "cost") || CONTAINS(LCASE(?label), "billing"))
}
```

## 🎯 Key Features to Validate

### Cardinality Constraints
- [ ] `APIGateway` requires ≥ 1 `hasStage`
- [ ] `ECSService` requires exactly 1 `hasTaskDefinition`
- [ ] `ECSService` runs on exactly 1 cluster
- [ ] `EventBridgeRule` requires ≥ 1 target

### Disjoint Classes
- [ ] Base resource types are mutually exclusive
- [ ] IAM policy types don't overlap
- [ ] Container service types are distinct

### Property Hierarchies
- [ ] All inverse properties are properly declared
- [ ] Domain and range restrictions are correct
- [ ] Property characteristics (functional, transitive) work

## 📈 Ontology Metrics Validation

Your ontology should show:
- **Total Triples**: 1,095
- **Classes**: 71
- **Object Properties**: 93
- **Data Properties**: 62

## 🔍 Troubleshooting

**Common Issues:**

1. **Reasoner Errors**: Check for circular dependencies or conflicting constraints
2. **Missing Imports**: Ensure all namespace prefixes are declared
3. **Performance**: Large ontologies may take time to load/reason

**Solutions:**
- Use HermiT reasoner for best OWL 2 DL support
- Check Window → Log for detailed error messages
- Disable reasoning temporarily for faster browsing

## 📚 Next Steps

After exploring in Protégé:
1. **Export Documentation**: Tools → Create ontology documentation
2. **Export Formats**: File → Export as (Turtle, JSON-LD, N-Triples)
3. **Query Testing**: Test complex SPARQL queries
4. **Extension Planning**: Identify areas for further development

## 🔗 Related Files

- `ontology/aws.owl` - Main ontology file
- `ontology/aws.ttl` - Turtle format (more readable)
- `ontology/examples.ttl` - Example instances
- `tests/` - Validation test suite
- `tools/sync_formats.py` - Format synchronization tool

---

For questions or issues, refer to the main project README.md or the test suite for validation examples.