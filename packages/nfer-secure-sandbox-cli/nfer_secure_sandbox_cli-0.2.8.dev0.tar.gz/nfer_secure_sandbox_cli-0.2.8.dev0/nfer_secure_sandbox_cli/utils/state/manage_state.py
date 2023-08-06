import os
import json
import traceback
from pathlib import Path
from utils.state.get_state_utils import *
from utils.state.post_state_utils import *
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def read_state(task, verbosity, step):
    logging.root.setLevel(verbosity)
    get_state_funcs = {
        "algokey": get_algokey_state,
        "codebase": get_codebase_state,
        "certs": get_certs_state,
        "client-keypair": get_client_keypair_state,
        "sandbox-specs": get_sandbox_specs_state,
        "data-projection": get_data_projection,
        "dockerize-algo": get_dockerize_algo_state,
        "output-encrypt-bundle": get_output_enrypt_state,
        "prepare-policy": get_prepare_policy_state,
        "upload-policy": get_upload_policy_state,
        "execute-policy": get_execute_policy_state,
        "retrieve-output": get_retrieve_output_state,
        "decrypt-output": get_decrypt_output_state
    }
    return get_state_funcs[step](task, verbosity)


def persist_state(task, verbosity, step, confobj):
    logging.root.setLevel(verbosity)
    post_state_funcs = {
        "algokey": post_algokey_state,
        "codebase": post_codebase_state,
        "certs": post_certs_state,
        "client-keypair": post_client_keypair_state,
        "sandbox-specs": post_sandbox_specs_state,
        "data-projection": post_data_projection,
        "dockerize-algo": post_dockerize_algo_state,
        "output-encrypt-bundle": post_output_enrypt_state,
        "prepare-policy": post_prepare_policy_state,
        "upload-policy": post_upload_policy_state,
        "execute-policy": post_execute_policy_state,
        "retrieve-output": post_retrieve_output_state,
        "decrypt-output": post_decrypt_output_state
    }
    post_state_funcs[step](task, verbosity, confobj)


def initialize_state():
    if not os.path.isfile('.pbstate'):
        Path('.pbstate').touch()
    else:
        logger.critical("\033[93mThe Project already has a state in the file: \033[1m`.pbstate`\033[0m, \033[93mthe execution may be affected by it.\033[0m")
    if not os.path.isfile('.register'):
        with open('.register', 'a') as json_file:
            json.dump({}, json_file)
    logger.debug("""
    \033[92m\nThe state maintenance and response logging files : 
    '\033[1m.pbstate\033[0m' \033[92mand '\033[1m.register\033[0m' \033[92m\033[4mhave been created\033[0m.
    """)


def register_policy_properties(confobj):
    with open(".register","r") as fj:
        data = json.load(fj)
        data["properties"] = confobj
    fj.close()
    with open(".register","w") as fj:
        json.dump(data, fj)
    fj.close()


def register(confobj, task):
    try:
        if 'register' in task.keys():
            with open(".register", 'r') as fj:
                data = json.load(fj)
                data[task["register"]] = confobj
            fj.close()
            with open(".register", 'w') as fj:
                json.dump(data, fj)
            fj.close()
        return True
    except Exception as e:
        traceback.print_exc()
        return False
