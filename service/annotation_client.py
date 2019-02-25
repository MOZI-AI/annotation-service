import grpc
import sys
import yaml
import os
import service_specs.annotation_pb2 as annotation_pb2
import service_specs.annotation_pb2_grpc as annotation_pb2_grpc
from config import PROJECT_ROOT,SERVICE_PORT, SERVICE_URL


def run(stub, annotation_file):
    """
    Sends an annotation request to gRPC server by reading annotations and genes from annotation_file
    :param stub: a gRPC client stub
    :param annotation_file: a yml file that contains a list of annotations and genes
    :return: a string response which will be scheme.
    """
    request = annotation_pb2.AnnotationRequest()
    with open(os.path.join(PROJECT_ROOT, annotation_file), 'r') as fb:
        config = yaml.load(fb)
        annotations = config['annotations']
        for a in annotations:
            annotation = annotation_pb2.Annotation()
            annotation.functionName = a["annotation"]
            if 'filters' in a:
                for f in a['filters']:
                    annotation.filters.add(
                        filter=f['filter'],
                        value=f['value']
                    )

            request.annotations.extend(
                [annotation]
            )

        for gene in config['genes']:
            request.genes.add(
                geneName=gene['geneName']
            )
        return stub.Annotate(request)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        annotation_yml = sys.argv[1]
        channel = grpc.insecure_channel('{url}:{port}'.format(url=SERVICE_URL, port=SERVICE_PORT))
        stub = annotation_pb2_grpc.AnnotateStub(channel)
        res = run(stub, annotation_yml)
        print(res)
    else:
        print('Please provide an Annotation configuration file.')