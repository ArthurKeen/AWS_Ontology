#!/usr/bin/env python3
"""
Comprehensive ontology quality tests for AWS Ontology.
Tests structure, consistency, completeness, and compliance.
"""

import unittest
import re
from pathlib import Path

try:
    from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal
    from rdflib.namespace import XSD
    RDFLIB_AVAILABLE = True
except ImportError:
    print("rdflib not installed. Install with: pip install rdflib")
    RDFLIB_AVAILABLE = False


@unittest.skipUnless(RDFLIB_AVAILABLE, "rdflib not available")
class TestOntologyQuality(unittest.TestCase):
    """Comprehensive ontology quality tests."""
    
    def setUp(self):
        """Set up test environment."""
        self.project_root = Path(__file__).parent.parent
        self.ttl_file = self.project_root / "ontology" / "aws.ttl"
        
        # Load ontology
        self.graph = Graph()
        self.graph.parse(str(self.ttl_file), format="turtle")
        
        # Define namespaces
        self.aws = Namespace("http://www.semanticweb.org/aws-ontology#")
        self.graph.bind("aws", self.aws)

    def test_ontology_metadata(self):
        """Test that ontology has proper metadata."""
        # Check ontology declaration exists
        ontology_uri = URIRef("http://www.semanticweb.org/aws-ontology")
        self.assertTrue(
            (ontology_uri, RDF.type, OWL.Ontology) in self.graph,
            "Ontology declaration not found"
        )
        
        # Check required metadata
        metadata_props = [
            (ontology_uri, RDFS.label),
            (ontology_uri, RDFS.comment),
            (ontology_uri, OWL.versionInfo)
        ]
        
        for subject, predicate in metadata_props:
            self.assertTrue(
                any(self.graph.triples((subject, predicate, None))),
                f"Missing metadata: {predicate}"
            )

    def test_class_consistency(self):
        """Test class definitions for consistency."""
        classes = list(self.graph.subjects(RDF.type, OWL.Class))
        
        # Ensure we have classes
        self.assertGreater(len(classes), 20, "Expected more than 20 classes")
        
        # Check that all classes have labels
        missing_labels = []
        for cls in classes:
            if not any(self.graph.triples((cls, RDFS.label, None))):
                missing_labels.append(cls)
        
        self.assertEqual(
            len(missing_labels), 0,
            f"Classes missing labels: {missing_labels}"
        )
        
        # Check that all classes have comments
        missing_comments = []
        for cls in classes:
            if not any(self.graph.triples((cls, RDFS.comment, None))):
                missing_comments.append(cls)
        
        self.assertEqual(
            len(missing_comments), 0,
            f"Classes missing comments: {missing_comments}"
        )

    def test_property_consistency(self):
        """Test property definitions for consistency."""
        # Get all object and data properties
        obj_props = list(self.graph.subjects(RDF.type, OWL.ObjectProperty))
        data_props = list(self.graph.subjects(RDF.type, OWL.DatatypeProperty))
        
        all_props = obj_props + data_props
        
        # Ensure we have properties
        self.assertGreater(len(all_props), 15, "Expected more than 15 properties")
        
        # Check that all properties have labels
        missing_labels = []
        for prop in all_props:
            if not any(self.graph.triples((prop, RDFS.label, None))):
                missing_labels.append(prop)
        
        self.assertEqual(
            len(missing_labels), 0,
            f"Properties missing labels: {missing_labels}"
        )
        
        # Check that all properties have comments
        missing_comments = []
        for prop in all_props:
            if not any(self.graph.triples((prop, RDFS.comment, None))):
                missing_comments.append(prop)
        
        self.assertEqual(
            len(missing_comments), 0,
            f"Properties missing comments: {missing_comments}"
        )

    def test_domain_range_consistency(self):
        """Test that domain and range declarations are consistent."""
        obj_props = list(self.graph.subjects(RDF.type, OWL.ObjectProperty))
        
        # Check object properties have appropriate domains and ranges
        for prop in obj_props:
            domains = list(self.graph.objects(prop, RDFS.domain))
            ranges = list(self.graph.objects(prop, RDFS.range))
            
            # Skip properties that intentionally have no domain/range restrictions
            prop_name = str(prop).split('#')[-1]
            if prop_name in ['uses', 'manages', 'dependsOn', 'contains', 'attachedTo']:
                continue
                
            # Most properties should have at least a domain or range
            self.assertTrue(
                len(domains) > 0 or len(ranges) > 0,
                f"Property {prop} has neither domain nor range"
            )

    def test_class_hierarchy_consistency(self):
        """Test that class hierarchy is properly structured."""
        # Check that AWSResource is the root class for most classes
        aws_resource = self.aws.AWSResource
        
        # Get all classes that should be subclasses of AWSResource
        resource_classes = [
            self.aws.ComputeResource,
            self.aws.StorageResource,
            self.aws.NetworkingResource,
            self.aws.SecurityResource,
            self.aws.IdentityResource,
            self.aws.DatabaseResource,
            self.aws.MonitoringResource
        ]
        
        for cls in resource_classes:
            self.assertTrue(
                (cls, RDFS.subClassOf, aws_resource) in self.graph,
                f"{cls} should be subclass of AWSResource"
            )
        
        # Check that infrastructure classes are also subclasses of AWSResource
        infrastructure_classes = [
            self.aws.AWSAccount,
            self.aws.AWSRegion,
            self.aws.AvailabilityZone
        ]
        
        for cls in infrastructure_classes:
            self.assertTrue(
                (cls, RDFS.subClassOf, aws_resource) in self.graph,
                f"{cls} should be subclass of AWSResource"
            )

    def test_inverse_properties(self):
        """Test that inverse properties are properly defined."""
        # Define expected inverse property pairs
        expected_inverses = [
            (self.aws.hasRegion, self.aws.regionOf),
            (self.aws.hasAvailabilityZone, self.aws.availabilityZoneOf),
            (self.aws.contains, self.aws.containedBy),
            (self.aws.attachedTo, self.aws.attachmentOf),
            (self.aws.memberOf, self.aws.hasMember),
            (self.aws.uses, self.aws.usedBy),
            (self.aws.manages, self.aws.managedBy),
            (self.aws.monitors, self.aws.monitoredBy),
            (self.aws.dependsOn, self.aws.dependencyOf),
            (self.aws.isSourceFor, self.aws.hasSource)
        ]
        
        for prop1, prop2 in expected_inverses:
            # Check if inverse relationship is declared
            inverse_declared = (
                (prop1, OWL.inverseOf, prop2) in self.graph or
                (prop2, OWL.inverseOf, prop1) in self.graph
            )
            
            self.assertTrue(
                inverse_declared,
                f"Inverse relationship not declared between {prop1} and {prop2}"
            )

    def test_required_aws_classes(self):
        """Test that all required AWS classes from PRD are present."""
        required_classes = [
            # Infrastructure
            'AWSAccount', 'AWSRegion', 'AvailabilityZone',
            # Compute
            'EC2Instance', 'EC2AMI', 'EC2SecurityGroup', 'EC2LoadBalancer', 'LambdaFunction',
            # Storage
            'S3Bucket', 'S3Object', 'EBSVolume', 'EBSSnapshot', 'RDSInstance', 'RDSDatabase',
            # Networking
            'VPC', 'Subnet', 'RouteTable', 'InternetGateway', 'NATGateway',
            # IAM
            'IAMUser', 'IAMRole', 'IAMGroup', 'IAMPolicy',
            # Monitoring
            'CloudWatchMetric', 'CloudWatchAlarm', 'CloudTrailLog'
        ]
        
        existing_classes = [str(cls).split('#')[-1] for cls in self.graph.subjects(RDF.type, OWL.Class)]
        
        for required_class in required_classes:
            self.assertIn(
                required_class, existing_classes,
                f"Required class missing: {required_class}"
            )

    def test_iam_specific_structure(self):
        """Test IAM-specific ontology structure."""
        # Check IAM policy hierarchy
        iam_policy = self.aws.IAMPolicy
        policy_types = [
            self.aws.ManagedPolicy,
            self.aws.InlinePolicy,
            self.aws.IAMPermissionBoundary,
            self.aws.IAMTrustPolicy,
            self.aws.ServiceControlPolicy
        ]
        
        for policy_type in policy_types:
            # Check if it's a subclass of IAMPolicy (directly or indirectly)
            self.assertTrue(
                self._is_subclass_of(policy_type, iam_policy),
                f"{policy_type} should be subclass of IAMPolicy"
            )
        
        # Check that IAMRole has trust relationship constraint
        role_restrictions = list(self.graph.objects(self.aws.IAMRole, RDFS.subClassOf))
        has_trust_constraint = any(
            self._is_cardinality_restriction(restriction, self.aws.hasTrustRelationship)
            for restriction in role_restrictions
        )
        
        self.assertTrue(
            has_trust_constraint,
            "IAMRole should have cardinality constraint on hasTrustRelationship"
        )

    def test_owl_dl_compliance(self):
        """Test basic OWL DL compliance."""
        # Check for potential OWL DL violations
        
        # 1. No class should be both a class and an individual
        classes = set(self.graph.subjects(RDF.type, OWL.Class))
        individuals = set(self.graph.subjects(RDF.type, OWL.NamedIndividual))
        overlap = classes.intersection(individuals)
        
        self.assertEqual(
            len(overlap), 0,
            f"Resources cannot be both classes and individuals: {overlap}"
        )
        
        # 2. Properties should have consistent types
        obj_props = set(self.graph.subjects(RDF.type, OWL.ObjectProperty))
        data_props = set(self.graph.subjects(RDF.type, OWL.DatatypeProperty))
        prop_overlap = obj_props.intersection(data_props)
        
        self.assertEqual(
            len(prop_overlap), 0,
            f"Properties cannot be both object and data properties: {prop_overlap}"
        )

    def test_naming_conventions(self):
        """Test naming conventions."""
        classes = list(self.graph.subjects(RDF.type, OWL.Class))
        properties = list(self.graph.subjects(RDF.type, OWL.ObjectProperty)) + \
                    list(self.graph.subjects(RDF.type, OWL.DatatypeProperty))
        
        # Check class naming (should start with uppercase)
        for cls in classes:
            class_name = str(cls).split('#')[-1]
            if class_name:  # Skip empty names
                self.assertTrue(
                    class_name[0].isupper(),
                    f"Class name should start with uppercase: {class_name}"
                )
        
        # Check property naming (should start with lowercase)
        for prop in properties:
            prop_name = str(prop).split('#')[-1]
            if prop_name:  # Skip empty names
                self.assertTrue(
                    prop_name[0].islower(),
                    f"Property name should start with lowercase: {prop_name}"
                )

    def test_data_property_ranges(self):
        """Test that data properties have appropriate ranges."""
        data_props = list(self.graph.subjects(RDF.type, OWL.DatatypeProperty))
        
        for prop in data_props:
            ranges = list(self.graph.objects(prop, RDFS.range))
            prop_name = str(prop).split('#')[-1]
            
            # Most data properties should have ranges
            if prop_name not in ['path']:  # Some exceptions allowed
                self.assertGreater(
                    len(ranges), 0,
                    f"Data property {prop_name} should have a range"
                )
            
            # Check that ranges are valid XSD types
            for range_val in ranges:
                if str(range_val).startswith(str(XSD)):
                    valid_types = [
                        XSD.string, XSD.integer, XSD.boolean, 
                        XSD.dateTime, XSD.decimal, XSD.float
                    ]
                    self.assertIn(
                        range_val, valid_types,
                        f"Invalid XSD type: {range_val}"
                    )

    def _is_subclass_of(self, subclass, superclass):
        """Check if subclass is a subclass of superclass (transitively)."""
        if (subclass, RDFS.subClassOf, superclass) in self.graph:
            return True
        
        # Check transitively
        for intermediate in self.graph.objects(subclass, RDFS.subClassOf):
            if self._is_subclass_of(intermediate, superclass):
                return True
        
        return False

    def _is_cardinality_restriction(self, restriction, on_property):
        """Check if restriction is a cardinality restriction on given property."""
        if not (restriction, RDF.type, OWL.Restriction) in self.graph:
            return False
        
        # Check if it's on the right property
        if not (restriction, OWL.onProperty, on_property) in self.graph:
            return False
        
        # Check if it has cardinality constraints
        cardinality_props = [
            OWL.cardinality, OWL.minCardinality, OWL.maxCardinality,
            OWL.qualifiedCardinality, OWL.minQualifiedCardinality, OWL.maxQualifiedCardinality
        ]
        
        return any((restriction, prop, None) in self.graph for prop in cardinality_props)


def run_quality_tests():
    """Run all ontology quality tests."""
    if not RDFLIB_AVAILABLE:
        print("❌ rdflib not available. Install with: pip install rdflib")
        return False
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOntologyQuality)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running ontology quality tests...")
    success = run_quality_tests()
    
    if success:
        print("\n✅ All quality tests passed!")
        exit(0)
    else:
        print("\n❌ Some quality tests failed!")
        exit(1) 