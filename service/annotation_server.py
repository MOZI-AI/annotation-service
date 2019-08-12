__author__ = "Enku Wendwosen<enku@singularitynet.io>"

import base64
import logging
import time
import uuid
from concurrent import futures
import contextlib
import multiprocessing
import socket

import grpc
import os

import grpc
from service_specs import annotation_pb2, annotation_pb2_grpc

from config import SERVICE_PORT, setup_logging, MOZI_RESULT_URI
from task.task_runner import start_annotation, check_genes
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
        annotation["function_name"] = a.functionName
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
            pid = os.getpid()
            logger.info("Current PID: " + str(pid))
            payload = parse_payload(request.annotations, request.genes)
            response, check = check_genes(payload=payload)
            self.logger.warning(response)

            if check:
                response = start_annotation(session_id=session_id, mnemonic=mnemonic, payload=payload)
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
                msg = "Invalid Argument `{g}` : Gene Doesn't exist in the Atomspace".format(g=response)
                context.set_details(msg)
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return annotation_pb2.AnnotationResponse(result=msg)

        except Exception as ex:
            logger.error("Error: " + str(ex.__traceback__))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Error occurred in while trying to perform request: " + ex.__str__())
            return annotation_pb2.AnnotationResponse(result="url")


def _wait_forever(server):
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(None)


@contextlib.contextmanager
def _reserve_port():
    """Find and reserve a port for all subprocesses to use."""
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
        raise RuntimeError("Failed to set SO_REUSEPORT.")
    sock.bind(('', int(SERVICE_PORT)))
    try:
        yield sock.getsockname()[1]
    finally:
        sock.close()


def _run_server(bind_address):
    """Start a server in a subprocess"""
    options = (("grpc.so_reuseport", 1),)
    # WARNING: This example takes advantage of SO_REUSEPORT. Due to the
    # limitations of manylinux1, none of our precompiled Linux wheels currently
    # support this option. (https://github.com/grpc/grpc/issues/18210). To take
    # advantage of this feature, install from source with
    # `pip install grpcio --no-binary grpcio`.

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=_THREAD_CONCURRENCY),
        options=options
    )
    annotation_pb2_grpc.add_AnnotateServicer_to_server(AnnotationService(), server)
    server.add_insecure_port(bind_address)
    server.start()
    _wait_forever(server)


if __name__ == '__main__':
    setup_logging()
    with _reserve_port() as port:
        address = "0.0.0.0:{}".format(port)
        workers = []
        for _ in range(_PROCESS_COUNT):
            worker = multiprocessing.Process(
                target=_run_server, args=(address,)
            )
            worker.start()
            workers.append(workers)

        for worker in workers:
            worker.join()
