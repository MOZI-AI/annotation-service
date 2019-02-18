import os
import unittest
from unittest.mock import patch, MagicMock

import grpc
from config import SERVICE_URL, SERVICE_PORT, PROJECT_ROOT
from service.annotation_client import run
from service.annotation_server import serve
from service_specs.annotation_pb2_grpc import AnnotateStub

class TestAnnotationServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = serve(None, SERVICE_PORT)
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop(0)

    def setUp(self):
        self.channel = grpc.insecure_channel('{url}:{port}'.format(url=SERVICE_URL, port=SERVICE_PORT))
        self.stub = AnnotateStub(self.channel)
        self.test_annotation_file = os.path.join(PROJECT_ROOT, 'tests/data/annotation.test.data.yml')
        self.test_file = "test_file"
        open(os.path.join(PROJECT_ROOT,self.test_file),'w')

    def tearDown(self):
        pass

    def test_annotation(self):
        with patch('service.annotation_server.annotate', return_value=('(scheme)', self.test_file)):
            response = run(self.stub, self.test_annotation_file)
            self.assertEqual(response.graph, "(scheme)")


if __name__ == "__main__":
    unittest.main()
