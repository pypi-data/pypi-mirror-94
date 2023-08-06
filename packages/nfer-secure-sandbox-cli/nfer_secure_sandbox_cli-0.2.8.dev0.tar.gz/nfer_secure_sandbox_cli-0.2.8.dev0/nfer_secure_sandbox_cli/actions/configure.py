import os
import sys
import getpass
from utils.logging.logger import log
from utils.sensoriant.configuration.conf import *
import logging

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def configure():
    logger.setLevel(logging.INFO)
    creds_path = creds_conf_path % getpass.getuser() #creds_conf_path % (os.environ["USER"])
    if os.path.isfile("%s%s" % (creds_path, creds_conf_file)):
        cat_content = "\n".join([str(line).strip() for line in open("%s%s" % (creds_path, creds_conf_file),"r")])
        oin = input("\033[93mFile `%s%s` already exists\033[0m, with credentials:\n %s \n \033[1mDo you wish to ovewrite the file?\033[0m [y|Y "
                    "for yes, any other for No]: \n" % (creds_path, creds_conf_file, cat_content))
        if str(oin).lower() == "y":
            os.makedirs(creds_path, exist_ok=True)
            fout = open("%s%s" % (creds_path, creds_conf_file), "w")
            access_key = input("\033[94mPlease enter the Access ID: \033[0m")
            secret_key = input("\033[94mPlease enter the Secret Key: \033[0m")
            fout.write("ACCESS_KEY=%s\n" % access_key)
            fout.write(("SECRET_KEY=%s\n" % secret_key))
            logger.info("\033[92mRewrote `credentials.txt` file inside `%s`\033[0m, containing `access_id` and `secret_key` "
                        "above" % (creds_path))
        else:
            logger.info("\033[96mOK. Skipping to configure the nfer-sandbox-cli... \033[1mExitting.\033[0m")
            sys.exit(1)
    else:
        os.makedirs(creds_path, exist_ok=True)
        fout = open("%s%s" % (creds_path, creds_conf_file), "w")
        access_key = input("\033[94mPlease enter the Access ID: \033[0m")
        secret_key = input("\033[94mPlease enter the Secret Key: \033[0m")
        fout.write("ACCESS_KEY=%s\n" % access_key)
        fout.write(("SECRET_KEY=%s\n" % secret_key))
        logger.info("\033[92mAdded `credentials.txt` file inside `%s`\033[0m, containing `access_id` and `secret_key` "
                    "above" % (creds_path))
    fout.close()
