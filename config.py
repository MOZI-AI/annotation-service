__author__ = "Enku Wendwosen & Abdulrahman Semrie"

import os
import yaml
import logging
import logging.config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

OPENCOG_DEPS_PATH = os.path.join(PROJECT_ROOT, "scheme/opencog_deps")

DATASET_FOLDER = os.path.join(PROJECT_ROOT, "datasets")

FUNCTIONS_FOLDER = os.path.join(PROJECT_ROOT, "scheme/functions")

FUNCTION_PATHs = [os.path.join(FUNCTIONS_FOLDER, fn) for fn in os.listdir(FUNCTIONS_FOLDER) if
                  os.path.isfile(os.path.join(FUNCTIONS_FOLDER, fn))]

HELPERS_FOLDER = os.path.join(ROOT, PROJECT_ROOT, "scheme/helpers")

HELPER_PATHs = [os.path.join(HELPERS_FOLDER, fn) for fn in os.listdir(HELPERS_FOLDER) if
                  os.path.isfile(os.path.join(HELPERS_FOLDER, fn))]

try:
    DATASET_PATHs = [os.path.join(DATASET_FOLDER, dataset) for dataset in os.listdir(DATASET_FOLDER) if
                 os.path.isfile(os.path.join(DATASET_FOLDER, dataset))]
except FileNotFoundError: #For testing
    DATASET_PATHs = "/home/root"

ANNOTATIONS_YML = os.path.join(PROJECT_ROOT, "scheme/annotation_definition.yml")

TEST_DATASET = os.path.join(DATASET_FOLDER, "sample_dataset.scm")

TEST_FOLDER = os.path.join(PROJECT_ROOT, "tests/data")


try:
    PRODUCTION_MODE = True if int(os.environ["PROD_MODE"]) == 1 else False
    SERVICE_PORT = os.environ["SERVICE_PORT"]
except KeyError:
    PRODUCTION_MODE = False
    SERVICE_PORT = 3000

SERVICE_URL = "localhost"


def setup_logging(default_path='logging.yml', default_level=logging.INFO):
    """Setup logging configuration
    """
    if os.path.exists(default_path):
        with open(default_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
