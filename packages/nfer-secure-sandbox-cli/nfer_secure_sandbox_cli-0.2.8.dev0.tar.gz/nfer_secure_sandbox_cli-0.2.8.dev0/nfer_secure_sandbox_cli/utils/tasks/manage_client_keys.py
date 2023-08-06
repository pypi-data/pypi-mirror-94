from utils.state.manage_state import read_state, persist_state
from utils.state.manage_state import register
from utils.logging.logger import log
from Crypto.PublicKey import RSA
import os
import sys
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def get_client_keypairs(task, verbosity):
    logging.root.setLevel(verbosity)
    if read_state(task, verbosity, 'client-keypair'):
        if task["get-client-keypair"]["mode"] == "fetch":
            path = task["get-client-keypair"]["path"]
            cert = ''
            privkey = ''
            for f in os.listdir(path):
                if str(f).endswith(".cert"):
                    cert = str(f)
                elif str(f).endswith(".key"):
                    privkey = str(f)
            assert len(cert) > 0
            assert len(privkey) > 0
            confobj = {
                "mode": task["get-client-keypair"]["mode"],
                "path": path,
                "cert": cert,
                "privkey": privkey
            }
        elif task["get-client-keypair"]["mode"] == "create":
            os.makedirs(task["get-client-keypair"]["path"], exist_ok=True)
            key = RSA.generate(2048)
            with open(os.path.join(task["get-client-keypair"]["path"], '%s.key' % task["get-client-keypair"]["name"]),
                      'wb') as content_file:
                content_file.write(key.exportKey('PEM'))
                # os.chmod( # TODO otherwise permission erros while `docker-compose build algorithm`
                #     os.path.join(task["get-client-keypair"]["path"], '%s.key' % task["get-client-keypair"]["name"]),
                #     600)
            pubkey = key.publickey()
            with open(os.path.join(task["get-client-keypair"]["path"], "%s.cert" % task["get-client-keypair"]["name"]),
                      'wb') as content_file:
                content_file.write(pubkey.exportKey('OpenSSH'))
            confobj = {
                "mode": task["get-client-keypair"]["mode"],
                "path": task["get-client-keypair"]["path"],
                "cert": os.path.join(task["get-client-keypair"]["path"],
                                     "%s.cert" % task["get-client-keypair"]["name"]),
                "privkey": os.path.join(task["get-client-keypair"]["path"],
                                        '%s.key' % task["get-client-keypair"]["name"])
            }
        else:
            logger.error(
                "\033[91mThis mode for client keypairs : %s is not supported. Try amongst['fetch','create'] ...\033[0m" % (
                    task["get-client-keypair"]["mode"]))
            sys.exit(1)
        register(confobj, task)
        persist_state(task, verbosity, "client-keypair", confobj)
