#!/usr/bin/env python3
"""
Test script to ensure OWL and TTL ontology files are semantically synchronized.
"""

import unittest
import os
import sys
from pathlib import Path

try:
    from rdflib import Graph, compare
    from rdflib.util import guess_format
except ImportError:
    print("rdflib not installed. Install with: pip install rdflib")
    sys.exit(1)


class TestFormatSynchronization(unittest.TestCase):
    """Test that OWL and TTL files contain identical semantic content."""
    
    def setUp(self):
        """Set up test paths."""
        self.project_root = Path(__file__).parent.parent
        self.owl_file = self.project_root / "ontology" / "aws.owl"
        self.ttl_file = self.project_root / "ontology" / "aws.ttl"
        
    def test_files_exist(self):
        """Test that both ontology files exist."""
        self.assertTrue(
            self.owl_file.exists(),
            f"OWL file not found: {self.owl_file}"
        )
        self.assertTrue(
            self.ttl_file.exists(),
            f"TTL file not found: {self.ttl_file}"
        )
    
    def test_files_parseable(self):
        """Test that both files can be parsed as valid RDF."""
        # Test OWL file
        owl_graph = Graph()
        try:
            owl_graph.parse(str(self.owl_file), format="xml")
        except Exception as e:
            self.fail(f"Failed to parse OWL file: {e}")
        
        # Test TTL file
        ttl_graph = Graph()
        try:
            ttl_graph.parse(str(self.ttl_file), format="turtle")
        except Exception as e:
            self.fail(f"Failed to parse TTL file: {e}")
    
    def test_semantic_equivalence(self):
        """Test that OWL and TTL files are semantically equivalent."""
        # Load both graphs
        owl_graph = Graph()
        owl_graph.parse(str(self.owl_file), format="xml")
        
        ttl_graph = Graph()
        ttl_graph.parse(str(self.ttl_file), format="turtle")
        
        # Compare graph sizes
        owl_size = len(owl_graph)
        ttl_size = len(ttl_graph)
        
        self.assertEqual(
            owl_size, ttl_size,
            f"Different number of triples: OWL={owl_size}, TTL={ttl_size}"
        )
        
        # Test semantic equivalence using graph isomorphism
        iso_result = compare.isomorphic(owl_graph, ttl_graph)
        
        if not iso_result:
            # If not isomorphic, find differences for debugging
            owl_only = owl_graph - ttl_graph
            ttl_only = ttl_graph - owl_graph
            
            error_msg = "Graphs are not semantically equivalent.\n"
            if len(owl_only) > 0:
                error_msg += f"Triples only in OWL ({len(owl_only)}):\n"
                for triple in list(owl_only)[:5]:  # Show first 5
                    error_msg += f"  {triple}\n"
                if len(owl_only) > 5:
                    error_msg += f"  ... and {len(owl_only) - 5} more\n"
            
            if len(ttl_only) > 0:
                error_msg += f"Triples only in TTL ({len(ttl_only)}):\n"
                for triple in list(ttl_only)[:5]:  # Show first 5
                    error_msg += f"  {triple}\n"
                if len(ttl_only) > 5:
                    error_msg += f"  ... and {len(ttl_only) - 5} more\n"
            
            self.fail(error_msg)
    
    def test_version_consistency(self):
        """Test that version information is consistent between files."""
        owl_graph = Graph()
        owl_graph.parse(str(self.owl_file), format="xml")
        
        ttl_graph = Graph()
        ttl_graph.parse(str(self.ttl_file), format="turtle")
        
        # Query for version information
        version_query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?version WHERE {
            ?ontology a owl:Ontology ;
                      owl:versionInfo ?version .
        }
        """
        
        owl_versions = list(owl_graph.query(version_query))
        ttl_versions = list(ttl_graph.query(version_query))
        
        self.assertEqual(
            len(owl_versions), 1,
            f"Expected exactly one version in OWL file, found {len(owl_versions)}"
        )
        self.assertEqual(
            len(ttl_versions), 1,
            f"Expected exactly one version in TTL file, found {len(ttl_versions)}"
        )
        
        owl_version = str(owl_versions[0][0])
        ttl_version = str(ttl_versions[0][0])
        
        self.assertEqual(
            owl_version, ttl_version,
            f"Version mismatch: OWL={owl_version}, TTL={ttl_version}"
        )
    
    def test_class_count_consistency(self):
        """Test that both files have the same number of classes."""
        owl_graph = Graph()
        owl_graph.parse(str(self.owl_file), format="xml")
        
        ttl_graph = Graph()
        ttl_graph.parse(str(self.ttl_file), format="turtle")
        
        class_query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT (COUNT(?class) as ?count) WHERE {
            ?class a owl:Class .
        }
        """
        
        owl_count = int(list(owl_graph.query(class_query))[0][0])
        ttl_count = int(list(ttl_graph.query(class_query))[0][0])
        
        self.assertEqual(
            owl_count, ttl_count,
            f"Different number of classes: OWL={owl_count}, TTL={ttl_count}"
        )
        
        # Ensure we have a reasonable number of classes
        self.assertGreater(
            owl_count, 20,
            f"Expected more than 20 classes, found {owl_count}"
        )
    
    def test_property_count_consistency(self):
        """Test that both files have the same number of properties."""
        owl_graph = Graph()
        owl_graph.parse(str(self.owl_file), format="xml")
        
        ttl_graph = Graph()
        ttl_graph.parse(str(self.ttl_file), format="turtle")
        
        object_prop_query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT (COUNT(?prop) as ?count) WHERE {
            ?prop a owl:ObjectProperty .
        }
        """
        
        data_prop_query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT (COUNT(?prop) as ?count) WHERE {
            ?prop a owl:DatatypeProperty .
        }
        """
        
        # Object properties
        owl_obj_count = int(list(owl_graph.query(object_prop_query))[0][0])
        ttl_obj_count = int(list(ttl_graph.query(object_prop_query))[0][0])
        
        self.assertEqual(
            owl_obj_count, ttl_obj_count,
            f"Different number of object properties: OWL={owl_obj_count}, TTL={ttl_obj_count}"
        )
        
        # Data properties
        owl_data_count = int(list(owl_graph.query(data_prop_query))[0][0])
        ttl_data_count = int(list(ttl_graph.query(data_prop_query))[0][0])
        
        self.assertEqual(
            owl_data_count, ttl_data_count,
            f"Different number of data properties: OWL={owl_data_count}, TTL={ttl_data_count}"
        )


def run_sync_test():
    """Run the synchronization test and return results."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFormatSynchronization)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Testing OWL and TTL format synchronization...")
    success = run_sync_test()
    
    if success:
        print("\n✅ All synchronization tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Synchronization tests failed!")
        sys.exit(1) 