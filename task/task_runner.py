__author__ = "Enku Wendwosen<enku@singularitynet.io>"

from config import CELERY_OPTS,REDIS_URI, PROJECT_ROOT,MONGODB_URI, DB_NAME, setup_logging
from celery import Celery, current_app
from celery.bin import worker
from core.annotation import annotate , check_gene_availability
from utils.atomspace_setup import load_atomspace
import logging
import base64
import os
import pymongo
import time
from models.dbmodels import Session
from utils.scm2csv.scm2csv import to_csv
from opencog.scheme_wrapper import scheme_eval

# celery = Celery('annotation_snet',broker=CELERY_OPTS["CELERY_BROKER_URL"])
atomspace = load_atomspace()
# celery.conf.update(CELERY_OPTS)
setup_logging()
# sio = socketio.RedisManager(REDIS_URI, write_only=True)

def read_file(location):
    with open(location, "rb") as fp:
        content = fp.read()

    return base64.b64encode(content)

# @celery.task(name="task.task_runner.check_genes")
def check_genes(**kwargs):
    logger = logging.getLogger("annotation-service")
    return check_gene_availability(atomspace , kwargs["payload"]["genes"])


# @celery.task(name="task.task_runner.start_annotation")
def start_annotation(**kwargs):
    logger = logging.getLogger("annotation-service")
    db = pymongo.MongoClient(MONGODB_URI)[DB_NAME]
    session = Session(id=kwargs["session_id"],mnemonic=kwargs["mnemonic"],annotations=kwargs["payload"]["annotations"],genes=kwargs["payload"]["genes"])
    session.save(db)
    session.status = 1
    session.start_time = time.time()
    session.update_session(db)
    logger.warning("when executing atoms:" +scheme_eval(atomspace,"(count-all)").decode("utf-8"))
    response, file_name = annotate(atomspace, kwargs["payload"]["annotations"], kwargs["payload"]["genes"])
    logger.info("Filename: " + file_name)
    if file_name is None:
        logger.warning("The following genes were not found in the atomspace %s", response)
        msg = "Invalid Argument `{g}` : Gene Doesn't exist in the Atomspace".format(g=response)
        raise ValueError(msg)
    try:
        scm_file = os.path.join(PROJECT_ROOT,file_name)
        # TODO: Implement file cleanup
        # os.remove(os.path.join(PROJECT_ROOT, file_name))
        session.status = 2
        session.result = response
        session.result_file = scm_file
        #csv_file = to_csv(scm_file)
        #logger.warning(csv_file)
        #session.csv_file = csv_file
        session.update_session(db)
        return True

    except Exception as ex:
        msg = "Error: " + str(ex.__traceback__)
        session.status = -1
        session.update_session(db)
        session.message = msg
        logger.error(msg)
        return False

    finally:
        session.end_time = time.time()
        session.update_session(db)
