__author__ = "Abdulrahman Semrie<xabush@singularitynet.io> & Enku Wendwosen<enku@singularitynet.io>"

from config import CELERY_OPTS, RESULT_DIR, REDIS_URI, MONGODB_URI, DB_NAME, setup_logging
from celery import Celery, current_app
from core.annotation import annotate, check_gene_availability
from utils.atomspace_setup import load_atomspace
import logging
import base64
import os
import pymongo
import time
from models.dbmodels import Session
from utils.scm2csv.scm2csv import to_csv
from opencog.scheme_wrapper import scheme_eval
from flask_socketio import SocketIO, emit

celery = Celery('annotation_snet', broker=CELERY_OPTS["CELERY_BROKER_URL"])


celery.conf.update(CELERY_OPTS)
setup_logging()


logger = logging.getLogger("annotation-service")


def read_file(location):
    with open(location, "rb") as fp:
        content = fp.read()

    return base64.b64encode(content)


@celery.task(name="task.task_runner.check_genes")
def check_genes(**kwargs):
    response, check = check_gene_availability(atomspace, kwargs["payload"]["genes"])
    if check:
        sio.emit("checkgenes", None)
        current_app.send_task("task.task_runner.start_annotation", kwargs=kwargs)

    else:
        sio.emit("checkgenes", response)


@celery.task(name="task.task_runner.start_annotation")
def start_annotation(**kwargs):
    logger.info("Starting Annotation")
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
        logger.info("when executing atoms:" + scheme_eval(atomspace, "(count-all)").decode("utf-8"))
        response, file_name = annotate(atomspace, kwargs["payload"]["annotations"], kwargs["payload"]["genes"],
                                       session.mnemonic)
        logger.info("Filename: " + file_name)
        if file_name is None:
            logger.warning("The following genes were not found in the atomspace %s", response)
            msg = "Invalid Argument `{g}` : Gene Doesn't exist in the Atomspace".format(g=response)
            raise ValueError(msg)
        session.status = 2
        file = os.path.join(path, "{session}.json".format(session=session.mnemonic))
        with open(file, "w") as f:
            f.write(response)
        session.result = file
        session.results_file = file_name
        csv_file = to_csv(session.mnemonic)
        logger.info(csv_file)
        session.csv_file = csv_file
        session.update_session(db)
        return True

    except Exception as ex:
        msg = "Error: " + ex.__str__()
        session.status = -1
        session.message = msg
        logger.error(msg)
        return False

    finally:
        session.end_time = time.time()
        session.update_session(db)
        sio.emit("status", session.mnemonic)


if __name__ == "__main__":
    sio = SocketIO(message_queue=REDIS_URI, async_mode="threading")
    atomspace = load_atomspace()
    argv = [
        'worker',
        '--loglevel=INFO',
    ]
    celery.worker_main(argv)
    logger.info("Celery started!")
