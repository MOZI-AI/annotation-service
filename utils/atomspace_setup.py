__author__ = "Enku Wendwosen & Abdulrahman Semrie"

import logging
from opencog.atomspace import AtomSpace
from opencog.scheme_wrapper import scheme_eval

import config

logger = logging.getLogger("annotation-service")


def load_atomspace():
    """
    loads atomspace with knowledge bases and annotation scheme functions found in scm directory.
    :return: atomspace instance
    """
    atomspace = AtomSpace()
    scheme_eval(atomspace, '(primitive-load "{}")'.format(config.OPENCOG_DEPS_PATH))
    return atomspace


def load_datasets(atomspace):
    """
    loads datasets from scm/datasets directory to atomspace
    :param atomspace: atomspace instance that will be loaded with datasets.
    :return: a loaded atomspace instance
    """
    logger.info("Loading datasets")

    logger.info("In Production Mode")
    for dataset in config.DATASET_PATHs:
        scheme_eval(atomspace, '(load-file "{}")'.format(dataset))

    return atomspace

def apply_pln(atomspace):
    """
    Apply PLN rules to get rid of outdated gene symbols and create a link to the current ones.
    :param atomspace: atomspace instance that a PLN rules will be applied.
    :return: an atomspace instance enriched with additional links 
    """
    logger.info("Applying PLN rules")
    scheme_eval(atomspace, '(primitive-load "{}")'.format(config.PLN_RULE))
    return atomspace