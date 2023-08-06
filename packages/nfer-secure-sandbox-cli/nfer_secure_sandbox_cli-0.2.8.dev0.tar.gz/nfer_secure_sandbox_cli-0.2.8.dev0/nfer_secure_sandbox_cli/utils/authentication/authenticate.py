import os
import json
import requests
from utils.logging.logger import log
from utils.sensoriant.configuration.conf import *
import json; import base64; import requests
import logging
import getpass
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def authenticate(credobj):
    access_key = credobj['access_key']
    secret_key = credobj['secret_key']
    key = '%s:%s' % (access_key, secret_key)
    sig = base64.standard_b64encode(key.encode('utf-8')).decode('utf-8')
    headers = {'Authorization': 'Basic %s' % sig, 'Content-Type': 'application/json'}
    resp = requests.get(auth_url, headers=headers)
    return resp.json()


def create_CSR(taskobj, credobj):
    path = taskobj["path"]
    cert = "%s/%s-pubkey.pem" %(path, taskobj["name"])
    data = {'access_key': credobj["access_key"], 'secret_key': credobj["secret_key"]}
    files = [
        ('upload-cert', (cert, open(cert, 'rb'), 'application/octet')),
        ('datas', ('datas', json.dumps(data), 'application/json')),
    ]
    key = '%s:%s' % (credobj["access_key"], credobj["secret_key"])
    sig = base64.standard_b64encode(key.encode('utf-8')).decode('utf-8')
    headers = {'Authorization': 'Basic %s' % sig, 'Content-Type': 'application/json'}
    headers={'cookie':'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1',}
    return requests.post(cert_upload_url, files=files,headers=headers)


def get_credentials(field):
    creds_path = creds_conf_path % getpass.getuser()
    path = '%s/%s' %(creds_path, creds_conf_file)
    if os.path.exists(path):
        found = False
        with open(path) as fin:
            for line in fin:
                kv = line.strip().split("=")
                if kv[0].strip() == field:
                    found = True
                    return kv[1].strip()
        if not found:
            logger.debug("the requested field `%s` could not be found in the credentials.txt file!"%(field))
    else:
        logger.error("the path `%s` carrying the credentials file `credentials.txt` doesn't exist!")

