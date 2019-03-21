import time

__author__ = 'Enku Wendwosen<enku@singularitynet.io>'

import os
from models.dbmodels import Session
from flask import Flask, send_file, jsonify
from flask_cors import CORS
import pymongo
from config import MONGODB_URI, DB_NAME, EXPIRY_SPAN, PROJECT_ROOT
from datetime import timedelta

app = Flask(__name__)
CORS(app)

db = pymongo.MongoClient(MONGODB_URI)[DB_NAME]

@app.route("/status/<mnemonic>", methods=["GET"])
def check_status(mnemonic):


    session = Session.get_session(db, mnemonic=mnemonic)

    if session:
        if session.status == 1:
            return jsonify({"status": session.status, "progress": session.progress, "start_time": session.start_time, "end_time": session.end_time, "message": session.message}), 200

        elif session.status == 2 or session.status == -1:
            td = timedelta(days=EXPIRY_SPAN)
            time_to_expire = td.total_seconds() - (time.time() - session.end_time)
            return jsonify({"status": session.status, "start_time": session.start_time, "end_time": session.end_time, "expire_time": time_to_expire}), 200

    else:
        return jsonify({"response": "Session not found"}), 404


@app.route("/result/<mnemonic>", methods=["GET"])
def send_result(mnemonic):
    session = Session.get_session(db, mnemonic=mnemonic)

    if session:
        if session.status == 2 and not session.expired:
            td = timedelta(days=EXPIRY_SPAN)
            time_to_expire = td.total_seconds() - (time.time() - session.end_time)
            return jsonify({"status": session.status,"start_time": session.start_time, "end_time": session.end_time,"result":session.result,"annotations":session.annotations,"genes":session.genes,"expire_time":time_to_expire,"status_message":session.message}), 200
        elif session.expired:
            return jsonify({"response": "Session has expired."}), 400
        elif session.status != 2:
            return jsonify({"response", "Session not finished"}), 401

    else:
        return jsonify({"response": "Session not found"}), 404

@app.route("/result_file/<mnemonic>",methods=["GET"])
def send_result_file(mnemonic):
    session = Session.get_session(db,mnemonic=mnemonic)

    if session:
        if session.status == 2 and not session.expired:
            return send_file(session.result_file,as_attachment=True), 200
        elif session.expired:
            return jsonify({"response": "Session has expired."}), 400
        elif session.status != 2:
            return jsonify({"response", "Session not finished"}), 401

    else:
        return jsonify({"response": "Session not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")