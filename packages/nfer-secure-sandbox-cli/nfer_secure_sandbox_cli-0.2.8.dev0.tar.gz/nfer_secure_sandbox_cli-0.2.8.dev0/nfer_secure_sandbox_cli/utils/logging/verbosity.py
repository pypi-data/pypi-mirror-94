from utils.logging.logger import log
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def get_verbosity_message(verbose_level):
    return verbose_level


def print_verbosity_message(verbosity):
    logging.root.setLevel(logging.INFO)
    msges = {
        10: """
        \033[93m\n\nPrinting logs with very high verbosity upto debug statements. Switch to\033[0m: 
        
        - \033[93mINFO\033[0m by setting ``verbose : info`` in the `main.yml` file for low verbosity.
        - \033[93mWARN\033[0m by setting ``verbose : warn`` in the `main,yml` file for Warnings/Errors only. 
        """,
        20: """
        \033[93m\n\nPrinting logs with adequate verbosity. Informative, necessary statements. Switch to\033[0m:
        
        - \033[93mDEBUG\033[0m by setting ``verbose : debug`` in the `main.yml` file for higher verbosity.
        - \033[93mWARN\033[0m by setting ``verbose : warn`` in the `main,yml` file for Warnings/Errors only.
        """,
        30: """
        \033[93m\n\nPrinting only Errors/Warnings as the execution is run using `nfer-sandbox-cli run`. Switch to\033[0m:
        
        - \033[93mDEBUG\033[0m by setting ``verbose : debug`` in the `main.yml` file for higher verbosity.
        - \033[93mINFO\033[0m by setting ``verbose : info`` in the `main.yml` file for low verbosity.
        """
    }
    logger.info(msges[verbosity])
