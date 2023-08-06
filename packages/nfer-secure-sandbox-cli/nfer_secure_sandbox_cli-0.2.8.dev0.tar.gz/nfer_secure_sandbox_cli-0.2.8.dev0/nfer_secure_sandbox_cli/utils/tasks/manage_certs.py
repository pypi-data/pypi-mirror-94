from OpenSSL import crypto, SSL
import os
import sys
import random
import subprocess
from utils.state.manage_state import read_state, persist_state
from utils.logging.logger import log
from utils.state.manage_state import register
from utils.sensoriant.configuration.conf import *
from utils.authentication.authenticate import create_CSR, get_credentials
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def get_certs(task, verbosity):
    logging.root.setLevel(verbosity)
    access_key = get_credentials('ACCESS_KEY')
    secret_key = get_credentials('SECRET_KEY')
    if read_state(task, verbosity, 'certs'):
        if task["get-certs"]["mode"] == "from-CA":  # modify basis need/logic for caCert, bundle elements etc.
            confobj = {
                "path": task["get-certs"]["path"],  # assume .crt is cert and .key is privkey
                "cert": task["get-certs"]["name"] if str(task["get-certs"]["name"]).endswith(".cert") else "%s.cert" % (
                    task["get-certs"]["name"]),
                "privkey": [f for f in os.listdir(task["get-certs"]["path"]) if f.endswith('.key')][0],
                "ca_cert": task["get-certs"]["ca_cert"] if task["get-certs"]["ca_cert"] else ""
                # need ca_cert validations
            }
            verout, vererr = subprocess.Popen(
                ["openssl", "verify", "%s/%s.cert" % (task["get-certs"]["path"], task["get-certs"]["name"])],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
            if verout == "":
                logger.error("\033[91mSome problems verifying the CA Issued cert `%s/%s.pem`\033[0m" % (
                    task["get-certs"]["path"],
                    task["get-certs"]["name"]
                ))
            else:
                logger.debug("\033[92mThe certificate `%s/%s.cert` issued from CA, has been verified. \033[0m" % (
                    task["get-certs"]["path"], task["get-certs"]["name"]))
        elif task["get-certs"]["mode"] == "self-signed":
            if task["get-certs"]["action"] == "create":
                os.makedirs(task["get-certs"]["path"], exist_ok=True)
                privout, priverr = subprocess.Popen(["openssl","genrsa","-out","%s/%s-privkey.pem"%(task["get-certs"]["path"], task["get-certs"]["name"]),"2048"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
                pubout, puberr = subprocess.Popen(
                    ["openssl", "rsa", "-in", "%s/%s-privkey.pem" % (task["get-certs"]["path"], task["get-certs"]["name"]),
                     "-pubout","-out","%s/%s-pubkey.pem"%(task["get-certs"]["path"], task["get-certs"]["name"])], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
                # out, err = subprocess.Popen(
                #     ["openssl", "req", "-nodes", "-new", "-x509", "-keyout",
                #      "%s/%s.key" % (task["get-certs"]["path"], task["get-certs"]["name"]),
                #      "-out",
                #      "%s/%s.cert" % (task["get-certs"]["path"], task["get-certs"]["name"]), "-subj",
                #      "/C=%s/ST=%s/L=%s/O=%s/OU=%s/CN=%s/emailAddress=%s" % (
                #          ss_ca_conf["country"], ss_ca_conf["state"], ss_ca_conf["city"], ss_ca_conf["org"],
                #          ss_ca_conf["unit"], ss_ca_conf["cn"], ss_ca_conf["email"])],
                #     stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
                # if out.decode("utf-8") == "":  # TODO watch out for better error response here.
                #     log("Some error with following command: `%s` from dir: `%s`" % (
                #         ','.join(["openssl", "req", "-nodes", "-new", "-x509", "-keyout",
                #                   "%s.key" % task["get-certs"]["name"],
                #                   "-out",
                #                   "%s.cert" % task["get-certs"]["name"], "-subj",
                #                   "/C=%s/ST=%s/L=%s/O=%s/OU=%s/CN=%s/emailAddress=%s" % (
                #                       ss_ca_conf["country"], ss_ca_conf["state"], ss_ca_conf["city"], ss_ca_conf["org"],
                #                       ss_ca_conf["unit"], ss_ca_conf["cn"], ss_ca_conf["email"])]),
                #         str(os.getcwd())
                #     ), True)
                if privout.decode('utf-8').startswith('Generating RSA private key') and pubout.decode('utf-8').startswith('writing RSA key'):
                    logger.debug("\033[92mGenerated the PrivKey and ss-cert inside directory : `%s`\033[0m" % (task["get-certs"]["path"]))
                    res = create_CSR(task["get-certs"], {
                        "access_key": access_key,
                        "secret_key": secret_key
                    })
                    if res.status_code == 200:
                        logger.debug("\033[92mUploaded the cert in path : `%s/%s.cert` with ack : `%s`\033[0m" % (task["get-certs"]["path"], task["get-certs"]["name"], res.content.decode('utf-8')))
                    else:
                        logger.debug("\033[91mSome error uploading the cert `%s.cert`. err msg : `%s`\033[0m" % (
                            task["get-certs"]["name"], res.content.decode('utf-8')))
                        sys.exit(1)
                else:
                    logger.debug("\033[91mSome Problems in generating the ss-cert using Openssl with following cmds : `%s` and `%s`\033[0m"%(
                        ' '.join(["openssl", "genrsa", "-out",
                         "%s/%s-privkey.pem" % (task["get-certs"]["path"], task["get-certs"]["name"]), "2048"]),
                        ' '.join(["openssl", "rsa", "-in", "%s/%s-privkey.pem" % (task["get-certs"]["path"], task["get-certs"]["name"]),
                     "-pubout","-out","%s/%s-pubkey.pem"%(task["get-certs"]["path"], task["get-certs"]["name"])])
                    ))
                    sys.exit(1)
            elif task["get-certs"]["action"] == "fetch":
                res = create_CSR((task["get-certs"], {
                    "access_id": access_key,
                    "secret_key": secret_key
                }))
                if res.status_code == 200:
                    logger.debug("\033[92mThe uploaded cert `\033[4m%s-pubkey.pem\033[0m` is valid. \033[0m"% task["get-certs"]["name"])
                else:
                    logger.error("\033[91mSome problems with cert `%s-pubkey.pem`. Reach support at `\033[4m%s\033[0m`\033[0m" % (
                        task["get-certs"]["path"], support_email_id))
            else:
                os.makedirs(task["get-certs"]["path"], exist_ok=True)  # could be delegated to another function/module
                pubkey = os.path.join(task["get-certs"]["path"], "%s.crt" % task["get-certs"]["name"])  # create .crt
                privkey = os.path.join(task["get-certs"]["path"], "%s.key" % task["get-certs"]["name"])  # create .key
                k = crypto.PKey()
                k.generate_key(crypto.TYPE_RSA, 2048)
                serialnumber = random.getrandbits(64)
                # create a self-signed cert
                cert = crypto.X509()
                cert.get_subject().C = "US";
                cert.get_subject().ST = "IL"
                cert.get_subject().L = "CHICAGO";
                cert.get_subject().O = "NFERENCE"
                cert.get_subject().OU = "LOCUS";
                cert.get_subject().CN = task["get-certs"]["name"]
                cert.set_serial_number(serialnumber)
                cert.gmtime_adj_notBefore(0);
                cert.gmtime_adj_notAfter(31536000)
                cert.set_issuer(cert.get_subject());
                cert.set_pubkey(k);
                cert.sign(k, 'sha512')
                pub = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
                priv = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
                open(pubkey, "wt").write(pub.decode("utf-8"))
                open(privkey, "wt").write(priv.decode("utf-8"))
        else:
            logger.critical(
                "\033[91mThis mode for certificates : \033[4m%s\033[0m \033[91mis not supported. Try amongst: \033[1m['from-CA','self-signed']\033[0m \033[91m...\033[0m" % (
                    task["get-certs"]["mode"])
            )
            sys.exit(1)
        confobj = {
            "path": task["get-certs"]["path"],
            "cert": "%s-pubkey.pem" % task["get-certs"]["name"],  # keep it cert or keey it .pub preferably
            "privkey": "%s-privkey.pem" % task["get-certs"]["name"],
            "ca_cert": ""  # need to solve the ca_cert for self-signed case
        }
        register(confobj, task)
        persist_state(task, verbosity, "certs", confobj)
