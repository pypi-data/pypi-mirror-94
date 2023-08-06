import os
import sys
import time
import json
import base64
import traceback

import requests
import subprocess

from utils.logging.logger import log
from utils.parsing.yaml import parse_var, parseable_expr
from utils.authentication.authenticate import get_credentials, authenticate
from utils.sensoriant.configuration.conf import *

import logging

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def prepare_policy_json(pipeline_name, dockobj, algo_conf, data_conf, output_conf, sandbox_conf):
    scli_digest = str(
        str(open([str("build/%s"%f) for f in os.listdir("%s/build/"%os.getcwd()) if str(f).endswith("-enc-meas.txt")][0], "r").read()).split(
            'sha256:')[-1])
    scli_epk_file = [str("build/%s"%f) for f in os.listdir("%s/build/"%os.getcwd()) if str(f).endswith('-enc-priv.pem-ek')][
        0]  # `base64 -w0 $SCLI_EPK_FILE`
    inf = open(scli_epk_file, "r").read().encode('ascii')
    scli_epk_base64 = base64.b64encode(inf).decode('ascii')
    scli_algo_fspf_ekey = open("build/algorithm.decryptionKeys.enclave.decryptionKey-eb", "r").read().encode('ascii')
    scli_algo_fspf_ekey = base64.b64encode(scli_algo_fspf_ekey).decode('ascii')
    scli_out_fspf_ekey = open("build/output.encryptionkey.symmetrickey-eb", "r").read().encode('ascii')
    scli_outp_sym_ekey = base64.b64encode(scli_out_fspf_ekey).decode('ascii')
    t = os.system("cat %s | sed -e 's/\\n/\\\n/g' > %s/build/tmpfile" % (algo_conf["cert_pub_file"], os.getcwd()))
    scli_ver_key = open("%s/build/tmpfile" % os.getcwd()).read()
    os.remove("%s/build/tmpfile" % os.getcwd())
    assert t == 0, "Something wrong with sed'ing the client pub key"
    policy_json = {
        "pipelineName": pipeline_name,
        "algorithm": {
            "id": "https://%s/%s/%s.enc:%s@%s" % (
                dest_sens_docker_registry, dockobj['image_repo'], dockobj['image_name'],
                dockobj['image_tag'], scli_digest
            ),
            "decryptionKeys": {
                "container": {
                    "filesystemMeasurement": scli_digest,
                    "secureStreamPlatformMeasurement": sandbox_conf["platform_measurement"],
                    "encryptedDecryptionKey": scli_epk_base64
                },
                "enclave": {
                    "filesystemMeasurement": algo_conf["algo_fspf_tag"],
                    "enclaveMeasurement":  algo_conf["mrenclave"],
                    "encryptedDecryptionKey": scli_algo_fspf_ekey
                }
            },
            "signatureVerification": {
                "publicKey": scli_ver_key,
                "domain": algo_conf["domain"]
            }
        },
        "dataset": {
            "name": data_conf["dataset_name"],
            "id": data_conf["dataset_id"],
            "decryptionKey": {
                "name": "dataset.encryptionkey.symmetrickey",
                "encryptedSymmetricKey": data_conf["scli_data_sym_ekey"]

            }
        },
        "output": {
            "name": "%s___%s" % (output_conf['output_name'], int(time.time())),
            "encryptionKey": {
                "name": "output.encryptionkey.symmetrickey",
                "encryptedSymmetricKey": scli_outp_sym_ekey
            },
            "receiversPublicKey": scli_ver_key

        },
        "secureStreamPlatform": {
            "name": sandbox_conf["instance_name"],
            "id": sandbox_conf["instance_id"]
        }
    }
    with open("policy/%s" % pipeline_name, "w") as fp:
        json.dump(policy_json, fp)
    return "policy/%s" % pipeline_name


def prepare_signed_policy(policyobj, verbosity):
    logging.root.setLevel(verbosity)
    os.makedirs("policy", exist_ok=True)
    image_name = parse_var(policyobj["docker"]["image_name"]) if parseable_expr(policyobj["docker"]["image_name"]) else \
        policyobj["docker"]["image_name"]
    image_repo = parse_var(policyobj["docker"]["image_repo"]) if parseable_expr(policyobj["docker"]["image_repo"]) else \
        policyobj["docker"]["image_repo"]
    image_tag = parse_var(policyobj["docker"]["image_tag"]) if parseable_expr(policyobj["docker"]["image_repo"]) else \
        policyobj["docker"]["image_tag"]
    dockobj = {
        'image_name': image_name,
        'image_repo': image_repo,
        'image_tag': image_tag,
    }
    platform_measurement = parse_var(policyobj["platform_measurement"]) if parseable_expr(policyobj["platform_measurement"]) else \
        policyobj["platform_measurement"]
    scli_data_sym_ekey = parse_var(policyobj["dataset"]["data_sym_ekey"]) if parseable_expr(
        policyobj["dataset"]["data_sym_ekey"]) else \
        policyobj["dataset"]["data_sym_ekey"]
    output_name = parse_var(policyobj["output"]["name"]) if parseable_expr(policyobj["output"]["name"]) else \
        policyobj["output"]["name"]
    dataset_id = parse_var(policyobj["dataset"]["cid"]) if parseable_expr(policyobj["dataset"]["cid"]) else \
        policyobj["dataset"]["cid"]
    dataset_name = parse_var(policyobj["dataset"]["name"]) if parseable_expr(policyobj["dataset"]["name"]) else \
    policyobj["dataset"]["name"]
    domain = parse_var(policyobj["domain"]) if parseable_expr(policyobj["domain"]) else policyobj[
        "domain"]
    pipeline_name = parse_var(policyobj["pipeline_name"]) if parseable_expr(policyobj["pipeline_name"]) else policyobj[
        "pipeline_name"]
    template_id = parse_var(policyobj["template_id"]) if parseable_expr(policyobj["template_id"]) else policyobj[
        "template_id"]
    public_key = parse_var(policyobj["sdbx_pubkey"]) if parseable_expr(policyobj["sdbx_pubkey"]) else policyobj[
        "sdbx_pubkey"]
    cert_path = parse_var(policyobj["cert_path"]) if parseable_expr(policyobj["cert_path"]) else policyobj[
        "cert_path"]
    certificate = parse_var(policyobj["certificate"]) if parseable_expr(policyobj["certificate"]) else policyobj[
        "certificate"]
    ca_cert_path = parse_var(policyobj["ca_cert_path"]) if parseable_expr(policyobj["ca_cert_path"]) else policyobj[
        "ca_cert_path"]
    ca_certificate = parse_var(policyobj["ca_certificate"]) if parseable_expr(policyobj["ca_certificate"]) else \
        policyobj[
            "ca_certificate"]
    algo_fspf_key = parse_var((policyobj["algo_fspf_key"])) if parseable_expr(policyobj["algo_fspf_key"]) else \
        policyobj["algo_fspf_key"]
    mrenclave = parse_var((policyobj["mrenclave"])) if parseable_expr(policyobj["mrenclave"]) else \
        policyobj["mrenclave"]
    algo_fspf_tag = parse_var((policyobj["algo_fspf_tag"])) if parseable_expr(policyobj["algo_fspf_tag"]) else \
        policyobj["algo_fspf_tag"]
    out_fspf_key = parse_var((policyobj["out_fspf_key"])) if parseable_expr(policyobj["out_fspf_key"]) else policyobj[
        "out_fspf_key"]
    instance_name = parse_var((policyobj["sandbox"]["instance_name"])) if parseable_expr(
        policyobj["sandbox"]["instance_name"]) else policyobj["sandbox"]["instance_name"]
    instance_id = parse_var((policyobj["sandbox"]["instance_id"])) if parseable_expr(
        policyobj["sandbox"]["instance_id"]) else policyobj["sandbox"]["instance_id"]
    out_fspf_key = parse_var((policyobj["out_fspf_key"])) if parseable_expr(policyobj["out_fspf_key"]) else policyobj[
        "out_fspf_key"]
    pub_key_file = open("keys/machine-pub.pem", "w")
    pub_key_file.write("%s\n" % str(public_key))
    pub_key_file.close()
    ca_cert_blob = "" if ca_certificate == "" else open("%s/%s" % (ca_cert_path, ca_certificate), "r").read()
    cert_pub_file = "%s/%s" % (cert_path, certificate)
    cert_blob = open(cert_pub_file, "r").read()
    scli_ipk_file = [str("build/%s"%f) for f in os.listdir("%s/build/"%os.getcwd()) if str(f).endswith("-enc-priv.pem")][0]
    os.environ["SCLI_ALGO_DIR"] = os.getcwd()
    polout, polerr = subprocess.Popen(
        ["scli.sh", "sensec", "ek", "--ipk", "/algo/%s" % scli_ipk_file, "--mpk", "/algo/keys/machine-pub.pem",
         "--outdir", "%s/build/" % "/algo/"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    [logger.debug('\033[94m'+s+'\033[0m') for s in polout.decode('utf-8').split("\n")]
    if polout.decode('utf-8') is not None:  # TODO Don't know why polout is NoneType
        logger.debug("\033[92mSuccessfully prepared the algo policy, as file `%s`\033[0m" % (
            [str(f) for f in os.listdir("%s/build/"%(os.getcwd())) if str(f).endswith("-enc-priv.pem-ek")][0]
        ))
    else:
        logger.debug("\033[91mSome problems preparing the policy..\033[0m")
    algo_decr_key = open("keys/algorithm.decryptionKeys.enclave.decryptionKey", "w")
    algo_decr_key.write(algo_fspf_key)
    algo_decr_key.close()
    out_encr_key = open("keys/output.encryptionkey.symmetrickey", "w")
    out_encr_key.write(out_fspf_key)
    out_encr_key.close()
    blobalgoout, blobalgoerr = subprocess.Popen([
        "scli.sh", "sensec", "ek", "--blob", "/algo/keys/algorithm.decryptionKeys.enclave.decryptionKey",
        "--mpk", "/algo/keys/machine-pub.pem", "--outdir", "%s/build/" %os.getcwd()], stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT).communicate()
    [logger.debug('\033[94m'+s+'\033[0m') for s in blobalgoout.decode('utf-8').split("\n")]
    bloboutout, blobouterr = subprocess.Popen([
        "scli.sh", "sensec", "ek", "--blob", "/algo/keys/output.encryptionkey.symmetrickey",
        "--mpk", "/algo/keys/machine-pub.pem", "--outdir", "%s/build/" %os.getcwd()
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    [logger.debug('\033[94m'+s+'\033[0m') for s in bloboutout.decode('utf-8').split("\n")]
    data_conf = {
        'dataset_name': dataset_name,
        'dataset_id': dataset_id,
        'scli_data_sym_ekey': scli_data_sym_ekey
    }
    algo_conf = {
        'algo_fspf_tag': algo_fspf_tag,
        'cert_pub_file': cert_pub_file,
        'domain': domain,
        "mrenclave": mrenclave
    }
    output_conf = {
        'output_name': output_name
    }
    sandbox_conf = {
        "instance_name": instance_name,
        "instance_id": instance_id,
        "platform_measurement": platform_measurement
    }
    try:
        policy_doc = prepare_policy_json(pipeline_name, dockobj, algo_conf, data_conf, output_conf, sandbox_conf)
        return {
            "algo_decryptionkey": "keys/algorithm.decryptionKeys.enclave.decryptionKey",
            "out_encryptionkey": "keys/output.encryptionkey.symmetrickey",
            "algo_blob": "build/algorithm.decryptionKeys.enclave.decryptionKey-eb",
            "out_blob": "build/output.encryptionkey.symmetrickey-eb",
            "template_id": template_id,
            "policy_file": policy_doc
        }
    except Exception as e:
        traceback.print_exc()
        logger.error('\033[91m'+str(e)+'\033[0m')
        retconf =  {
            "algo_decryptionkey": "",
            "out_encryptionkey": "",
            "algo_blob": "",
            "out_blob": "",
            "template_id": template_id,
            "policy_file": ""
        }
        sys.exit(1)
    # return { # TODO it should rather be a build no. wherein all these files copied
    #     "policy_file" : [str(f) for f in os.listdir(os.getcwd()) if str(f).startswith('.pem-ek')][0]
    # }


def upload_signed_policy(policyobj, verbosity):
    logging.root.setLevel(verbosity)
    access_key = get_credentials('ACCESS_KEY')
    secret_key = get_credentials('SECRET_KEY')
    template_id = parse_var(policyobj["template_id"]) if parseable_expr(policyobj["template_id"]) else \
        policyobj["template_id"]
    pipeline_name = parse_var(policyobj["pipeline_name"]) if parseable_expr(policyobj["pipeline_name"]) else \
        policyobj["pipeline_name"]
    policy_file = parse_var(policyobj["policy_doc"]) if parseable_expr(policyobj["policy_doc"]) else \
        policyobj["policy_doc"]
    with open(policy_file) as f:
        policy_json = json.load(f)
    authobj = authenticate({
        "access_key": access_key,
        "secret_key": secret_key
    })
    policy_json["message"] = authobj["message"]
    policy_json["email"] = authobj["email"]
    policy_json["name"] = pipeline_name
    if authobj["message"] == "Authenticated":
        response = requests.post(
            '%s/pipelines/create/%s' % (
                nfer_sdbx_url,
                template_id
            ),
            json=policy_json, headers={'cookie':'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1',})
        return response.json()
    else:
        logger.error("\033[91mSome problems authenticating the user. Exitting\033[0m")
        sys.exit(1)
