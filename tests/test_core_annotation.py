__author__ = 'Enku Wendwosen<enku@singularitynet.io>'

import unittest
import os
import yaml
from core.annotation import annotate, generate_scheme_function
from service_specs.annotation_pb2 import AnnotationRequest
from unittest.mock import patch
from config import PROJECT_ROOT


class TestCoreAnnotation(unittest.TestCase):

    def setUp(self):
        self.single_annotation_request = AnnotationRequest()
        single_annotation_test_file = os.path.join(PROJECT_ROOT, 'tests/data/annotation.test.data.yml')
        with open(os.path.join(PROJECT_ROOT, single_annotation_test_file), 'r') as fb:
            config = yaml.load(fb)
            annotations = config['annotations']
            for a in annotations:
                self.single_annotation_request.annotations.add(
                    functionName=a['annotation']
                )

            genes = config['genes']
            for gene in genes:
                self.single_annotation_request.genes.add(
                    geneName=gene['gene_name']
                )

        self.multiple_annotation_request = AnnotationRequest()
        multiple_annotation_test_file = os.path.join(PROJECT_ROOT, 'tests/data/annotation.test.data.yml')
        with open(os.path.join(PROJECT_ROOT, multiple_annotation_test_file), 'r') as fb:
            config = yaml.load(fb)
            annotations = config['annotations']
            for a in annotations:
                self.multiple_annotation_request.annotations.add(
                    functionName=a['annotation']
                )

            genes = config['genes']
            for gene in genes:
                self.multiple_annotation_request.genes.add(
                    geneName=gene['gene_name']
                )

    @patch('utils.atomspace_setup.load_atomspace')
    @patch('core.annotation.scheme_eval')
    def test_single_annotation(self, scheme_eval, load_atomspace):
        scheme_eval().return_value = "Test Result"
        result = annotate(load_atomspace(), self.single_annotation_request.annotations,
                          self.single_annotation_request.genes)
        self.assertIsNotNone(result)
        self.assertTrue(scheme_eval.called)

    @patch('utils.atomspace_setup.load_atomspace')
    @patch('core.annotation.scheme_eval')
    def test_multiple_annotation(self, scheme_eval, load_atomspace):
        scheme_eval().return_value = "Test Result"
        result = annotate(load_atomspace(), self.multiple_annotation_request.annotations,
                          self.single_annotation_request.genes)
        self.assertIsNotNone(result)
        self.assertTrue(scheme_eval.called)


    def test_generate_scheme_multiple_annotation(self):
        scheme_function = ('(do_annotation (list ( gene_go_annotation )( gene_pathway_annotation )( biogrid_interaction_annotation )))', '(genes \"SLC1A5 SPARC\")')
        result = generate_scheme_function(self.multiple_annotation_request.annotations,
                                                  self.multiple_annotation_request.genes)
        self.assertEqual(result, scheme_function)


if __name__ == "__main__":
    unittest.main()