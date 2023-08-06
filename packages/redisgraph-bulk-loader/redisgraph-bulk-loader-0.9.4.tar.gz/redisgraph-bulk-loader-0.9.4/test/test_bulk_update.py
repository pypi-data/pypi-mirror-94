# -*- coding: utf-8 -*-

import os
import csv
import redis
import unittest
from redisgraph import Graph
from click.testing import CliRunner
from redisgraph_bulk_loader.bulk_update import bulk_update


class TestBulkUpdate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Instantiate a new Redis connection
        """
        cls.redis_con = redis.Redis(host='localhost', port=6379, decode_responses=True)
        cls.redis_con.flushall()

    @classmethod
    def tearDownClass(cls):
        """Delete temporary files"""
        os.remove('/tmp/csv.tmp')
        cls.redis_con.flushall()

    def test01_simple_updates(self):
        """Validate that bulk updates work on an empty graph."""
        graphname = "tmpgraph1"
        # Write temporary files
        with open('/tmp/csv.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["id", "name"])
            out.writerow([0, "a"])
            out.writerow([5, "b"])
            out.writerow([3, "c"])

        runner = CliRunner()
        res = runner.invoke(bulk_update, ['--csv', '/tmp/csv.tmp',
                                          '--query', 'CREATE (:L {id: row[0], name: row[1]})',
                                          graphname], catch_exceptions=False)

        self.assertEqual(res.exit_code, 0)
        self.assertIn('Labels added: 1', res.output)
        self.assertIn('Nodes created: 3', res.output)
        self.assertIn('Properties set: 6', res.output)

        tmp_graph = Graph(graphname, self.redis_con)
        query_result = tmp_graph.query('MATCH (a) RETURN a.id, a.name ORDER BY a.id')

        # Validate that the expected results are all present in the graph
        expected_result = [[0, "a"],
                           [3, "c"],
                           [5, "b"]]
        self.assertEqual(query_result.result_set, expected_result)

        # Attempt to re-insert the entities using MERGE.
        res = runner.invoke(bulk_update, ['--csv', '/tmp/csv.tmp',
                                          '--query', 'MERGE (:L {id: row[0], name: row[1]})',
                                          graphname], catch_exceptions=False)

        # No new entities should be created.
        self.assertEqual(res.exit_code, 0)
        self.assertNotIn('Labels added', res.output)
        self.assertNotIn('Nodes created', res.output)
        self.assertNotIn('Properties set', res.output)

    def test02_traversal_updates(self):
        """Validate that bulk updates can create and perform traversals."""
        graphname = "tmpgraph2"
        # Write temporary files
        with open('/tmp/csv.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["id", "name"])
            out.writerow([0, "a"])
            out.writerow([5, "b"])
            out.writerow([3, "c"])

        # Create a graph of the form:
        # (a)-->(b)-->(c), (a)-->(c)
        runner = CliRunner()
        res = runner.invoke(bulk_update, ['--csv', '/tmp/csv.tmp',
                                          '--query', 'OPTIONAL MATCH (src) CREATE (dest:L {id: row[0], name: row[1]}) CREATE (src)-[:R]->(dest)',
                                          graphname], catch_exceptions=False)

        self.assertEqual(res.exit_code, 0)
        self.assertIn('Labels added: 1', res.output)
        self.assertIn('Nodes created: 3', res.output)
        self.assertIn('Relationships created: 3', res.output)
        self.assertIn('Properties set: 6', res.output)

        tmp_graph = Graph(graphname, self.redis_con)
        query_result = tmp_graph.query('MATCH (a)-[:R]->(b) RETURN a.name, b.name ORDER BY a.name, b.name')

        # Validate that the expected results are all present in the graph
        expected_result = [["a", "b"],
                           ["a", "c"],
                           ["b", "c"]]
        self.assertEqual(query_result.result_set, expected_result)

        # Attempt to re-insert the entities using MERGE.
        res = runner.invoke(bulk_update, ['--csv', '/tmp/csv.tmp',
                                          '--query', 'MERGE (:L {id: row[0], name: row[1]})',
                                          graphname], catch_exceptions=False)
