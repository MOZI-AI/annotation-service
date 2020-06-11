__author__ = "Enku Wendwosen<enku@singularitynet.io> & Abdulrahman Semrie<xabush@singularitynet.io>"

import base64
import json
import logging
import os
import time
import traceback

import pymongo
from opencog.scheme_wrapper import scheme_eval

from config import RESULT_DIR, MONGODB_URI, DB_NAME, setup_logging
from core.annotation import annotate, check_gene_availability
from models.dbmodels import Session
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
    session = Session(id=kwargs["session_id"], mnemonic=kwargs["mnemonic"],
                      annotations=kwargs["payload"]["annotations"], genes=kwargs["payload"]["genes"])
    db = pymongo.MongoClient(MONGODB_URI)[DB_NAME]
    try:
        session.save(db)
        session.status = 1
        session.start_time = time.time()
        session.update_session(db)
        path = os.path.join(RESULT_DIR, session.mnemonic)
        if not os.path.exists(path):
            os.makedirs(path)

        annotate(atomspace, kwargs["payload"]["annotations"], kwargs["payload"]["genes"],
                                       session.mnemonic)
        logger.info("when executing atoms:" + scheme_eval(atomspace, "(count-all)").decode("utf-8"))
        scm_dir = "/root/result/{session}".format(session=session.mnemonic)
        json_file = "/root/result/{session}/{session}.json".format(session=session.mnemonic)
        logger.info("Result dir: " + scm_dir)
        session.status = 2
        session.result = json_file
        logger.info("Applying Multi-level Layout")
        out_dict = multi_level_layout(json_file)
        with open(json_file, "w") as fp:
            json.dump({"elements": out_dict}, fp)
        session.results_file = scm_dir
        csv_file = to_csv(session.mnemonic)
        logger.info(csv_file)
        session.csv_file = csv_file
        session.update_session(db)
        return True

    except Exception as ex:
        msg = "Error: " + ex.__str__()
        session.status = -1
        session.update_session(db)
        session.message = msg
        logger.error(msg)
        traceback.print_exc()
        return False

    finally:
        session.end_time = time.time()
        session.update_session(db)

