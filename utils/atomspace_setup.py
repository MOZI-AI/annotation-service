__author__ = "Enku Wendwosen"


from opencog.atomspace import AtomSpace
from opencog.scheme_wrapper import scheme_eval_h
import config
import sys


def load_atomspace():
    """
    loads atomspace with knowledge bases and annotation scheme functions found in scm directory.
    :return: atomspace instance
    """
    atomspace = AtomSpace()
    print("loading atomspace")
    scheme_eval_h(atomspace, '(primitive-load "{}")'.format(config.OPENCOG_DEPS_PATH))
    atomspace = load_functions(atomspace)
    atomspace = load_datasets(atomspace)
    return atomspace


def load_datasets(atomspace):
    """
    loads datasets from scm/datasets directory to atomspace
    :param atomspace: atomspace instance that will be loaded with datasets.
    :return: a loaded atomspace instance
    """
    print("loading datasets")
    if config.PRODUCTION_MODE:
        for dataset in config.DATASET_PATHs:
            print(dataset)
            scheme_eval_h(atomspace, '(primitive-load "{}")'.format(dataset))

        return atomspace
    else:
        print(config.TEST_DATASET)
        scheme_eval_h(atomspace, '(primitive-load "{}")'.format(config.TEST_DATASET))
        return atomspace


def load_functions(atomspace):
    """
    loads annotation functions from scm/functions directory to atomspace
    :param atomspace: atomspace instance taht will be loaded with functions
    :return: a loaded atomspace instance
    """
    print("loading functions")
    for fn in config.FUNCTION_PATHs:
        print(fn)
        scheme_eval_h(atomspace, '(primitive-load "{}")'.format(fn))

    sys.stdout.flush()
    return atomspace
