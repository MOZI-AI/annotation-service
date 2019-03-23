__author__ = "Enku Wendwosen<enku@singularitynet.io>"

import grpc
import time
from concurrent import futures
from service_specs import annotation_pb2, annotation_pb2_grpc
from utils.atomspace_setup import load_atomspace
from config import SERVICE_PORT, setup_logging, PROJECT_ROOT , MOZI_URI
from task.task_runner import start_annotation,check_genes
from utils.url_encoder import encode
from core.annotation import annotate
import os
import base64
import logging
import uuid
_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def read_file(location):
    with open(location, "rb") as fp:
        content = fp.read()

    return base64.b64encode(content)

def parse_payload(annotations,genes):
    annotation_payload = []
    for a in annotations:
        annotation = dict()
        annotation["function_name"] =  a.functionName
        if not (a.filters is None):
            filters = []
            for f in a.filters:
                filters.append({"filter":f.filter,"value":f.value})

            annotation["filters"] = filters
            annotation_payload.append(annotation)
    genes_payload = []
    for g in genes:
        genes_payload.append({"gene_name" : g.geneName})

    return { "annotations" : annotation_payload, "genes" : genes_payload }



class AnnotationService(annotation_pb2_grpc.AnnotateServicer):
    """
    Annotation Service gRPC server that implements annotation RPC function
    """
    logger = logging.getLogger("annotation-service")

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

        session_id = uuid.uuid4()
        mnemonic = encode(session_id)

        try:
            # TODO: Implement a separate EAGER task for checking genes
            payload = parse_payload(request.annotations, request.genes)
            response , check = check_genes(payload = payload)

            if check:
                start_annotation.delay(session_id = session_id, mnemonic= mnemonic, payload = payload)
                url = "{MOZI_URL}/result?id={mnemonic}".format(MOZI_URL=MOZI_URI,mnemonic=mnemonic)
                return annotation_pb2.AnnotationResponse(result=url)
            else:
                self.logger.warning("The following genes were not found in the atomspace %s", response)
                msg = "Invalid Argument `{g}` : Gene Doesn't exist in the Atomspace".format(g=response)
                context.set_details(msg)
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return annotation_pb2.AnnotationResponse(graph=msg, scm_file="")

        except Exception as ex:
            logger.error("Error: " + str(ex.__traceback__))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Error occurred in while trying to perform request: " + ex.__str__())
            return annotation_pb2.AnnotationResponse(result="url")

        # try:
        #     response, file_name = annotate(self.atomspace, request.annotations, request.genes)
        #
        #     if file_name is None:
        #         self.logger.warning("The following genes were not found in the atomspace %s", response)
        #         msg = "Invalid Argument `{g}` : Gene Doesn't exist in the Atomspace".format(g=response)
        #         context.set_details(msg)
        #         context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        #         return annotation_pb2.AnnotationResponse(graph=msg, scm_file="")
        #
        #     scm_file = read_file(os.path.join(PROJECT_ROOT, file_name))
        #     os.remove(os.path.join(PROJECT_ROOT, file_name))
        #     return annotation_pb2.AnnotationResponse(graph=response, scm=scm_file)
        #
        # except Exception as ex:
        #     logger.error("Error: " + str(ex.__traceback__))
        #     context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        #     context.set_details("Error occurred in while trying to perform request: " + ex.__str__())
        #     return annotation_pb2.AnnotationResponse(graph="", scm="")


def serve(atomspace, port):
    """
    Starts a gRPC server that will listen on port
    :param atomspace: The loaded atomspace
    :param port: a port gRPC server will listen on.
    :return: gRPC server instance
    """
    logger = logging.getLogger("annotation-service")
    logger.info("Starting up the Server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    annotation_pb2_grpc.add_AnnotateServicer_to_server(AnnotationService(atomspace), server)
    server.add_insecure_port("[::]:{port}".format(port=port))
    return server


if __name__ == '__main__':
    setup_logging()
    atomspace = load_atomspace()
    logger = logging.getLogger("annotation-service")
    logger.info("Starting up the Server")
    server = serve(atomspace, SERVICE_PORT)
    server.start()
    logger.info("Server started.")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
        logger.info("Stopping Server...")
