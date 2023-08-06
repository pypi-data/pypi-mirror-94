import os
import platform
import sys
import json
import time
import uuid
import getpass
import requests
import subprocess
import nfer_secure_sandbox_cli
from shutil import copyfile
from datetime import datetime

import yaml
from flask import Flask, request
from healthcheck import HealthCheck, EnvironmentDump
from flask_cors import CORS, cross_origin

health = HealthCheck()
envdump = EnvironmentDump()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.add_url_rule("/health", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/env", "environment", view_func=lambda: envdump.run())


def get_starter_config(pipeline_conf, codebase_conf, certs_conf, sandbox_conf, algo_conf, data_conf, output_conf,
                       policy_conf):
    return [
        {
            "name": pipeline_conf["name"],
            "verbose": pipeline_conf["verbose"],
            "tasks": [
                {
                    "name": codebase_conf["desc"],
                    "populate-codebase": {
                        "mode": codebase_conf["mode"],
                        "url": codebase_conf["url"],
                        "code_path": '.' if not len(codebase_conf["code_path"]) else codebase_conf["code_path"],
                        "main_file": codebase_conf["main_file"],
                        "deps_path": '.' if not len(codebase_conf["deps_path"]) else codebase_conf["deps_path"],
                        "deps_file": codebase_conf["deps_file"],
                        "stack": codebase_conf["stack"],
                        "credentials": {
                            "username": codebase_conf["credentials"]["username"],
                            "password": codebase_conf["credentials"]["password"],
                        }
                    },
                    "register": "codebase_metadata"
                },
                {
                    "name": certs_conf["desc"],
                    "get-certs": {
                        "mode": certs_conf["mode"],
                        "action": certs_conf["action"],
                        "path": certs_conf["path"],
                        "name": certs_conf["name"]
                    },
                    "register": "cert_metadata"
                },
                {
                    "name": sandbox_conf["desc"],
                    "set-sandbox-specs": {
                        "template_id": sandbox_conf["template_id"],
                        "cert_path": sandbox_conf["cert_path"],
                        "certificate": sandbox_conf["certificate"],
                        "ca_cert_path": sandbox_conf["ca_cert_path"],
                        "ca_certificate": sandbox_conf["ca_certificate"]
                    },
                    "register": "sandbox_metadata"
                },
                {
                    "name": algo_conf["desc"],
                    "dockerize-algo": {
                        "lang": algo_conf["lang"],
                        "app_dir": algo_conf["app_dir"],
                        "deps_dir": algo_conf["deps_dir"],
                        "key_algo": algo_conf["key_algo"],
                        "sdbx_pubkey": algo_conf["sdbx_pubkey"],
                        "cert_path": algo_conf["cert_path"],
                        "certificate": algo_conf["certificate"],
                        "ca_cert_path": algo_conf["ca_cert_path"],
                        "ca_certificate": algo_conf["ca_certificate"],
                        "domain": algo_conf["domain"],
                        "docker": {
                            "image_name": algo_conf["image_name"],
                            "image_tag": algo_conf["image_tag"],
                            "image_repo": algo_conf["image_repo"]
                        }
                    },
                    "register": "algo_metadata"
                },
                {
                    "name": data_conf["desc"],
                    "get-data-projection": {
                        "sdbx_pubkey": data_conf["sdbx_pubkey"],
                        "cert_path": data_conf["cert_path"],
                        "certificate": data_conf["certificate"],
                        "ca_cert_path": data_conf["ca_cert_path"],
                        "ca_certificate": data_conf["ca_certificate"],
                        "projection_id": data_conf["projection_id"],
                        "data_identifier": data_conf["data_identifier"]
                    },
                    "register": "data_metadata"
                },
                {
                    "name": output_conf["desc"],
                    "output-encrypt-bundle": {
                        "name": output_conf["name"],
                        "id": output_conf["id"]
                    },
                    "register": "output_metadata"
                },
                {
                    "name": policy_conf["desc"],
                    "prepare-policy": {
                        "mrenclave": '{{ algo_metadata "mrenclave" }}',
                        "platform_measurement": '{{ sandbox_metadata "measurement" }}',
                        "template_id": policy_conf["template_id"],
                        "cert_path": policy_conf["cert_path"],
                        "certificate": policy_conf["certificate"],
                        "ca_cert_path": policy_conf["ca_cert_path"],
                        "ca_certificate": policy_conf["ca_certificate"],
                        "algo_image": policy_conf["algo_image"],
                        "data_loc": policy_conf["data_loc"],
                        "key_algo": policy_conf["key_algo"],
                        "algo_fspf_key": policy_conf["algo_fspf_key"],
                        "algo_fspf_tag": policy_conf["algo_fspf_tag"],
                        "out_fspf_key": policy_conf["out_fspf_key"],
                        "sdbx_pubkey": policy_conf["sdbx_pubkey"],
                        "pipeline_name": policy_conf["pipeline_name"],
                        "domain": policy_conf["domain"],
                        "output": {
                            "name": policy_conf["output_name"]
                        },
                        "dataset": {
                            "name": policy_conf["dataset_name"],
                            "cid": policy_conf["dataset_cid"],
                            "data_sym_ekey": policy_conf["data_sym_ekey"]
                        },
                        "docker": {
                            "image_name": '{{ algo_metadata "image" }}',
                            "image_tag": '{{ algo_metadata "tag" }}',
                            "image_repo": '{{ algo_metadata "repo" }}'
                        },
                        "sandbox": {
                            "instance_name": '{{ sandbox_metadata "instance_name" }}',
                            "instance_id": '{{ sandbox_metadata "instance_id" }}'
                        }
                    },
                    "register": "policy_metadata"
                },
                {
                    "name": "Submit Policy (created above)",
                    "upload-policy": {
                        "policy_doc": '{{ policy_metadata "policy_file" }}',
                        "template_id": '{{ policy_metadata "template_id" }}',
                        "pipeline_name": '{{ properties "pipeline_name" }}'
                    },
                    "register": "submission_metadata"
                },
                {
                    "name": "Trigger Policy a.k.a Pipeline",
                    "execute-policy": {
                        "entity": '{{ submission_metadata "pipeline_id" }}'
                    },
                    "register": "execution_metadata"
                },
                {
                    "name": "Retrieve Output",
                    "retrieve-output": {
                        "experiment_id": '{{ execution_metadata "exec_hash" }}',
                        "dest": "output",
                        "policy_doc": '{{ policy_metadata "policy_file" }}',
                        "pipeline_id": '{{ submission_metadata "pipeline_id" }}',
                        "fspf_key": '{{ output_metadata "fspf_key" }}'
                    },
                    "register": "retrieve_metadata"
                },
                {
                    "name": "Publish Artefacts",
                    "publish-artefacts": {
                        "format": "md",
                        "keep_original": True
                    }
                }
            ]
        }
    ]


def prepare_yaml(data):
    pipeline_conf = {
        "name": data["project_name"],
        "verbose": data["project_verbosity"]
    }
    codebase_conf = {
        "desc": "Get algo+deps code in file structure",
        "mode": "git",
        "url": data["git_url"],
        "code_path": "/".join(data["code_file"].split("/")[:-1]),
        "main_file": data["code_file"].split("/")[-1],
        "deps_path": "/".join(data["deps_file"].split("/")[:-1]),
        "deps_file": data["deps_file"].split("/")[-1],
        "stack": data["stack"],
        "credentials": {
            "username": data["creds_user"],
            "password": data["creds_pass"]
        }
    }
    certs_conf = {
        "desc": "Get Certificates (Self-Signed)",
        "mode": data["source"],
        "action": data["mode"],
        "path": "certs",
        "name": "%s-%s"%(data["project_name"], int(time.time()))
    }
    sandbox_conf = {
        "desc": "Specify Sandbox Specs",
        "template_id": data["sandboxVM"],
        "cert_path": '{{ cert_metadata "path" }}',
        "certificate": '{{ cert_metadata "cert" }}',
        "ca_cert_path": '{{ cert_metadata "path" }}',
        "ca_certificate": '{{ cert_metadata "ca_cert" }}'
    }
    algo_conf = {
        "desc": "Specify Algorithm to get Dockerized Image Encrypted (app and deps)",
        "lang": '{{ codebase_metadata "stack" }}',
        "app_dir": '{{ codebase_metadata "dest_code" }}',
        "deps_dir": '{{ codebase_metadata "dest_deps" }}',
        "key_algo": '{{ algokey_metadata "path" }}',
        "sdbx_pubkey": '{{ sandbox_metadata "public_key" }}',
        "cert_path": '{{ cert_metadata "path" }}',
        "certificate": '{{ cert_metadata "privkey" }}',
        "ca_certificate": '{{ cert_metadata "ca_cert" }}',
        "ca_cert_path": '{{ cert_metadata "path" }}',
        "domain": "www.%s.com"%(data["project_name"]),
        "image_name": data["image_name"],
        "image_tag": data["image_tag"],
        "image_repo": data["image_repo"]
    }
    data_conf = {
        "desc": "Prepare / Choose Data Projections",
        "sdbx_pubkey": '{{ sandbox_metadata "public_key" }}',
        "cert_path": '{{ cert_metadata "path" }}',
        "certificate": '{{ cert_metadata "cert" }}',
        "ca_cert_path": '{{ cert_metadata "path" }}',
        "ca_certificate": '{{ cert_metadata "ca_cert" }}',
        "projection_id": data["projection_name"],
        "data_identifier": data["input-dataprojection"]
    }
    output_conf = {
        "desc": "Prepare Output Encryption Fields",
        "name": "%s-%s-output" % ("www.%s.com"%(data["project_name"]), data["project_name"]),
        "id": str(uuid.uuid4()),
    }
    policy_conf = {
        "desc": "Prepare Policy (comprising algo, deps, data info)",
        "template_id": data["pipeline_template_id"],
        "cert_path": '{{ cert_metadata "path" }}',
        "certificate": '{{ cert_metadata "cert" }}',
        "ca_cert_path": '{{ cert_metadata "path" }}',
        "ca_certificate": '{{ cert_metadata "ca_cert" }}',
        "algo_image": '{{ algo_metadata "image_id" }}',
        "data_loc": '{{ data_metadata "arn" }}',
        "key_algo": '{{ algo_metadata "key_algo" }}',
        "platform_measurement": '{{ sandbox_metadata "measurement" }}',
        "algo_fspf_key": '{{ algo_metadata "FSPF_KEY" }}',
        "algo_fspf_tag": '{{ algo_metadata "FSPF_TAG" }}',
        "mrenclave": '{{ algo_metadata "mrenclave" }}',
        "out_fspf_key":'{{ output_metadata "fspf_key" }}',
        "sdbx_pubkey": '{{ sandbox_metadata "public_key" }}',
        "pipeline_name": '{{ properties "pipeline_name" }}',
        "domain": '{{ algo_metadata "DOMAIN" }}',
        "output_name": output_conf["name"],
        "dataset_name": '{{ data_metadata "name" }}',
        "dataset_cid": '{{ data_metadata "cid" }}',
        "data_sym_ekey": '{{ data_metadata "data_sym_ekey" }}',
        "instance_name": '{{ sandbox_metadata "instance_name" }}',
        "instance_id": '{{ sandbox_metadata "instance_id" }}',
    }
    config = get_starter_config(
        pipeline_conf, codebase_conf, certs_conf, sandbox_conf,
        algo_conf, data_conf, output_conf, policy_conf
    )
    with open("main.yml", 'w') as file:
        documents = yaml.dump(config, file)


def mkdir_essentials():
    os.makedirs("app", exist_ok=True)
    os.makedirs("build", exist_ok=True)
    os.makedirs("certs", exist_ok=True)
    os.makedirs("docker-files", exist_ok=True)
    os.makedirs("keys", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs("policy", exist_ok=True)
    os.makedirs("volumes", exist_ok=True)


def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))


@cross_origin()
@app.route("/setup_project/", methods=['POST'])
def setup_project():
    data = request.get_json()
    dirn = ""
    with open("%s/%s" % ("/Users/%s/.nfer-sandbox/" % os.environ['USER'], ".setup.db"), "r") as fin:
        for line in fin:
            dirn = line.strip().split("|")[1].strip()
    os.makedirs("%s/%s" % (dirn, data["project_name"]), exist_ok=True)
    cwd = os.getcwd()
    os.chdir("%s/%s" % (dirn, data["project_name"]))
    prepare_yaml(data)
    major = sys.version_info.major
    minor = sys.version_info.minor
    if platform.system() == "Linux":
        if is_venv():
            dest = "%s/%s"%("/".join(nfer_secure_sandbox_cli.__file__.split("/")[:-1]), "webapp/public/main.yml")
        else:
            dest = "/usr/local/lib/python%s.%s/dist-packages/nfer_secure_sandbox_cli/webapp/public/main.yml" % (major, minor)
    elif platform.system() == 'Darwin':
        if is_venv():
            dest = "%s/%s"%("/".join(nfer_secure_sandbox_cli.__file__.split("/")[:-1]), "webapp/public/main.yml")
        else:
            dest = "/usr/local/lib/python%s.%s/site-packages/nfer_secure_sandbox_cli/webapp/public/main.yml" % (major, minor)
    copyfile("main.yml", dest)
    mkdir_essentials()
    os.chdir(cwd)
    return {
               "status": "PERSISTED",
               "path": "%s/%s" % (dirn, data["project_name"])
           }, 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=5112)
