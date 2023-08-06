from utils.display.artefacts_utils import publish
from utils.state.manage_state import read_state, persist_state, register
from utils.sensoriant.algo.algo_utils import encrypt_dockerize_persist
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def dockerize_algo(task, verbosity):
    logging.root.setLevel(verbosity)
    if read_state(task, verbosity, 'dockerize-algo'):
        algo_specs = encrypt_dockerize_persist(task["dockerize-algo"], verbosity)
        confobj = {
            "image": algo_specs["docker-identifier"],
            "fspf_key": algo_specs["FSPF_KEY"],
            "fspf_tag": algo_specs["FSPF_TAG"],
            "mrenclave": algo_specs["mrenclave"]
        }
        register(algo_specs, task)
        persist_state(task, verbosity, "dockerize-algo", confobj)
        publish("dockerize", task, confobj)
