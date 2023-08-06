import time
import logging

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)

from utils.parsing.yaml import read_yaml
from utils.logging.verbosity import get_verbosity_message, print_verbosity_message
from utils.tasks.manage_symm_keys import get_symm_algokey
from utils.tasks.manage_codebase import populate_codebase
from utils.tasks.manage_certs import get_certs
from utils.tasks.manage_client_keys import get_client_keypairs
from utils.tasks.manage_sandbox_specs import set_sandbox_specs
from utils.tasks.manage_data_projections import get_data_projection
from utils.tasks.manage_outputs import gen_output_encryption_bundle, publish_artefacts
from utils.tasks.manage_dockerization import dockerize_algo
from utils.tasks.manage_policies import prepare_policy
from utils.tasks.manage_policies import upload_policy
from utils.tasks.manage_executions import execute_policy
from utils.tasks.manage_outputs import retrieve_output, decrypt_output
from utils.state.manage_state import initialize_state, register_policy_properties
from actions.initialize import init


def run():
    yaml_content = read_yaml()
    loglvl = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARN,
    }

    verbosity = loglvl[str(get_verbosity_message(yaml_content["verbose"])).upper()]
    print_verbosity_message(verbosity)
    logging.root.setLevel(yaml_content["verbose"].upper())
    init(verbosity)
    logger.info("\033[94mRunning for the policy : \033[1m\033[4m%s\033[0m ..." % (yaml_content["name"]))
    logger.info("\033[95mRunning the playbook : `\033[4m\033[1mmain.yml\033[0m` ...")
    logging.root.setLevel(logging.INFO)
    initialize_state()
    confobj = {
        "pipeline_name": yaml_content["name"],
        "start_epoch": int(time.time())
    }
    register_policy_properties(confobj)
    task_runners = {
        "populate-codebase": populate_codebase,
        "get-certs": get_certs,
        # "get-client-keypair": get_client_keypairs,
        # "get-symmetric-algokey": get_symm_algokey,
        "set-sandbox-specs": set_sandbox_specs,
        "get-data-projection": get_data_projection,
        "output-encrypt-bundle": gen_output_encryption_bundle,
        "dockerize-algo": dockerize_algo,
        "prepare-policy": prepare_policy,
        "upload-policy": upload_policy,
        "execute-policy": execute_policy,
        "retrieve-output": retrieve_output,
        "publish-artefacts": publish_artefacts
    }
    for task in yaml_content["tasks"]:
        verb = [k for k in task.keys() if k not in ["name", "register"]][0]
        logger.info(
            "\n\n\033[94mRunning task : '\033[4m%s\033[0m' \033[94m- i.e -'\033[4m%s\033[0m\033[94m'\033[0m\n\n" % (
            verb, task["name"]))
        task_runners[verb](task, verbosity)
        input("\n\033[94m\n\nEnd of task : `%s`. PRESS ENTER to move ahead: \033[0m" % (verb))
