from utils.display.artefacts_utils import publish
from utils.state.manage_state import read_state, register
from utils.state.manage_state import persist_state
from utils.sensoriant.policy.policy_utils import prepare_signed_policy, upload_signed_policy
import logging
import sys
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def prepare_policy(task, verbosity):
    logging.root.setLevel(verbosity)
    if read_state(task, verbosity, 'prepare-policy'):
        policy_specs = prepare_signed_policy(task["prepare-policy"], verbosity)
        register( policy_specs, task)
        persist_state(task, verbosity, "prepare-policy",  policy_specs)
        publish("prepare-policy", task, policy_specs)


def upload_policy(task, verbosity):
    logging.root.setLevel(verbosity)
    if read_state(task, verbosity, 'upload-policy'):
        policy_specs = upload_signed_policy(task["upload-policy"], verbosity)
        if policy_specs["SUCCESS"]:
            confobj = {
                "SUCCESS": policy_specs["SUCCESS"],
                "pipeline_name": policy_specs["response"]["name"],
                "pipeline_id": policy_specs["response"]["id"],
                "status": policy_specs["response"]["status"],
                "template_id": policy_specs["response"]["template"]["id"],
                "template_name": policy_specs["response"]["template"]["name"],
                "pipeline_creation_date": policy_specs["response"]["creationDate"],
            }
            register(confobj, task)
            persist_state(task, verbosity, "upload-policy", confobj)
            publish("upload-policy", task, confobj)
        else:
            logger.error("The Creation of Pipeline was unsuccessful with message `%s`"%(
                policy_specs["response"]["message"]
            ))
            logger.error("Exitting ...")
            sys.exit(1)
