from configparser import ConfigParser
from utils.logging.logger import log
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def post_algokey_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["ALGOKEY"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of symmetric Algokey into the `.pbstate` file\033[0m")


def post_codebase_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["CODE"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of codebase into the `.pbstate` file\033[0m")


def post_certs_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["CERTS"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of certificates generation into the `.pbstate` file\033[0m")


def post_client_keypair_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["CLIENT_KEYPAIRS"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of Client Asymmetric Key Pair details into the `.pbstate` file\033[0m")


def post_sandbox_specs_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["SANDBOX_SPECS"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of Sandbox Provisioning Task into the `.pbstate` file\033[0m")


def post_data_projection(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["DATA_PROJECTION"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of data projection into the `.pbstate` file\033[0m")


def post_dockerize_algo_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["DOCKERIZE_ALGO"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of algo dockerization into the `.pbstate` file\033[0m")


def post_output_enrypt_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["ENCRYPT_OUTPUT_BUNDLE"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of output encryption bundle into the `.pbstate` file\033[0m")


def post_prepare_policy_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["PREPARE_POLICY"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of policy doc preparation into the `.pbstate` file\033[0m")


def post_upload_policy_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["UPLOAD_POLICY"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of policy upload into the `.pbstate` file\033[0m")


def post_execute_policy_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["EXECUTE_POLICY"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of policy a.k.a pipeline execution into the `.pbstate` file\033[0m")


def post_retrieve_output_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["RETRIEVE_OUTPUT"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of output retrieval into the `.pbstate` file\033[0m")


def post_decrypt_output_state(task, verbosity, confobj):
    logging.root.setLevel(verbosity)
    config_object = ConfigParser()
    config_object["DECRYPT_OUTPUT"] = confobj
    with open('.pbstate', 'a') as conf:
        config_object.write(conf)
    logger.info("\033[93mWrote the state of output decryption into the `.pbstate` file\033[0m")
