__author__ = 'Enku Wendwosen<enku@singularitynet.io>'

import unittest
import os
import yaml
from opencog.atomspace import AtomSpace
from core.annotation import annotate
from utils.atomspace_setup import load_atomspace
from service_specs.annotation_pb2 import AnnotationRequest
from unittest.mock import patch
from config import PROJECT_ROOT
from service.annotation_server import parse_payload

class TestCoreAnnotation(unittest.TestCase):

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
        annotate(load_atomspace(), self.multi_req_payload["annotations"],
                          self.multi_req_payload["genes"], "rsrd")
        self.assertTrue(os.path.exists("/tmp/results/rsrd/rsrd.json"))


    def tearDown(self):
        if os.path.exists("/root/result/rsrd"):
            os.removedirs("/root/result/rsrd")

if __name__ == "__main__":
    unittest.main()