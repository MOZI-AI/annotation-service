__author__ = "Enku Wendwosen"

from opencog.scheme_wrapper import scheme_eval
import logging
import json
from array import array


def generate_gene_function(genes):
    genes_comp = '(list '
    for gene in genes:
        genes_comp += '"{gene}" '.format(gene=gene["gene_name"])
    genes_comp += ')'
    return genes_comp


def check_gene_availability(atomspace, genes):
    logger = logging.getLogger("annotation-service")
    genes = generate_gene_function(genes)
    logger.info("checking genes : " + genes)
    logger.info(genes)
    genes_fn = "(find-genes {gene_list})".format(gene_list=genes)
    gene_result = scheme_eval(atomspace, genes_fn).decode('utf-8')
    logger.warning("result : " + gene_result[0])

    if int(gene_result[0]) == 1:
        return gene_result[2:], False

    return gene_result, True


def convert_to_byte_str(s):
    arr = array('b')
    arr.frombytes(s.encode())
    ls = " ".join(str(x) for x in arr)
    return "'({0})".format(ls)


def annotate(atomspace, annotations, genes, session_id):
    """
    Performs annotation according to a list of annotations given on a list of genes
    :param atomspace: the atomspace that contains the loaded knowledge bases where the annotations will be performed from
    :param annotations: a list of annotations
    :param genes: a list of genes.
    :return: a string response directly from the scheme_eval response decoded in utf-8
    """
    logger = logging.getLogger("annotation-service")
    genes_list = generate_gene_function(genes)
    parse_function = "(annotate-genes {genes} \"{session}\" {request})".format(
        genes=genes_list, request=convert_to_byte_str(json.dumps(annotations)), session=session_id)
    response = scheme_eval(atomspace, parse_function).decode("utf-8")
    file_name = "/root/result/{session}/{session}.scm".format(session=session_id)
    logger.info("saving result in file : " + file_name)
    return response, file_name
