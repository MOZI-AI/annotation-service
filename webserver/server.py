import time

__author__ = 'Abdulrahman Semrie<xabush@singularitynet.io> & Enku Wendwosen<enku@singularitynet.io>'

import eventlet
eventlet.monkey_patch()

import os
from models.dbmodels import Session
from flask import Flask, send_file, jsonify
from flask_cors import CORS
import pymongo
from config import MONGODB_URI, DB_NAME, EXPIRY_SPAN, RESULT_DIR,REDIS_URI
from datetime import timedelta
import zipfile
import uuid
import glob
from flask_socketio import SocketIO, emit
from config import setup_logging
import logging

setup_logging()

logger = logging.getLogger("annotation-service")



app = Flask(__name__)
CORS(app)

db = pymongo.MongoClient(MONGODB_URI)[DB_NAME]
sio = SocketIO(app, message_queue=REDIS_URI, cors_allowed_origins="*")

@app.route("/status/<mnemonic>", methods=["GET"])
def get_status(mnemonic):
    session = Session.get_session(db, mnemonic=mnemonic)

    if session:
        if session.status == 2 and not session.expired:
            td = timedelta(days=EXPIRY_SPAN)
            time_to_expire = td.total_seconds() + session.end_time
            return jsonify({"status": session.status, "start_time": session.start_time, "end_time": session.end_time,
                            "annotations": session.annotations, "genes": session.genes,
                            "expire_time": time_to_expire, "status_message": session.message,
                            "csv_files": session.csv_file}), 200
        elif session.expired:
            return jsonify({"response": "Session has expired."}), 400
        elif session.status != 2:
            return jsonify({"response", "Session not finished"}), 401

    else:
        return jsonify({"response": "Session not found"}), 404


@app.route("/<mnemonic>", methods=["GET"])
def send_result(mnemonic):
    path = os.path.join(RESULT_DIR, mnemonic, "{session}.json".format(session=mnemonic))
    if os.path.exists(path):
        return send_file(path, as_attachment=True), 200
    else:
        return jsonify({"response": "File not found"}), 404


@app.route("/result_file/<mnemonic>", methods=["GET"])
def send_result_file(mnemonic):
    session = Session.get_session(db, mnemonic=mnemonic)
    if session:
        if session.status == 2 and not session.expired:
            path = "{result}{id}/*.scm".format(result=RESULT_DIR, id=mnemonic)
            files = glob.glob(path)
            logger.info(files)
            z_path = "{result}{id}/{id}.zip".format(result=RESULT_DIR, id=mnemonic)
            zFile = zipfile.ZipFile(z_path, "w")
            # zFile.write(os.path.join(RESULT_DIR, mnemonic, "{session}.json".format(session=mnemonic)), arcname=mnemonic, compress_type=zipfile.ZIP_STORED)
            for file in files:
                zFile.write(file, arcname=os.path.basename(file),compress_type=zipfile.ZIP_DEFLATED)
            zFile.close()
            return send_file(z_path, as_attachment=True, mimetype="application/x-lisp"), 200
        elif session.expired:
            return jsonify({"response": "Session has expired."}), 400
        elif session.status != 2:
            return jsonify({"response", "Session not finished"}), 401

    else:
        return jsonify({"response": "Session not found"}), 404


@app.route("/csv_file/<mnemonic>/<file_name>", methods=["GET"])
def send_csv_files(mnemonic, file_name):
    path = os.path.join(RESULT_DIR, mnemonic, file_name.lower() + ".csv")
    if os.path.exists(path):
        return send_file(path, as_attachment=True), 200
    else:
        return jsonify({"response": "File not found"}), 404

@sio.on("status")
def status(st):
    logger.info("Received Status" + st)


if __name__ == "__main__":
    sio.run(app, host="0.0.0.0", port="80")
