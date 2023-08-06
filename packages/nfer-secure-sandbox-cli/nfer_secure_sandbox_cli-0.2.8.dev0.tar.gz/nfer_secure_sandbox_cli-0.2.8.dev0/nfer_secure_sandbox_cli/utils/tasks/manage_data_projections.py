from utils.display.artefacts_utils import publish
from utils.state.manage_state import read_state, persist_state
from utils.state.manage_state import register
from utils.sensoriant.projection.data_projection import get_or_create_data
from utils.authentication.authenticate import get_credentials
import logging
import sys

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def get_data_projection(task, verbosity):
    logging.root.setLevel(verbosity)
    access_key = get_credentials('ACCESS_KEY')
    secret_key = get_credentials('SECRET_KEY')
    if read_state(task, verbosity, 'data-projection'):
        data_specs = get_or_create_data(task["get-data-projection"], {
            'access_key': access_key,
            'secret_key': secret_key
        }, verbosity)
        if data_specs["SUCCESS"]:
            logger.debug("\033[92mSuccessfully pushed data"
                         " projection '%s' %s to Sandbox VM. \033[0m" % (
                data_specs["cid"],
                data_specs["name"]
            ))
        else:
            logger.error("\033[91mSome problems pushing the projection to the Sandbox. \033[1mExitting!\033[0m")
            sys.exit(1)
        confobj = {
            "projection_id": data_specs["cid"],
            "projection_name": data_specs["name"],
            "data_sym_ekey": data_specs["data_sym_ekey"]
        }
        register(data_specs, task)
        persist_state(task, verbosity, "data-projection", confobj)
        publish("input-data", task, confobj)
