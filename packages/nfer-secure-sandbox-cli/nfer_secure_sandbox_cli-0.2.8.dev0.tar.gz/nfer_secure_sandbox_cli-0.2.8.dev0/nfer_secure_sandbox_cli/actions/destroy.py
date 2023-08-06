import os
import shutil
from utils.logging.logger import log
from utils.sensoriant.termination.destroy_infra import destroy_exec_resources
import logging

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def destroy():
    logger.setLevel(logging.INFO)
    proj = os.getcwd().split("/")[-1]
    logger.info("\033[93mDestroying the folders, state in `current directory` i.e project `%s`...\033[0m\n\n" % (
        proj
    ))
    try:
        logger.info("\033[94mClearing the app directory i.e code+deps files ...\033[0m")
        os.remove("app/nference_algorithm.py")
        os.remove("app/requirements.txt")
        logger.info("\033[94mDeleting directory 'build' ...\033[0m")
        [os.remove("build/%s" % f) for f in os.listdir('build')]
        logger.info("\033[94mDeleting directory 'keys' ...\033[0m")
        [os.remove("keys/%s" % f) for f in os.listdir('keys')]
        logger.info("\033[94mDeleting directory 'certs' ...\033[0m")
        [os.remove(("certs/%s" % f)) for f in os.listdir('certs')]
        logger.info("\033[94mDeleting directory 'policy' ...\033[0m")
        [os.remove("policy/%s" % f) for f in os.listdir('policy')]
        logger.info("\033[94mDeleting directory 'docker-files' ...\033[0m")
        [os.remove("docker-files/%s" % f) for f in os.listdir('docker-files')]
        logger.info("\033[94mRemoving the output folders : 'decrypt-output ...\033[0m")
        [os.remove("output/decrypt-output/%s" % f) for f in os.listdir("output/decrypt-output")]
        logger.info("\033[94mRemoving the output folders : 'empty-output' ...\033[0m")
        [shutil.rmtree("output/empty-output/%s" % f) for f in os.listdir("output/empty-output")]
        logger.info("\033[94mRemoving google creds for sensoriant : 'gcs-creds' ...\033[0m")
        shutil.rmtree("gcs-creds")
        logger.info("\033[94mDeleting directory 'output/decrypt-input' ...\033[0m")
        shutil.rmtree("output/decrypt-input")
        logger.info("\033[94mDeleting directory 'output/decrypt-output' ...\033[0m")
        shutil.rmtree("output/decrypt-output")
        logger.info("\033[94mDeleting directory 'output/decrypt-empty-output' ...\033[0m")
        shutil.rmtree("output/empty-output")
    except Exception as e:
        logger.info(
            "\n\n\033[91mSome problems with cleaning the file structure of project `%s`! err - \033[4m%s\033[0m \033[0m" % (
                proj, str(e)
            ))
    logger.info("\n\n\033[92mCleaned `build`, `policy`, `docker-files`, `keys`, `certs` in the `current directory`\033[0m")
    destroy_exec_resources()
    try:
        os.remove(".pbstate")
        os.remove(".register")
    except Exception as e:
        logger.info("\n\n\033[91mSome problems removing the state files - `.pbstate` and `.register` ! err - \033[4m%s\033[0m" % (
            str(e)
        ))  # stub - this can be improved.
    logger.info("\n\n\033[92mDeleted the internal state file `.pbstate`\033[0m")

