import json
import os
import sys
import shutil
import subprocess
import logging

import requests

from utils.authentication.authenticate import get_credentials
from utils.parsing.yaml import parse_var, parseable_expr
from utils.sensoriant.configuration.conf import nfer_sdbx_url, data_upload_url, google_credentials_json

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def generate_encryption_bundle(outobj, verbosity):
    shutil.rmtree("output")
    os.makedirs("output", exist_ok=True)
    logging.root.setLevel(verbosity)
    os.makedirs("output/empty-output", exist_ok=True)
    os.chdir("output/empty-output")
    sconout, sconerr = subprocess.Popen([
        "docker", "run", "--rm", "-e", "SCONE_MODE=sim", "-it", "-v", "%s/empty-dir:/empty-dir" % os.getcwd(),
        "-v", "%s/encrypted-output:/encrypted-output" % os.getcwd(),
        "sensoriant.azurecr.io/priv-comp/python-3.8.1-ubuntu:11022020", "bash", "-c",
        # rm -rf /encrypted-output/* && mkdir -p /encrypted-output &&
        "cd /encrypted-output && scone fspf create "
        "volume.fspf && scone fspf addr /encrypted-output/volume.fspf . --encrypted --kernel . && scone fspf addf "
        "/encrypted-output/volume.fspf . /empty-dir /encrypted-output/ && scone fspf encrypt volume.fspf > "
        "/empty-dir/tag_key.txt"
        #  && cat /empty-dir/tag_key.txt
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    [logger.debug('\033[94m' + s + '\033[0m') for s in sconout.decode('utf-8').split("\n")]
    fspf_tuple = [(str(line.strip().split("key:")[1]).strip(),
                   str(str(line.strip().split("key:")[0]).split("tag:")[1]).strip()) for line in
                  open("empty-dir/tag_key.txt", "r")]
    os.chdir("../..")
    fspf_key = fspf_tuple[0][0]
    fspf_tag = fspf_tuple[0][1]
    logger.debug(
        "\033[96m The \033[4mOutput Key\033[0m \033[96ma.k.a SensDecrypt Key has been generated : \033[4m%s\033[0m" % fspf_key)
    return {
        "FSPF_KEY": fspf_key,
        "FSPF_TAG": fspf_tag,
        "name": outobj["name"],
        "id": outobj["id"]
    }


def retrieve_encrypted_output(outobj):
    access_key = get_credentials("ACCESS_KEY")
    secret_key = get_credentials("SECRET_KEY")
    fspf_key = parse_var(outobj["fspf_key"]) if parseable_expr(outobj["fspf_key"]) else outobj["fspf_key"]
    dest = parse_var(outobj["dest"]) if parseable_expr(outobj["dest"]) else outobj["dest"]
    policy_doc = parse_var(outobj["policy_doc"]) if parseable_expr(outobj["policy_doc"]) else outobj["policy_doc"]
    pipeline_id = parse_var(outobj["pipeline_id"]) if parseable_expr(outobj["pipeline_id"]) else outobj["pipeline_id"]
    # experiment_id = parse_var(outobj["experiment_id"]) if parseable_expr(outobj["experiment_id"]) else outobj["experiment_id"]
    output_name = None
    with open(policy_doc, "r") as f:
        output_name = "%s-%s" % (pipeline_id, json.load(f)["output"]["name"])
        #output_name = "67d97e3a-a226-4607-b666-b74776870f59-www.mypharma.com-genentech-5050-output___1608749398"
    logger.debug("\033[94mFetching the output dataset named `%s` ...\033[0m" % (output_name))
    assert output_name is not None, "The Output Name could not be retrieved!!"
    output_ds_info = requests.get("%s/retrieve-output-info/by_name/%s" % (
        data_upload_url,
        output_name
    ), json={
        "access_key": access_key,
        "secret_key": secret_key
    },headers={'cookie':'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1',})
    output_ds_info = output_ds_info.json()
    assert output_ds_info["SUCCESS"] == True, "The Output DS doesn't exist yet!"
    if output_ds_info["SUCCESS"]:
        os.makedirs("%s/decrypt-output" % dest, exist_ok=True)
        os.makedirs("%s/gcs-creds" % os.getcwd(), exist_ok=True)
        with open("%s/gcs-creds/gcscreds.json" % os.getcwd(), 'w') as fcs:
            json.dump(google_credentials_json, fcs)
        gcspullout, gcspullerr = subprocess.Popen(
            ["docker-compose", "run", "--rm", "-e", "GCS_OBJECT_PREFIX=%s" % output_name, "-v",
             "%s/output/decrypt-input:/opt/sensoriant/gcs/pull/filesFromBucket" % os.getcwd(), "SensGcsPull"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
        logger.debug("\033[93mPrinting out the output of gcs pull encrypted output ... \033[0m")
        [logger.debug('\033[96m'+s+'\033[0m') for s in gcspullout.decode("utf-8").split("\n")]
        import in_place
        with in_place.InPlace('docker-compose.yml') as file:
            for line in file:
                line = line.replace('$SENSDECRYPT_FSPF_KEY', fspf_key)
                #line = line.replace('$SENSDECRYPT_FSPF_KEY', "60f2d6a143e1d44d84cc07a6ba5cb5a2a720185262d7569cd2ee233e5b42fc5d")
                file.write(line)
        decout, decerr = subprocess.Popen(["docker-compose", "run", "--rm", "SensDecrypt"], stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT).communicate()
        [logger.debug('\033[94m'+s+'\033[0m') for s in decout.decode("utf-8").split("\n")]
        return {
            "source_output_name": output_name,
            "source_output_id": output_ds_info["cid"],
            "output_key": fspf_key,
            "dest_output_folder": dest
        }
    else:
        logger.debug("Could not infer know-hows for output to be decrypted. Error Msg : %s for output : %s" % (
            output_ds_info["status"],
            output_ds_info["name"]
        ))
        logger.debug("Exitting!")
        sys.exit(1)


def decrypt_encrypted_output(outobj):
    # decrypt retrieved output
    return {
        "local_source_dir": "",
        "local_dest_dir": "",
        "decrypt_metadata": {}
    }
