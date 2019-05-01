__author__ = "Enku Wendwosen & Abdulrahman Semrie"

import logging
from opencog.atomspace import AtomSpace
from opencog.scheme_wrapper import scheme_eval_h, scheme_eval
import config

logger = logging.getLogger("annotation-service")


def load_atomspace():
    """
    loads atomspace with knowledge bases and annotation scheme functions found in scm directory.
    :return: atomspace instance
    """
    atomspace = AtomSpace()
    logger.info("Loading Atoms")
    print("loading atoms")
    scheme_eval_h(atomspace, '(primitive-load "{}")'.format(config.OPENCOG_DEPS_PATH))
    print("initial atoms:" + scheme_eval(atomspace, "(count-all)").decode("utf-8"))
    atomspace = load_functions(atomspace)
    print("after functions atoms:" +scheme_eval(atomspace, "(count-all)").decode("utf-8"))
    atomspace = load_datasets(atomspace)
    print("after datasets:" +scheme_eval(atomspace, "(count-all)").decode("utf-8"))
    print("done")
    logger.info("Atoms loaded!")
    return atomspace


def load_datasets(atomspace):
    """
    loads datasets from scm/datasets directory to atomspace
    :param atomspace: atomspace instance that will be loaded with datasets.
    :return: a loaded atomspace instance
    """
    logger.info("Loading datasets")
    if config.PRODUCTION_MODE:
        logger.info("In Production Mode")
        for dataset in config.DATASET_PATHs:
            scheme_eval_h(atomspace, '(primitive-load "{}")'.format(dataset))

        return atomspace
    else:
        logger.info("In Dev Mode")
        scheme_eval_h(atomspace, '(primitive-load "{}")'.format(config.TEST_DATASET))
        return atomspace


def load_functions(atomspace):
    """
    loads annotation functions from scm/functions directory to atomspace
    :param atomspace: atomspace instance taht will be loaded with functions
    :return: a loaded atomspace instance
    """
    logger.info("loading helper functions")
    for fn in config.HELPER_PATHs:
        scheme_eval_h(atomspace, '(primitive-load "{}")'.format(fn))

    logger.info("loading functions")
    for fn in config.FUNCTION_PATHs:
        scheme_eval_h(atomspace, '(primitive-load "{}")'.format(fn))

    return atomspace
