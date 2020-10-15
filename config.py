__author__ = "Enku Wendwosen & Abdulrahman Semrie"

import os
import yaml
import logging
import logging.config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

OPENCOG_DEPS_PATH = os.path.join(PROJECT_ROOT, "utils/opencog_deps")

DATASET_FOLDER = os.path.join(PROJECT_ROOT, "datasets")


ANNOTATIONS_YML = os.path.join(PROJECT_ROOT, "scheme/annotation_definition.yml")

TEST_DATASET = os.path.join(PROJECT_ROOT, "scheme/tests/sample_dataset.scm")

TEST_FOLDER = os.path.join(PROJECT_ROOT, "tests/data")

CSV_TEST_FOLDER = os.path.join(TEST_FOLDER,"csv")


PLN_RULE = os.path.join(PROJECT_ROOT, "scheme/annotation/pln_rule.scm")

try:
    DATASET_PATHs = [os.path.join(DATASET_FOLDER, dataset) for dataset in os.listdir(DATASET_FOLDER) if
                 os.path.isfile(os.path.join(DATASET_FOLDER, dataset))]
except FileNotFoundError: #For testing
    DATASET_PATHs = "/home/root"


try:
    SERVICE_PORT = os.environ["SERVICE_PORT"]
except KeyError:
    SERVICE_PORT = 3000

try:
    MOZI_RESULT_URI = os.environ["SERVICE_ADDR"]
    SERVICE_URL = "http://"+ os.environ["SERVICE_ADDR"]
except KeyError:
    MOZI_RESULT_URI = "http://localhost:3004"
    SERVICE_URL = "localhost"

try: 
    RESULT_DIR = os.environ["RESULT_DIR"]
except KeyError:
    RESULT_DIR = "/tmp/result/"


def setup_logging(default_path='logging.yml', default_level=logging.INFO):
    """Setup logging configuration
    """
    LOG_DIR = "/tmp/annotation-service/log"
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    if os.path.exists(default_path):
        with open(default_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
