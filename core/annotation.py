__author__ = "Enku Wendwosen"

from opencog.scheme_wrapper import scheme_eval
import logging

def generate_annotate_function(annotations, genes_list):
    """
    Generates scheme functions by concatenating annotations and genes
    :param annotations: a list containing annotations
    :param genes: a list containing genes
    :return: a concatenated string which is a scheme function containing the list of genes and annotations.
    """

    annotations_comp = '(list '
    for a in annotations:
        if not (a["filters"] is None):
            filters = ""
            for f in a["filters"]:
                if f["filter"] == 'parents':
                    filters += f["value"]
                else:
                    filters += ' \"' + f["value"] + '\" '
            annotations_comp += '( {fn_name} {genes} {filters})'.format(fn_name=a["function_name"], genes=genes_list,  filters=filters)
        else:
            annotations_comp += '( {fn_name} {genes})'.format(fn_name=a.functionName, genes=genes_list)
    annotations_comp += ')'
    scheme_function = '(define result (append (list (gene-info (mapSymbol {genes}))) {annotation_fns}))'.format(genes=genes_list, annotation_fns=annotations_comp)
    #scheme_function = '(do_annotation {fns})'.format(fns=annotations_comp)
    return scheme_function

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
    genes_fn = "(genes {gene_list})".format(gene_list=genes)
    gene_result = scheme_eval(atomspace, genes_fn).decode('utf-8')
    logger.warning("result : " + gene_result[0])

    if int(gene_result[0]) == 1:
        return gene_result[2:], False

    return gene_result, True


def annotate(atomspace, annotations, genes):
    """
    Performs annotation according to a list of annotations given on a list of genes
    :param atomspace: the atomspace that contains the loaded knowledge bases where the annotations will be performed from
    :param annotations: a list of annotations
    :param genes: a list of genes.
    :return: a string response directly from the scheme_eval response decoded in utf-8
    """
    logger = logging.getLogger("annotation-service")
    genes_list = generate_gene_function(genes)
    scheme_function = generate_annotate_function(annotations, genes_list)
    logger.info("Scheme Func: " + scheme_function)
    scheme_eval(atomspace, scheme_function)
    parse_function = "(parse result {genes_list})".format(genes_list=genes_list) 
    logger.info("doing annotation " + parse_function)
    response = scheme_eval(atomspace, parse_function).decode("utf-8")
    logger.info(response)
    file_name = scheme_eval(atomspace, "(write-to-file)").decode("utf-8").rstrip()
    logger.warning("saving result in file : " + file_name)

    return response, file_name
