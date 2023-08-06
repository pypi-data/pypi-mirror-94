import sys
import json
from typing import Dict, Any

import requests
from utils.sensoriant.configuration.conf import *
from utils.parsing.yaml import parse_var, parseable_expr
from utils.authentication.authenticate import get_credentials, authenticate

import logging

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def check_sandbox(respobj):
    access_id = get_credentials('ACCESS_KEY')
    secret_key = get_credentials('SECRET_KEY')
    authobj = authenticate({
        "access_key": access_id,
        "secret_key": secret_key
    })
    if authobj["message"] == 'Authenticated':
        response = requests.get(
            '%s/platforms/by_id/%s' % (nfer_sdbx_url, respobj["id"]), headers={'cookie':'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1',}
        )
        return response.json()["response"]["status"]


def provision_sandbox(specobj, verbosity):
    logger.setLevel(verbosity)
    cert_path = parse_var(specobj["cert_path"]) if parseable_expr(specobj["cert_path"]) else specobj["cert_path"]
    certificate = parse_var(specobj["certificate"]) if parseable_expr(specobj["certificate"]) else specobj[
        "certificate"]
    ca_cert_path = parse_var(specobj["ca_cert_path"]) if parse_var(specobj["ca_cert_path"]) else specobj["ca_cert_path"]
    ca_certificate = parse_var(specobj["ca_certificate"]) if parseable_expr(specobj["ca_certificate"]) else specobj[
        "ca_certificate"]
    if not len(ca_certificate):
        logger.warning("\033[91mthe CA Certificate is empty.\033[0m")
        ca_cert_blob = ""
    else:
        with open("%s/%s" % (ca_cert_path, ca_certificate), "r") as fin:
            ca_cert_blob = fin.read()
    if not len(certificate):
        logger.error("\033[91mThe Certificate is \033[4mempty\033[0m. \033[91mThis is Fatal.\033[0m")
        logger.error("\033[91m\033[1mExitting! ...\033[0m")
        cert_blob = ""
    else:
        with open("%s/%s" % (cert_path, certificate), "r") as fin:
            cert_blob = fin.read()
    access_key = get_credentials('ACCESS_KEY')
    secret_key = get_credentials('SECRET_KEY')
    payload: dict[str, Any] = {
        'certificate': cert_blob,
        'ca_certificate': ca_cert_blob,
        'access_key': access_key,
        'secret_key': secret_key
    }
    response = requests.post(
        '%s/platforms/create/%s' % (
            nfer_sdbx_url, specobj["template_id"]
        ), json=payload,headers={'cookie':'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1',}
    )
    return response.json()
