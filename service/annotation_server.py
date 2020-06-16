__author__ = "Abdulrahman Semrie<xabush@singularitynet.io & Enku Wendwosen<enku@singularitynet.io>"

import base64
import logging
import multiprocessing
import traceback
import uuid
from concurrent import futures

import grpc

from config import setup_logging, MOZI_RESULT_URI
from service_specs import annotation_pb2, annotation_pb2_grpc
from task.task_runner import start_annotation, check_genes
from utils.atomspace_setup import load_atomspace
from utils.url_encoder import encode

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PROCESS_COUNT = multiprocessing.cpu_count()
_THREAD_CONCURRENCY = _PROCESS_COUNT


def read_file(location):
    with open(location, "rb") as fp:
        content = fp.read()

    return base64.b64encode(content)


def parse_payload(annotations, genes):
    annotation_payload = []
    for a in annotations:
        annotation = dict()
        annotation["functionName"] = a.functionName
        if not (a.filters is None):
            filters = []
            for f in a.filters:
                filters.append({"filter": f.filter, "value": f.value})

            annotation["filters"] = filters
            annotation_payload.append(annotation)
    genes_payload = []
    for g in genes:
        genes_payload.append({"gene_name": g.geneName})

    return {"annotations": annotation_payload, "genes": genes_payload}


class AnnotationService(annotation_pb2_grpc.AnnotateServicer):
    """
    Annotation Service gRPC server that implements annotation RPC function
    """
    logger = logging.getLogger("annotation-service")

    def __init__(self):
        """
        constructor
        :param atomspace: atomspace that has a loaded list of knowledge bases
        """
        # self.atomspace = atomspace

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
            atomspace = load_atomspace()
            payload = parse_payload(request.annotations, request.genes)
            response, check = check_genes(atomspace, payload=payload)
            self.logger.warning(response)

            if check:
                response = start_annotation(atomspace, session_id=session_id, mnemonic=mnemonic, payload=payload)
                if response:
                    url = "{MOZI_RESULT_URI}/?id={mnemonic}".format(MOZI_RESULT_URI=MOZI_RESULT_URI, mnemonic=mnemonic)
                    return annotation_pb2.AnnotationResponse(result=url)
                else:
                    msg = "an internal error occured. please try again"
                    context.set_details(msg)
                    context.set_code(grpc.StatusCode.INTERNAL)
                    return annotation_pb2.AnnotationResponse(result=msg)
            else:
                self.logger.warning("The following genes were not found in the atomspace %s", response)
                context.set_details(response)
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return annotation_pb2.AnnotationResponse(result=response)

        except Exception as ex:
            self.logger.exception(traceback.format_exc())
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Error occurred in while trying to perform request: " + ex.__str__())
            return annotation_pb2.AnnotationResponse(result="url")


def _run_server(bind_address):
    """Start a server in a subprocess"""
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=_THREAD_CONCURRENCY)
    )
    annotation_pb2_grpc.add_AnnotateServicer_to_server(AnnotationService(), server)
    server.add_insecure_port(bind_address)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    setup_logging()
    _run_server("[::]:3000")
