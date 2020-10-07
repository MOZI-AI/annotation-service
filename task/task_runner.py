__author__ = "Enku Wendwosen<enku@singularitynet.io> & Abdulrahman Semrie<xabush@singularitynet.io>"

import base64
import json
import logging
import os
import traceback

from opencog.scheme import scheme_eval

from config import RESULT_DIR, setup_logging
from core.annotation import annotate, check_gene_availability
from utils.multi_level import multi_level_layout
from utils.scm2csv.scm2csv import to_csv
from utils.atomspace_setup import load_atomspace
from ann_graph import GraphProcessor

setup_logging()


atomspace = load_atomspace()

def read_file(location):
    with open(location, "rb") as fp:
        content = fp.read()

    return base64.b64encode(content)

def check_genes(**kwargs):
    return check_gene_availability(atomspace , kwargs["payload"]["genes"])

def start_annotation(**kwargs):
    logger = logging.getLogger("annotation-service")

    try:
        mnemonic  = kwargs["mnemonic"]
        path = os.path.join(RESULT_DIR, mnemonic)
        if not os.path.exists(path):
            os.makedirs(path)

        response = annotate(atomspace, kwargs["payload"]["annotations"], kwargs["payload"]["genes"],
                                       mnemonic)
        if "#f" in response:
            not_found = response[4:].split(" ")
            res = []
            for n in not_found:
                res.append({"symbol": n, "current": "", "similar": ""})
            return False, json.dumps(res)
        else:

            logger.info("when executing atoms:" + scheme_eval(atomspace, "(count-all)").decode("utf-8"))
            json_file = os.path.join(path, mnemonic + ".json")
            logger.info("Applying Multi-level Layout")
            graph_processor = GraphProcessor(json_file)
            graph_processor.process()
            csv_file = to_csv(mnemonic)
            logger.info(csv_file)
            return True, None

    except Exception as ex:
        msg = "Error: " + ex.__str__()
        logger.error(msg)
        print(traceback._cause_message)
        return False, msg

