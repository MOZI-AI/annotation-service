__author__ = 'Enku Wendwosen<enku@singularitynet.io>'

import os
import unittest

import yaml

from opencog.atomspace import AtomSpace
from config import PROJECT_ROOT
from core.annotation import annotate, check_gene_availability
from service.annotation_server import parse_payload
from service_specs.annotation_pb2 import AnnotationRequest
from utils.atomspace_setup import load_atomspace
import json


class TestCoreAnnotation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.atomspace = load_atomspace()

    def setUp(self):
        multiple_annotation_request = AnnotationRequest()
        multiple_annotation_test_file = os.path.join(PROJECT_ROOT, 'tests/data/annotation.test.data.yml')
        with open(os.path.join(PROJECT_ROOT, multiple_annotation_test_file), 'r') as fb:
            config = yaml.load(fb)
            annotations = config['annotations']
            for a in annotations:
                multiple_annotation_request.annotations.add(
                    functionName=a['annotation']
                )

            genes = config['genes']
            for gene in genes:
                multiple_annotation_request.genes.add(
                    geneName=gene['geneName']
                )

        self.multi_req_payload = parse_payload(multiple_annotation_request.annotations, multiple_annotation_request.genes)

    def test_multiple_annotation(self):
        annotate(self.atomspace, self.multi_req_payload["annotations"],
                          self.multi_req_payload["genes"], "rsrd")
        self.assertTrue(os.path.exists("/tmp/results/rsrd/rsrd.json"))


    def test_check_genes(self):
        result, check = check_gene_availability(self.atomspace, [{"gene_name": "NOV"}, {"gene_name" :"IGF1"}, {"gene_name" : "IGF"}])
        self.assertFalse(check)
        self.assertEqual(2, len(json.loads(result)))

    def tearDown(self):
        if os.path.exists("/root/result/rsrd"):
            os.removedirs("/root/result/rsrd")

    @classmethod
    def tearDownClass(cls):
        cls.atomspace = AtomSpace()

if __name__ == "__main__":
    unittest.main()