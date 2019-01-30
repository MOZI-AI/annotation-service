import os
import unittest
from unittest.mock import patch

import grpc

from config import SERVICE_URL, SERVICE_PORT, PROJECT_ROOT
from service.annotation_client import run
from service.annotation_server import serve
from service_specs.annotation_pb2_grpc import AnnotateStub

patcher = patch("service.annotation_server.load_atomspace")


class TestAnnotationServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        patcher.start()
        cls.server = serve(SERVICE_PORT)
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop(0)
        patcher.stop()

    def setUp(self):
        self.channel = grpc.insecure_channel('{url}:{port}'.format(url=SERVICE_URL, port=SERVICE_PORT))
        self.stub = AnnotateStub(self.channel)
        self.test_annotation_file = os.path.join(PROJECT_ROOT, 'tests/data/annotation.test.data.yml')

    def tearDown(self):
        pass

    @patch('service.annotation_server.annotate')
    def test_annotation(self, annotate):
        annotate().return_value = '(scheme)'
        response = run(self.stub, self.test_annotation_file)
        self.assertEqual(response.graph, '(scheme)')


if __name__ == "__main__":
    unittest.main()
