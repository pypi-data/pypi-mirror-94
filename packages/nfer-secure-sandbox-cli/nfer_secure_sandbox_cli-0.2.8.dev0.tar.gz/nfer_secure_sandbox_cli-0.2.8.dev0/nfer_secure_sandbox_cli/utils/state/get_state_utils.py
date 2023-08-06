from configparser import ConfigParser
from utils.logging.logger import log
import sys

import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def get_algokey_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("ALGOKEY"):
        confobj = dict(configparser["ALGOKEY"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready have a symmetric algokey created, at path `%s`\033[0m" % (
                confobj["path"]
            ))
        return False
    else:
        return True


def get_codebase_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("CODE"):
        confobj = dict(configparser["CODE"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready have code base polled, code path `%s` and deps path `%s`. To be replaced with SCM poller as CI\033[0m" % (
                confobj["src_code"], confobj["src_deps"]
            ))
        #sys.exit(1)
        return False
    else:
        return True


def get_certs_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("CERTS"):
        confobj = dict(configparser["CERTS"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug("\033[96mAlready have a certificate issued, with path = %s and files %s and %s. Skipping unless state is cleared\033[0m"%(
            confobj["path"], confobj["cert"], confobj["privkey"]
        ))
        #sys.exit(1)
        return False
    else:
        return True


def get_client_keypair_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("CLIENT_KEYPAIRS"):
        confobj = dict(configparser["CLIENT_KEYPAIRS"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready have a keypair issued, with path = %s and files %s and %s. Skipping unless state is cleared\033[0m" % (
                confobj["path"], confobj["path"], confobj["privkey"]
            ))
        #sys.exit(1)
        return False
    else:
        return True


def get_sandbox_specs_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("SANDBOX_SPECS"):
        confobj = dict(configparser["SANDBOX_SPECS"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready have a sandbox specs rolled and VM provisioned, with id %s. Skipping unless state is cleared\033[0m" % (
                confobj["instance_id"]
            ))
        #sys.exit(1)
        return False
    else:
        return True


def get_data_projection(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("DATA_PROJECTION"):
        confobj = dict(configparser["DATA_PROJECTION"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready have a data projection created, with id %s name %s. Skipping unless state is cleared\033[0m" % (
                confobj["projection_id"], confobj["projection_name"]
            ))
        #sys.exit(1)
        return False
    else:
        return True


def get_dockerize_algo_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("DOCKERIZE_ALGO"):
        confobj = dict(configparser["DOCKERIZE_ALGO"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready have an encrypted docker image %s. Skipping unless state is cleared\033[0m" % (
                confobj["image"]
            ))
        #sys.exit(1)
        return False
    else:
        return True


def get_prepare_policy_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("PREPARE_POLICY"):
        confobj = dict(configparser["PREPARE_POLICY"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready had a policy prepared %s. Skipping unless state is cleared\033[0m" % (
                confobj["policy_file"]
            ))
        #sys.exit(1)
        return False
    else:
        return True


def get_output_enrypt_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("ENCRYPT_OUTPUT_BUNDLE"):
        confobj = dict(configparser["ENCRYPT_OUTPUT_BUNDLE"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready have an encrypted bundle %s with %s. Skipping unless state is cleared\033[0m" % (
                confobj["name"], confobj["fspf_key"]
            ))
        #sys.exit(1)
        return False
    else:
        return True


def get_upload_policy_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("UPLOAD_POLICY"):
        confobj = dict(configparser["UPLOAD_POLICY"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready had a policy uploaded %s, with status %s. Skipping unless state is cleared\033[0m" % (
                confobj["pipeline_id"], confobj["status"]
            ))
        #sys.exit(1)
        return False
    else:
        return True


def get_execute_policy_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("EXECUTE_POLICY"):
        confobj = dict(configparser["EXECUTE_POLICY"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready have a pipeline %s with status %s\033[0m" % (
                confobj["id"], confobj["status"]
            ))
        #sys.exit(1)
        return False
    else:
        return True


def get_retrieve_output_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("RETRIEVE_OUTPUT"):
        confobj = dict(configparser["RETRIEVE_OUTPUT"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready had an output retrieved, path %s. Skipping unless state is cleared\033[0m" % (
                confobj["dest"]
            ))
        #sys.exit(1)
        return False
    else:
        return True


def get_decrypt_output_state(task, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    if configparser.has_section("DECRYPT_OUTPUT"):
        confobj = dict(configparser["DECRYPT_OUTPUT"])
    else:
        confobj = {}
    if bool(confobj):
        logger.debug(
            "\033[96mAlready had an output decrypted, from path %s to path %s. Skipping unless state is cleared\033[0m" % (
                confobj["local_source_dir"], confobj["local_dest_dir"]
            ))
        #sys.exit(1)
        return False
    else:
        return True