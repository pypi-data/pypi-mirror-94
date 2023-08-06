import sys

from utils.display.artefacts_utils import publish
from utils.state.manage_state import register
from utils.state.manage_state import read_state, persist_state
from utils.sensoriant.sandbox.sandbox import provision_sandbox, check_sandbox
from utils.sensoriant.configuration.conf import *
from utils.logging.logger import log
import time
import json
import requests
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def set_sandbox_specs(task, verbosity):
    logging.root.setLevel(verbosity)
    if read_state(task, verbosity, 'sandbox-specs'):
        specs = provision_sandbox(task["set-sandbox-specs"], verbosity)
        if specs["SUCCESS"]:
            status = specs["response"]["status"]
            while status not in end_statuses:
                logger.debug("\033[96msince sandbox provisioning status is still `\033[4m%s\033[0m\033[96m`, sleeping for %d secs and trying to check if status in: \033[1m%s\033[0m" % (
                    status, sleep_time,
                    end_statuses
                ))
                time.sleep(sleep_time)
                status = check_sandbox(specs["response"])
                # status = "READY"  # hack because nothing is working at the moment
            logger.debug("\n\n\033[92mFinally a sandbox has been provisioned : '\033[4m%s\033[0m\033[92m' \033[1m%s\033[0m\033[92m in \033[4m%s\033[0m\033[92m state.\033[0m"%(
                specs["response"]["id"],
                specs["response"]["name"],
                status
            ))
            confobj = {
                "instance_id": specs["response"]["id"],
                "instance_name": specs["response"]["name"],
                "template_id": specs["response"]["template"]["id"],
                "template_name":specs["response"]["template"]["name"],
                "public_key": specs["response"]["publicKey"],
                "measurement": specs["response"]["measurement"],
                "status": status
            }
        else:
            if specs["response"]["message"] == "AUTHENTICATION FAILED":
                logger.critical("\n\n\033[91mFailed because of Authentication Failure. Check ACCESS_KEY and SECRET_KEY in file : `\033[4m%s/%s\033[0m\033[91m`\033[0m"%(creds_conf_path, creds_conf_file))
            sys.exit(1)
        register(confobj, task)
        persist_state(task, verbosity, "sandbox-specs", confobj)
        publish("sandbox", task, confobj)
