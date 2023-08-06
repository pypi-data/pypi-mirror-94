import os
import sys
import requests
from utils.sensoriant.configuration.conf import *
from utils.parsing.yaml import parse_var, parseable_expr
from utils.authentication.authenticate import get_credentials, authenticate
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def get_or_create_data(dataobj, authobj, verbosity):
    logger.setLevel(verbosity)
    data_identifier = parse_var(dataobj["data_identifier"]) if parseable_expr(dataobj["data_identifier"]) else dataobj[
        "data_identifier"]
    public_key = parse_var(dataobj["sdbx_pubkey"]) if parseable_expr(dataobj["sdbx_pubkey"]) else dataobj["sdbx_pubkey"]
    cert_path = parse_var(dataobj["cert_path"]) if parseable_expr(dataobj["cert_path"]) else dataobj[
        "cert_path"]
    certificate = parse_var(dataobj["certificate"]) if parseable_expr(dataobj["certificate"]) else dataobj[
        "certificate"]
    ca_cert_path = parse_var(dataobj["ca_cert_path"]) if parseable_expr(dataobj["ca_cert_path"]) else dataobj[
        "ca_cert_path"]
    ca_certificate = parse_var(dataobj["ca_certificate"]) if parseable_expr(dataobj["ca_certificate"]) else dataobj[
        "ca_certificate"]
    ca_cert_blob = "" if ca_certificate == "" else open("%s/%s" % (ca_cert_path, ca_certificate), "r").read().strip()
    certificate = "%s/%s" % (cert_path, certificate)
    ca_certificate = "%s/%s" % (ca_cert_path, ca_certificate)
    cert_blob = open(certificate, "r").read().strip()
    data = {
        "data_identifier": data_identifier,
        'access_key': authobj["access_key"], 'secret_key': authobj["secret_key"],
        "certificate": cert_blob, "ca_certificate": ca_cert_blob, "public_key": public_key,
    }
    response = requests.post("%s/push_to_sens/%s" % (data_upload_url, dataobj["projection_id"]), json=data,headers={'cookie':'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1',})
    return response.json()
