from cryptography.fernet import Fernet
from utils.logging.logger import log
from utils.state.manage_state import read_state, persist_state, register
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def get_symm_algokey(task, verbosity):
    logging.root.setLevel(verbosity)
    if read_state(task, verbosity, 'algokey'):
        key = Fernet.generate_key()
        kf = open(task["get-symmetric-algokey"]["path"], "w")
        kf.write(key.decode('utf-8'))
        kf.close()
        logger.debug("\033[92mWrote a symmetric file `algokey` at path: `%s`\033[0m"% task["get-symmetric-algokey"]["path"])
        confobj = {
            "path": task["get-symmetric-algokey"]["path"]
        }
        register(confobj, task)
        persist_state(task, verbosity, "algokey", confobj)

