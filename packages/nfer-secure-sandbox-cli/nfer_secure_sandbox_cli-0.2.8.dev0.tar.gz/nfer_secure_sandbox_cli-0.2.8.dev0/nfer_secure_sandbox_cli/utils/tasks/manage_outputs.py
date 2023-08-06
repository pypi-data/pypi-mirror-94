import sys

from utils.display.artefacts_utils import publish
from utils.state.manage_state import read_state, register
from utils.state.manage_state import persist_state
from utils.sensoriant.output.output_utils import retrieve_encrypted_output, decrypt_encrypted_output, \
    generate_encryption_bundle
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def gen_output_encryption_bundle(task, verbosity):
    logging.root.setLevel(verbosity)
    if read_state(task, verbosity, 'output-encrypt-bundle'):
        output_specs = generate_encryption_bundle(task["output-encrypt-bundle"], verbosity)
        confobj = {
            "fspf_key": output_specs["FSPF_KEY"],
            "fspf_tag": output_specs["FSPF_TAG"],
            "name": output_specs["name"],
            "id": output_specs["id"]
        }
        register(confobj, task)
        persist_state(task, verbosity, "output-encrypt-bundle", confobj)
        publish("output-encrypt", task, confobj)


def publish_artefacts(task, verbosity):
    logger.info("\033[92mThis brings us to the end of Our Pipeline. Please check the folder \033[1m\033[4m`artefacts`\033[0m \033[92mfor a synopsis walkthrough of the entire execution\033[0m")
    sys.exit(1)


def retrieve_output(task, verbosity):
    logging.root.setLevel(verbosity)
    if read_state(task, verbosity, 'retrieve-output'):
        output_specs = retrieve_encrypted_output(task["retrieve-output"])
        register(output_specs, task)
        persist_state(task, verbosity, "retrieve-output", output_specs)
        publish("retrieve-output", task, output_specs)


def decrypt_output(task, verbosity):
    if read_state(task, verbosity, 'decrypt-output'):
        output_specs = decrypt_encrypted_output(task["decrypt-output"])
        confobj = {
            "local_source_dir": output_specs["local_source_dir"],
            "local_dest_dir": output_specs["local_dest_dir"],
        }
        register(confobj, task)
        persist_state(task, verbosity, "decrypt-output", confobj)