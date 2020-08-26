__author__ = 'Abdulrahman Semrie<xabush@singularitynet.io> & Enku Wendwosen<enku@singularitynet.io>'

import glob
import json
import logging
import os
import zipfile

from flask import Flask, send_file, jsonify
from flask_cors import CORS

from config import RESULT_DIR
from config import setup_logging

setup_logging()

logger = logging.getLogger("annotation-service")



app = Flask(__name__)
CORS(app)

csv_dict = {"gene-go.csv": "GO", "gene-pathway.csv": "PATHWAY", "biogrid.csv" : "BIOGRID", "rna.csv": "RNA"}

@app.route("/<mnemonic>", methods=["GET"])
def send_result(mnemonic):
    path = os.path.join(RESULT_DIR, mnemonic, "{session}.json".format(session=mnemonic))
    if os.path.exists(path):
        return send_file(path, as_attachment=True), 200
    else:
        return jsonify({"response": "File not found"}), 404


@app.route("/result_file/<mnemonic>", methods=["GET"])
def send_result_file(mnemonic):
    path = "{result}/{id}/*.scm".format(result=RESULT_DIR, id=mnemonic)
    files = glob.glob(path)
    logger.info(files)
    z_path = "{result}/{id}/{id}.zip".format(result=RESULT_DIR, id=mnemonic)
    zFile = zipfile.ZipFile(z_path, "w")
    for file in files:
        zFile.write(file, arcname=os.path.basename(file), compress_type=zipfile.ZIP_DEFLATED)
    zFile.close()
    return send_file(z_path, as_attachment=True, mimetype="application/x-lisp"), 200



@app.route("/csv/<mnemonic>", methods=["GET"])
def send_csv_info(mnemonic):
    path = "{result}/{id}/*.csv".format(result=RESULT_DIR, id=mnemonic)
    files = glob.glob(path)
    logger.info(files)
    z_path = "{result}/{id}/{id}-csv.zip".format(result=RESULT_DIR, id=mnemonic)
    zFile = zipfile.ZipFile(z_path, "w")
    for file in files:
        zFile.write(file, arcname=os.path.basename(file), compress_type=zipfile.ZIP_DEFLATED)
    zFile.close()
    return send_file(z_path, as_attachment=True, mimetype="text/csv"), 200


@app.route("/csv/<mnemonic>/<file_name>", methods=["GET"])
def send_csv_files(mnemonic, file_name):
    path = os.path.join(RESULT_DIR, mnemonic, file_name.lower() + ".csv")
    if os.path.exists(path):
        return send_file(path, as_attachment=True), 200
    else:
        return jsonify({"response": "File not found"}), 404


@app.route("/summary/<mnemonic>", methods=["GET"])
def send_summary(mnemonic):
    path = os.path.join(RESULT_DIR, mnemonic, "summary.json")
    if os.path.exists(path):
        with open(path, "r") as s:
            summary = json.load(s)
            return jsonify(summary), 200
    else:
        return jsonify({"response": "File not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")
