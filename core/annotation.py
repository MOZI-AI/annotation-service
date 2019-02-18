__author__ = "Enku Wendwosen"

from opencog.scheme_wrapper import scheme_eval


def generate_scheme_function(annotations, genes):

    """
    Generates scheme functions by concatenating annotations and genes
    :param annotations: a list containing annotations
    :param genes: a list containing genes
    :return: a concatenated string which is a scheme function containing the list of genes and annotations.
    """

    annotations_comp = '(list '
    for a in annotations:
        if not (a.filters is None):
            filters = ""
            for f in a.filters:
                if f.filter == 'parents':
                    filters += f.value
                else:
                    filters += ' \"' + f.value + '\" '
            annotations_comp += '( {fn_name} {filters})'.format(fn_name=a.functionName,filters=filters)
        else:
            annotations_comp += '( {fn_name} )'.format(fn_name=a.functionName)
    annotations_comp += ')'

    genes_comp = '(genes "'
    for gene in genes:
        genes_comp += '{gene}'.format(gene=gene.geneName) if genes_comp == '(genes "' else ' {gene}'.format(gene=gene.geneName)
    genes_comp += '")'
    scheme_function = '(do_annotation {fns})'.format(fns=annotations_comp)

    return scheme_function, genes_comp


def annotate(atomspace, annotations, genes):
    """
    Performs annotation according to a list of annotations given on a list of genes
    :param atomspace: the atomspace that contains the loaded knowledge bases where the annotations will be performed from
    :param annotations: a list of annotations
    :param genes: a list of genes.
    :return: a string response directly from the scheme_eval response decoded in utf-8
    """
    scheme_function, genes = generate_scheme_function(annotations, genes)
    gene_result = scheme_eval(atomspace, genes).decode('utf-8')
    print(gene_result)

    if int(gene_result[0]) == 1:
        return gene_result[2:], None

    print("doing annotation " + scheme_function)
    response = scheme_eval(atomspace, scheme_function).decode('utf-8')
    file_name = scheme_eval(atomspace, "(write-to-file)").decode("utf-8").rstrip()
    print("saving result in file : " + file_name)

    return response, file_name
