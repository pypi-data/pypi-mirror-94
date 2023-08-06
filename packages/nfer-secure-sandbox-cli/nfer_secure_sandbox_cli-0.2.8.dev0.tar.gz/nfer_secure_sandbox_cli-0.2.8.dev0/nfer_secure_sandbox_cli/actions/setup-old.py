import yaml
import os
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def get_starter_config():
    # print comments also.
    return [
        {
            "name": "dummy-data echo-algo v0",
            "verbose": True,
            "tasks": [
                {
                    "name": "Get Certificates (Self-Signed)",
                    "get-certs": {
                        "mode": "self-signed",
                        "path": "certs",
                        "name": "my-self-signed-certs"
                    },
                    "register": "cert_metadata"
                },
                {
                    "name": "Get Assymetric Pair for client",
                    "get-client-keypair": {
                        "mode": "create",
                        "path": "keys"
                    },
                    "register": "clint_keypair"
                },
                {
                    "name": "Specify Sandbox Specs",
                    "set-sandbox-specs": {
                        "template_id:": "standard-small-4cpus-16GBs-160GBs-TPM_GCP"
                    },
                    "register": "sandbox_metadata"
                },
                {
                    "name": "Prepare / Choose Data Projections",
                    "get-data-projection": {
                        "sdbx_pubkey": "'{{ sandbox_metadata[\"pubkey\"] }}'",
                        "projection_id": "dqw3000bca"
                    },
                    "register": "data_metadata"
                },
                {
                    "name": "Specify Algorithm to get Dockerized Image Encrypted (app and deps)",
                    "dockerize-algo": {
                        "lang": "python3",
                        "apps_dir": "algo",
                        "deps_dir": "deps"
                    },
                    "register": "algo_metadata"
                },
                {
                    "name": "Prepare Policy (comprising algo, deps, data info)",
                    "prepare-policy": {
                        "cert_path": "'{{ cert_metadata[\"path\"] }}'",
                        "algo_image": "'{{ algo_metadata[\"image_id\"] }}'",
                        "data_loc": "'{{ data_metadata[\"arn\"] }}'",
                        "pub_client": "'{{ client_keypair[\"pubkey\"] }}'",
                        "key_algo": "'{{ algo_metadata[\"key_algo\"] }}'"
                    },
                    "register": "policy_metadata"
                },
                {
                    "name": "Submit Policy(created above)",
                    "upload-policy": {
                        "policy_doc": "'{{ policy_metadata[\"doc\"] }}'",
                        "policy_bundle": "'{{ policy_metadata[\"bundle\"] }}'"
                    },
                    "register": "submission_metadata"
                },
                {
                    "name": "Trigger Policy a.k.a Pipeline",
                    "execute-policy": {
                        "entity": "'{{ submission_metadata[\"pipeline_id\"] }}'"
                    },
                    "register": "execution_metadata"
                },
                {
                    "name": "Retrieve Output",
                    "retrieve-output": {
                        "experiment_id": "'{{ execution_metadata[\"exec_hash\"] }}'",
                        "dest": "output"
                    },
                    "register": "output_metadata"
                },
                {
                    "name": "Decrypt Output",
                    "decrypt-output": {
                        "from": "'{{ output_metadata[\"dest\"] }}'",
                        "keep_original": True
                    }
                }
            ]
        }
    ]


def setup():
    logger.setLevel(logging.INFO)
    logger.info("Setting up a starter project in `current directory` ...")
    get_starter_config()
    with open("main.yml", 'w') as file:
        documents = yaml.dump(get_starter_config(), file)
    logger.info("created an example runbook : `main.yml` in the `current directory`")
    os.makedirs("keys", exist_ok=True)
    os.makedirs("algo", exist_ok=True)
    os.makedirs("deps", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("certs", exist_ok=True)
    os.makedirs("docker-images", exist_ok=True)
    logger.info("...")
    logger.info("created optional folders `keys`, `algo`, `deps`, `certs` in the `current directory`")


