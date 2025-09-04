#!/usr/bin/env python3
"""
Base test class for AWS Ontology tests.
Provides common setup and utilities to reduce code duplication.
"""

import unittest
import sys
from pathlib import Path

# Add utils to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.common import (
    get_project_root,
    get_ontology_files,
    load_ontology_graph,
    setup_aws_namespace,
    check_rdflib_available,
    TTL_FORMAT,
    XML_FORMAT
)

try:
    from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal
    from rdflib.namespace import XSD
    RDFLIB_AVAILABLE = True
except ImportError:
    RDFLIB_AVAILABLE = False


@unittest.skipUnless(RDFLIB_AVAILABLE, "rdflib not available")
class BaseOntologyTest(unittest.TestCase):
    """Base test class for ontology-related tests."""
    
    def setUp(self):
        """Set up common test environment."""
        self.project_root = get_project_root()
        self.ttl_file, self.owl_file, self.examples_file = get_ontology_files()
        
        # Load main ontology graph
        self.graph = load_ontology_graph(self.ttl_file, TTL_FORMAT)
        self.assertIsNotNone(self.graph, "Failed to load TTL ontology")
        
        # Set up AWS namespace
        self.aws = setup_aws_namespace(self.graph)
        
    def load_examples_graph(self):
        """Load examples graph (called when needed)."""
        if not hasattr(self, 'examples_graph'):
            self.examples_graph = load_ontology_graph(self.examples_file, TTL_FORMAT)
            self.assertIsNotNone(self.examples_graph, "Failed to load examples")
        return self.examples_graph
    
    def load_combined_graph(self):
        """Load combined ontology + examples graph (called when needed)."""
        if not hasattr(self, 'combined_graph'):
            self.combined_graph = Graph()
            self.combined_graph += self.graph
            examples = self.load_examples_graph()
            self.combined_graph += examples
            setup_aws_namespace(self.combined_graph)
        return self.combined_graph
    
    def load_owl_graph(self):
        """Load OWL format graph (called when needed)."""
        if not hasattr(self, 'owl_graph'):
            self.owl_graph = load_ontology_graph(self.owl_file, XML_FORMAT)
            self.assertIsNotNone(self.owl_graph, "Failed to load OWL ontology")
        return self.owl_graph
    
    def assertTripleExists(self, subject, predicate, obj, graph=None):
        """Assert that a triple exists in the graph."""
        if graph is None:
            graph = self.graph
        self.assertTrue(
            (subject, predicate, obj) in graph,
            f"Triple not found: ({subject}, {predicate}, {obj})"
        )
    
    def assertClassExists(self, class_uri, graph=None):
        """Assert that a class exists in the ontology."""
        if graph is None:
            graph = self.graph
        self.assertTripleExists(class_uri, RDF.type, OWL.Class, graph)
    
    def assertPropertyExists(self, property_uri, graph=None):
        """Assert that a property exists in the ontology."""
        if graph is None:
            graph = self.graph
        # Check if it's either ObjectProperty or DatatypeProperty
        is_object_prop = (property_uri, RDF.type, OWL.ObjectProperty) in graph
        is_data_prop = (property_uri, RDF.type, OWL.DatatypeProperty) in graph
        self.assertTrue(
            is_object_prop or is_data_prop,
            f"Property not found: {property_uri}"
        )
    
    def get_class_instances(self, class_uri, graph=None):
        """Get all instances of a given class."""
        if graph is None:
            graph = self.combined_graph if hasattr(self, 'combined_graph') else self.load_combined_graph()
        return list(graph.subjects(RDF.type, class_uri))
    
    def get_all_classes(self, graph=None):
        """Get all classes defined in the ontology."""
        if graph is None:
            graph = self.graph
        return list(graph.subjects(RDF.type, OWL.Class))
    
    def get_all_properties(self, graph=None):
        """Get all properties defined in the ontology."""
        if graph is None:
            graph = self.graph
        object_props = list(graph.subjects(RDF.type, OWL.ObjectProperty))
        data_props = list(graph.subjects(RDF.type, OWL.DatatypeProperty))
        return object_props + data_props
