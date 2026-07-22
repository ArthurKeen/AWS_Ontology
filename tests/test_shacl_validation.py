#!/usr/bin/env python3
"""
SHACL validation tests for the AWS Resource Ontology.

Closed-world checks over ontology/examples.ttl using ontology/aws.shapes.ttl.
Complements the OWL open-world reasoning tests: OWL restrictions can never name
a specific individual as wrong, only "not enough information" — SHACL can.
"""

import sys
import unittest
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.common import get_ontology_files, get_project_root, load_ontology_graph

try:
    from pyshacl import validate

    PYSHACL_AVAILABLE = True
except ImportError:
    PYSHACL_AVAILABLE = False


@unittest.skipUnless(PYSHACL_AVAILABLE, "pyshacl not available")
class TestSHACLValidation(unittest.TestCase):
    """Validate example instances against ontology/aws.shapes.ttl."""

    @classmethod
    def setUpClass(cls):
        project_root = get_project_root()
        cls.shapes_file = project_root / "ontology" / "aws.shapes.ttl"
        _, _, examples_file = get_ontology_files()

        ontology_graph = load_ontology_graph(project_root / "ontology" / "aws.ttl", "turtle")
        examples_graph = load_ontology_graph(examples_file, "turtle")
        cls.data_graph = ontology_graph + examples_graph

        cls.shapes_graph = load_ontology_graph(cls.shapes_file, "turtle")
        self_check = cls.shapes_graph is not None
        if not self_check:
            raise RuntimeError(f"Failed to load SHACL shapes from {cls.shapes_file}")

    def run_validation(self):
        conforms, results_graph, results_text = validate(
            self.data_graph,
            shacl_graph=self.shapes_graph,
            ont_graph=None,
            inference=None,
            abort_on_first=False,
            allow_infos=True,
            allow_warnings=True,
        )
        return conforms, results_graph, results_text

    def test_no_violations(self):
        """No sh:Violation-severity shape may be broken by current example data.

        Warning-severity shapes (known, tracked data-completeness gaps — see
        ontology/aws.shapes.ttl header) are deliberately excluded from this gate.
        """
        conforms, _, results_text = self.run_validation()
        self.assertTrue(
            conforms,
            f"SHACL validation reported at least one Violation-severity result:\n{results_text}",
        )

    def test_shapes_file_is_valid_turtle(self):
        self.assertIsNotNone(self.shapes_graph)
        self.assertGreater(len(self.shapes_graph), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
