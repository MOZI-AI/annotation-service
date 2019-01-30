__author__ = "Enku Wendwosen"

import grpc
import time
from concurrent import futures
from service_specs import annotation_pb2, annotation_pb2_grpc
from utils import atomspace_setup
from config import SERVICE_PORT, TEST_FOLDER, PROJECT_ROOT
from core.annotation import annotate
import os
import base64

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def read_file(location):
    with open(location, "rb") as fp:
        content = fp.read()

    return base64.b64encode(content)


class AnnotationService(annotation_pb2_grpc.AnnotateServicer):
    """
    Annotation Service gRPC server that implements annotation RPC function
    """

    def __init__(self, atomspace):
        """
        constructor
        :param atomspace: atomspace that has a loaded list of knowledge bases
        """
        self.atomspace = atomspace

    def Annotate(self, request, context):
        """
        Implements Annnotation gRPC function
        :param request: gRPC request
        :param context: gRPC context
        :return:
        """

        response, file_name = annotate(self.atomspace, request.annotations, request.genes)

        if file_name is None:
            msg = "Invalid Argument `{g}` : Gene Doesn't exist in the Atomspace".format(g=response)
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return annotation_pb2.AnnotationResponse(graph=msg, scm_file="")

        scm_file = read_file(os.path.join(PROJECT_ROOT, file_name))

        os.remove(file_name)
        return annotation_pb2.AnnotationResponse(graph=response, scm=scm_file)


def serve(port):
    """
    Starts a gRPC server that will listen on port
    :param port: a port gRPC server will listen on.
    :return: gRPC server instance
    """
    atomspace = atomspace_setup.load_atomspace()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    annotation_pb2_grpc.add_AnnotateServicer_to_server(AnnotationService(atomspace), server)
    server.add_insecure_port("[::]:{port}".format(port=port))
    return server


if __name__ == '__main__':
    server = serve(SERVICE_PORT)
    server.start()
    print("server started.")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
