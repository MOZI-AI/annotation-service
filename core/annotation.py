__author__ = "Abdulrahman Semrie & Enku Wendwosen"

from opencog.scheme_wrapper import scheme_eval
import logging
import json
from config import RESULT_DIR


def generate_gene_function(genes):
    genes_comp = '(list '
    for gene in genes:
        genes_comp += '"{gene}" '.format(gene=gene["geneName"])
    genes_comp += ')'
    return genes_comp


def check_gene_availability(atomspace, genes):
    logger = logging.getLogger("annotation-service")
    genes = generate_gene_function(genes)
    logger.info("checking genes : " + genes)
    logger.info(genes)
    genes_fn = "(find-genes {gene_list})".format(gene_list=genes)
    gene_result = scheme_eval(atomspace, genes_fn).decode('utf-8')
    gene_dict = json.loads(gene_result)
    return gene_result, len(gene_dict) == 0


def annotate(atomspace, annotations, genes, mnemonic):
    """
    Performs annotation according to a list of annotations given on a list of genes
    :param atomspace: the atomspace that contains the loaded knowledge bases where the annotations will be performed from
    :param annotations: a list of annotations
    :param genes: a list of genes.
    :return: a string response directly from the scheme_eval response decoded in utf-8
    """
    logger = logging.getLogger("annotation-service")
    logger.info(annotations)
    genes_list = generate_gene_function(genes)
    parse_function = "(annotate-genes {genes} \"{session}\" \"{request}\")".format(
        genes=genes_list, request=json.dumps(annotations).replace('"', '\\"'), session=mnemonic)
    logger.info(parse_function)
    scheme_eval(atomspace, parse_function).decode("utf-8")
    logger.info("Finished annotation")
