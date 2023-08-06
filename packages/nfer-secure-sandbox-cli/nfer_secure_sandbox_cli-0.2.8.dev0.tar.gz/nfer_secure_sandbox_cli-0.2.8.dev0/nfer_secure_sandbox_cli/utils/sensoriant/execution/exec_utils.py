import sys
import json
import requests
import logging

from utils.authentication.authenticate import get_credentials, authenticate
from utils.parsing.yaml import parse_var, parseable_expr
from utils.sensoriant.configuration.conf import *

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def exec_and_manage(execobj, verbosity):
    logging.root.setLevel(verbosity)
    access_key = get_credentials('ACCESS_KEY')
    secret_key = get_credentials('SECRET_KEY')
    entity = parse_var(execobj["entity"]) if parseable_expr(execobj["entity"]) else \
        execobj["docker"]["image_name"]
    authobj = authenticate({
        "access_key": access_key,
        "secret_key": secret_key
    })
    if authobj["message"] == "Authenticated":
        data = {
            "is_authenticated": True,
            "email": authobj["email"]
        }
        response = requests.post("%s/pipelines/start/%s" % (
            nfer_sdbx_url,
            entity
        ), json=data,headers={'cookie':'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1',})
        return response.json()
    else:
        logger.error("Errors authenticating user, while executing the policy `%s`" % (entity))
        logger.error("Exitting ...")
        sys.exit(1)
