#!/usr/bin/env python3
"""
OWL 2 DL compliance checks (PRD REQ-015).

Guards against the axiom-level defects that standard data-quality tests miss:
undeclared terms referenced in axioms, and constructs that are illegal in the
OWL 2 DL profile (e.g. inverse-functional datatype properties).
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.base_test import BaseOntologyTest
from utils.common import ONTOLOGY_NAMESPACE

try:
    from rdflib import OWL, RDF, RDFS
    from rdflib.term import BNode

    RDFLIB_AVAILABLE = True
except ImportError:
    RDFLIB_AVAILABLE = False


@unittest.skipUnless(RDFLIB_AVAILABLE, "rdflib not available")
class TestDLCompliance(BaseOntologyTest):
    """OWL 2 DL profile checks over the TTL serialization."""

    def in_aws_namespace(self, term) -> bool:
        return not isinstance(term, BNode) and str(term).startswith(ONTOLOGY_NAMESPACE)

    def declared_properties(self) -> set:
        return set(self.graph.subjects(RDF.type, OWL.ObjectProperty)) | set(
            self.graph.subjects(RDF.type, OWL.DatatypeProperty)
        )

    def declared_classes(self) -> set:
        return set(self.graph.subjects(RDF.type, OWL.Class))

    def test_no_inverse_functional_datatype_properties(self):
        """OWL 2 DL forbids inverse-functional datatype properties (use owl:hasKey)."""
        for prop in self.graph.subjects(RDF.type, OWL.DatatypeProperty):
            self.assertNotIn(
                (prop, RDF.type, OWL.InverseFunctionalProperty),
                self.graph,
                f"{prop} is a datatype property typed owl:InverseFunctionalProperty — "
                "illegal in OWL 2 DL; express uniqueness with owl:hasKey instead",
            )

    def test_restriction_properties_are_declared(self):
        """Every owl:onProperty target must be a declared property."""
        declared = self.declared_properties()
        for restriction, prop in self.graph.subject_objects(OWL.onProperty):
            if self.in_aws_namespace(prop):
                self.assertIn(
                    prop,
                    declared,
                    f"owl:Restriction {restriction} references undeclared property {prop}",
                )

    def test_property_axiom_references_are_declared(self):
        """inverseOf / equivalentProperty / subPropertyOf must reference declared properties."""
        declared = self.declared_properties()
        for predicate in (OWL.inverseOf, OWL.equivalentProperty, RDFS.subPropertyOf):
            for subject, obj in self.graph.subject_objects(predicate):
                for term in (subject, obj):
                    if self.in_aws_namespace(term):
                        self.assertIn(
                            term,
                            declared,
                            f"{predicate.n3()} axiom references undeclared property {term}",
                        )

    def test_domain_range_classes_are_declared(self):
        """rdfs:domain / rdfs:range targets in the AWS namespace must be declared classes."""
        declared = self.declared_classes()
        for predicate in (RDFS.domain, RDFS.range):
            for prop, cls in self.graph.subject_objects(predicate):
                if self.in_aws_namespace(cls):
                    self.assertIn(
                        cls,
                        declared,
                        f"{prop} has {predicate.n3()} pointing at undeclared class {cls}",
                    )

    def test_subclass_references_are_declared(self):
        """Named rdfs:subClassOf targets in the AWS namespace must be declared classes."""
        declared = self.declared_classes()
        for cls, parent in self.graph.subject_objects(RDFS.subClassOf):
            if self.in_aws_namespace(parent):
                self.assertIn(
                    parent,
                    declared,
                    f"{cls} declares undeclared superclass {parent}",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
