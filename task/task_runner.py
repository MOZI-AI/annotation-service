__author__ = "Enku Wendwosen<enku@singularitynet.io> & Abdulrahman Semrie<xabush@singularitynet.io>"

import base64
import json
import logging
import os
import traceback

from opencog.scheme_wrapper import scheme_eval

from config import RESULT_DIR, setup_logging
from core.annotation import annotate, check_gene_availability
from utils.multi_level import multi_level_layout
from utils.scm2csv.scm2csv import to_csv

setup_logging()


def read_file(location):
    with open(location, "rb") as fp:
        content = fp.read()

    return base64.b64encode(content)

def check_genes(atomspace, **kwargs):
    return check_gene_availability(atomspace , kwargs["payload"]["genes"])

def start_annotation(atomspace, **kwargs):
    logger = logging.getLogger("annotation-service")

    try:
        mnemonic = mnemonic = kwargs["mnemonic"]
        path = os.path.join(RESULT_DIR, mnemonic)
        if not os.path.exists(path):
            os.makedirs(path)

        annotate(atomspace, kwargs["payload"]["annotations"], kwargs["payload"]["genes"],
                                       mnemonic)
        logger.info("when executing atoms:" + scheme_eval(atomspace, "(count-all)").decode("utf-8"))
        scm_dir = "/root/result/{session}".format(session=mnemonic)
        json_file = "/root/result/{session}/{session}.json".format(session=mnemonic)
        logger.info("Result dir: " + scm_dir)
        logger.info("Applying Multi-level Layout")
        out_dict = multi_level_layout(json_file)
        with open(json_file, "w") as fp:
            json.dump({"elements": out_dict}, fp)
        csv_file = to_csv(mnemonic)
        logger.info(csv_file)
        return True

    except Exception as ex:
        msg = "Error: " + ex.__str__()
        logger.error(msg)
        traceback.print_exc()
        return False

