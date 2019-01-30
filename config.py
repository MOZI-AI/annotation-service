__author__ = "Enku Wendwosen"

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

OPENCOG_DEPS_PATH = os.path.join(PROJECT_ROOT, "scm/opencog_deps")

DATASET_FOLDER = os.path.join(PROJECT_ROOT, "scm/datasets")

FUNCTIONS_FOLDER = os.path.join(PROJECT_ROOT, "scm/functions")

FUNCTION_PATHs = [os.path.join(FUNCTIONS_FOLDER, fn) for fn in os.listdir(FUNCTIONS_FOLDER) if
                  os.path.isfile(os.path.join(FUNCTIONS_FOLDER, fn))]

DATASET_PATHs = [os.path.join(DATASET_FOLDER, dataset) for dataset in os.listdir(DATASET_FOLDER) if
                 os.path.isfile(os.path.join(DATASET_FOLDER, dataset))]

ANNOTATIONS_YML = os.path.join(PROJECT_ROOT, "scm/annotation_definition.yml")

TEST_DATASET = os.path.join(DATASET_FOLDER, "sample_dataset.scm")

TEST_FOLDER = os.path.join(PROJECT_ROOT, "tests/data")


try:
    PRODUCTION_MODE = True if int(os.environ["PROD_MODE"]) == 1 else False
    SERVICE_PORT = os.environ["SERVICE_PORT"]
    SERVICE_URL = os.environ["SERVICE_ADDR"]
except KeyError:
    PRODUCTION_MODE = False
    SERVICE_PORT = 5003
    SERVICE_URL = "localhost"
