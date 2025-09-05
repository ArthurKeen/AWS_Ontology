#!/usr/bin/env python3
"""
Import AWS Ontology into ArangoDB using ArangoRDF.
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.common import get_ontology_files, load_ontology_graph, TTL_FORMAT
from utils.logging_config import setup_tool_logging

try:
    from arango import ArangoClient
    from arango_rdf import ArangoRDF
    from rdflib import Graph
    ARANGO_AVAILABLE = True
except ImportError as e:
    logging.error(f"ArangoDB dependencies not available: {e}")
    logging.info("Please install: pip install python-arango")
    logging.info("And ensure ArangoRDF is installed from local clone")
    ARANGO_AVAILABLE = False


def connect_to_arangodb(host: str = 'http://localhost:8529', 
                       username: str = 'root', 
                       password: str = None,
                       db_name: str = 'aws_ontology') -> Optional[object]:
    """Connect to ArangoDB and create/access database."""
    if password is None:
        password = os.getenv('ARANGO_PASSWORD', 'openSesame')
    
    try:
        logging.info(f"Connecting to ArangoDB at {host}...")
        client = ArangoClient(hosts=host)
        
        # Connect to system database first
        sys_db = client.db('_system', username=username, password=password)
        
        # Try to create database
        try:
            db = sys_db.create_database(db_name)
            logging.info(f"Created new database: {db_name}")
        except Exception:
            # Database exists, connect to it
            db = client.db(db_name, username=username, password=password)
            logging.info(f"Connected to existing database: {db_name}")
        
        return db
        
    except Exception as e:
        logging.error(f"Failed to connect to ArangoDB: {e}")
        logging.info("Make sure ArangoDB is running and credentials are correct")
        return None


def load_ontology_data(include_examples: bool = True) -> Optional[Graph]:
    """Load AWS ontology data."""
    logging.info("Loading AWS ontology...")
    
    ttl_file, owl_file, examples_file = get_ontology_files()
    
    # Load main ontology
    ontology_graph = load_ontology_graph(ttl_file, TTL_FORMAT)
    if ontology_graph is None:
        logging.error("Failed to load main ontology")
        return None
    
    logging.info(f"Loaded ontology: {len(ontology_graph)} triples")
    
    if include_examples:
        # Load examples
        examples_graph = load_ontology_graph(examples_file, TTL_FORMAT)
        if examples_graph is None:
            logging.error("Failed to load examples")
            return None
        
        logging.info(f"Loaded examples: {len(examples_graph)} triples")
        
        # Combine ontology and examples
        combined_graph = Graph()
        combined_graph += ontology_graph
        combined_graph += examples_graph
        
        logging.info(f"Combined total: {len(combined_graph)} triples")
        return combined_graph
    
    return ontology_graph


def import_rdf_data(db, graph: Graph, overwrite: bool = True) -> bool:
    """Import RDF data into ArangoDB."""
    try:
        logging.info("Initializing ArangoRDF...")
        arango_rdf = ArangoRDF(db)
        
        logging.info(f"Importing {len(graph)} triples into ArangoDB...")
        arango_rdf.insert_rdf(graph, overwrite=overwrite)
        
        logging.info("Successfully imported RDF data")
        return True
        
    except Exception as e:
        logging.error(f"Failed to import RDF data: {e}")
        return False


def print_database_stats(db):
    """Print database statistics."""
    logging.info("Database Statistics:")
    try:
        collections = db.collections()
        total_docs = 0
        
        for collection in collections:
            if not collection['name'].startswith('_'):
                count = db.collection(collection['name']).count()
                total_docs += count
                logging.info(f"  {collection['name']}: {count:,} documents")
        
        logging.info(f"Total documents: {total_docs:,}")
        
    except Exception as e:
        logging.error(f"Failed to get statistics: {e}")


def test_queries(db):
    """Run test queries to verify import."""
    logging.info("Running test queries...")
    
    try:
        # Query 1: Count AWS classes
        aql = """
        FOR doc IN statements
            FILTER doc.predicate == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
            FILTER doc.object == "http://www.w3.org/2002/07/owl#Class"
            FILTER CONTAINS(doc.subject, "aws-ontology")
            RETURN doc.subject
        """
        
        cursor = db.aql.execute(aql)
        aws_classes = list(cursor)
        logging.info(f"Found {len(aws_classes)} AWS ontology classes")
        
        # Query 2: Count example instances
        aql = """
        FOR doc IN statements
            FILTER doc.predicate == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
            FILTER CONTAINS(doc.subject, "example")
            RETURN doc.subject
        """
        
        cursor = db.aql.execute(aql)
        examples = list(cursor)
        logging.info(f"Found {len(examples)} example instances")
        
        # Query 3: Sample EC2 instances
        aql = """
        FOR doc IN statements
            FILTER doc.predicate == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
            FILTER doc.object == "http://www.semanticweb.org/aws-ontology#EC2Instance"
            LIMIT 5
            RETURN doc.subject
        """
        
        cursor = db.aql.execute(aql)
        ec2_instances = list(cursor)
        logging.info(f"Sample EC2 instances: {len(ec2_instances)}")
        
        return True
        
    except Exception as e:
        logging.error(f"Test queries failed: {e}")
        return False


def main():
    """Main function."""
    if not ARANGO_AVAILABLE:
        sys.exit(1)
    
    parser = argparse.ArgumentParser(
        description="Import AWS Ontology into ArangoDB using ArangoRDF"
    )
    
    parser.add_argument(
        '--host',
        default='http://localhost:8529',
        help='ArangoDB host (default: http://localhost:8529)'
    )
    
    parser.add_argument(
        '--username',
        default='root',
        help='ArangoDB username (default: root)'
    )
    
    parser.add_argument(
        '--password',
        default=None,
        help='ArangoDB password (default: from ARANGO_PASSWORD env var)'
    )
    
    parser.add_argument(
        '--database',
        default='aws_ontology',
        help='Database name (default: aws_ontology)'
    )
    
    parser.add_argument(
        '--no-examples',
        action='store_true',
        help='Import only ontology, skip examples'
    )
    
    parser.add_argument(
        '--no-overwrite',
        action='store_true',
        help='Do not overwrite existing data'
    )
    
    parser.add_argument(
        '--test-queries',
        action='store_true',
        help='Run test queries after import'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_tool_logging("import_to_arangodb", args.verbose if hasattr(args, 'verbose') else False)
    
    logger.info("AWS Ontology → ArangoDB Import Tool")
    logger.info("=" * 50)
    
    # Step 1: Load ontology data
    graph = load_ontology_data(include_examples=not args.no_examples)
    if graph is None:
        sys.exit(1)
    
    # Step 2: Connect to ArangoDB
    db = connect_to_arangodb(
        host=args.host,
        username=args.username,
        password=args.password,
        db_name=args.database
    )
    if db is None:
        sys.exit(1)
    
    # Step 3: Import data
    success = import_rdf_data(db, graph, overwrite=not args.no_overwrite)
    if not success:
        sys.exit(1)
    
    # Step 4: Show statistics
    print_database_stats(db)
    
    # Step 5: Run test queries if requested
    if args.test_queries:
        test_queries(db)
    
    logger.info("Import completed successfully!")
    logger.info("Next steps:")
    logger.info(f"1. Access ArangoDB web interface: {args.host}")
    logger.info(f"2. Explore database: {args.database}")
    logger.info(f"3. Run AQL queries on the imported ontology")
    logger.info(f"4. See docs/ARANGODB_INTEGRATION.md for query examples")


if __name__ == "__main__":
    main()
