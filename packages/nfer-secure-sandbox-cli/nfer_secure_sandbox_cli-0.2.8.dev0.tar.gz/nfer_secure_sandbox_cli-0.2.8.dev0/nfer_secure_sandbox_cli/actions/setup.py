"""
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ mkdir -p algo/apps
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ mkdir -p algo/deps
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ mkdir build
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ mkdir certs
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ mkdir docker-files
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ mkdir keys
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ mkdir logs
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ mkdir output
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ mkdir policy
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ mkdir volumes
nference@sensoriant-sandbox-new:~/nfer-cli-components/secure-sandbox-cli/examples/top-secret2$ touch main.yml
"""

import uuid

import yaml
import os
import sys
import logging
import requests

from utils.authentication.authenticate import get_credentials, authenticate
from utils.display.setup_configs import *
from utils.sensoriant.configuration.conf import *

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def init_setup_state():
    state = {
        "project": {},
        "codebase": {},
        "certificates": {}
    }
    return state


def get_allowed_pipeline_templates(access_key, secret_key):
    data = {
        "access_key": access_key,
        "secret_key": secret_key
    }
    response = requests.get("%s/datasets/pipelines/templates/" % nfer_sdbx_url, json=data)
    try:
        respobj = response.json()["pipelineTemplates"]
    except Exception as e:
        respobj = [
            {
              "name": "Sens_Pipeline_Template_Name",
              "id": "d290f1ee-6c54-4b01-90e6-d701748f0851"
            }
          ]
        return [["choose `%d` for" % (i + 1), respobj[i]['name'], respobj[i]['id']] for i in range(len(respobj))]


def get_allowed_dataset_projections(access_key, secret_key):
    data = {
        "access_key": access_key,
        "secret_key": secret_key
    }
    response = requests.get("%s/datasets/projections/" % nfer_sdbx_url, json=data)
    try:
        respobj = response.json()["dataset_projections"]
    except Exception as e:
        respobj = [
            {
                "name": "jansonn-critical-rootcanal-data",
                "id": "197b00c2-0acc-474c-ba78-4daab9bf181c"
            }
        ]
    return [["choose `%d` for" % (i + 1), respobj[i]['name'], respobj[i]['id']] for i in range(len(respobj))]


def get_allowed_platform_templates(access_key, secret_key):
    data = {
        "access_key": access_key,
        "secret_key": secret_key
    }
    response = requests.get("%s/platforms/templates/" % nfer_sdbx_url, json=data)
    try:  # TODO - this needs to be implemented
        respobj = response.json()["response"]["secureStreamPlatformTemplates"]
    except Exception as e:
        respobj = [
            {
              "name": "Sens_SecureStreamPlatform_Large_Template",
              "id": "d290f1ee-6c54-4b01-90e6-d701748f0851"
            }
        ]
    return [["choose `%d` for" % (i + 1), respobj[i]['name'], respobj[i]['id']] for i in range(len(respobj))]


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
                        "code_path": codebase_conf["code_path"],
                        "main_file": codebase_conf["main_file"],
                        "deps_path": codebase_conf["deps_path"],
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
                    "name": asymmetric_desc_default,
                    "get-client-keypair": {
                        "mode": "create",
                        "path": "keys",
                        "name": "pharma"
                    },
                    "register": "client_keypair_metadata"
                },
                {
                    "name": symmetric_desc_default,
                    "get-symmetric-algokey": {
                        "path": "keys/algokey.pem"
                    },
                    "register": "algokey_metadata"
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
                        "mrenclave": mrenclave_regexp,
                        "template_id": policy_conf["template_id"],
                        "cert_path": policy_conf["cert_path"],
                        "certificate": policy_conf["certificate"],
                        "ca_cert_path": policy_conf["ca_cert_path"],
                        "ca_certificate": policy_conf["ca_certificate"],
                        "algo_image": policy_conf["algo_image"],
                        "data_loc": policy_conf["data_loc"],
                        "pub_client": policy_conf["pub_client"],
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
                            "image_name": docker_image_default,
                            "image_tag": docker_tag_default,
                            "image_repo": docker_repo_default
                        },
                        "sandbox": {
                            "instance_name": sandbox_name_default,
                            "instance_id": sandbox_id_default,
                            "platform_measurement": sandbox_measurement_regexp
                        }
                    },
                    "register": "policy_metadata"
                },
                {
                    "name": submit_policy_desc_default,
                    "upload-policy": {
                        "policy_doc": policy_doc_default,
                        "template_id": template_id_default,
                        "pipeline_name": pipeline_name_default
                    },
                    "register": "submission_metadata"
                },
                {
                    "name": trigger_policydesc_default,
                    "execute-policy": {
                        "entity": execute_entity_regexp
                    },
                    "register": "execution_metadata"
                },
                {
                    "name": retrieve_outputdesc_default,
                    "retrieve-output": {
                        "experiment_id": experiment_id_regexp,
                        "dest": output_dest_default,
                        "policy_doc": policy_doc_default,
                        "pipeline_id": execute_entity_regexp
                    },
                    "register": "output_metadata"
                },
                {
                    "name": decrypt_outputdesc_default,
                    "decrypt-output": {
                        "from": decrypt_source_regexp,
                        "keep_original": output_keep_original_default
                    }
                }
            ]
        }
    ]


def driver(state):
    pdir = input(setup_project_1st)
    state["project"]["dir"] = pdir
    state["project"]["path"] = os.getcwd()
    os.makedirs(pdir, exist_ok=True)
    os.chdir(pdir)
    print(ack_project_1st % (pdir, os.getcwd()))
    project_name = input(unique_project_name)
    print(fetch_code_deps)
    codebase_desc = input("\033[93mEnter an optional description to identify the `Code Retrieval` with\033[0m. \033[1mPRESS ENTER\033[0m    ")
    codebase_desc = codebase_desc if len(codebase_desc) else codebase_desc_default
    codebase_mode = input("\033[93mEnter a source to get the code/deps from\033[0m. \033[1mOnly Git supported\033[0m. `\033[4mgit\033[0m` BY DEFAULT:  ")
    codebase_mode = codebase_mode if len(codebase_mode) else "git"
    git_url = input("\033[93mEnter the URL of the git repository\033[0m. e.g \033[94mhttps://github.com/<user>>/<repo-name>\033[0m:   ")
    if not len(git_url) or not git_url.startswith("https://"):
        print("\033[91mgit url is not proper. \033[1mExitting\033[0m")
        sys.exit(1)
    code_folder = input("\033[93mEnter the code folder to pick the code `py` files from\033[0m. e.g `\033[4msrc\033[0m`: ")
    code_folder = code_folder if len(code_folder) else code_folder_default
    main_file = input("\033[93mSpecify the \033[1mmain algo code\033[0m \033[93mfile name\033[0m. e.g \033[4mmain.py\033[0m. \033[1mFile must be in `src` above\033[0m:  ")
    main_file = main_file if len(main_file) else main_file_default
    deps_folder = input("\033[93mEnter the\033[0m \033[1mdeps folder\033[0m \033[93mto pick the deps from\033[0m. e.g one containing `\033[4mrequirements.txt\033[0m`: ")
    deps_folder = deps_folder if len(deps_folder) else deps_folder_default
    deps_file = input("\033[93mEnter the deps txt file e.g\033[0m \033[1m`requirements.txt`\033[0m. `requirements.txt` BY DEFAULT:   ")
    deps_file = deps_file if len(deps_file) else deps_file_default
    stack = input("\033[93mEnter the codebase `stack`\033[0m. e.g \033[4mpython\033[0m, \033[4mgo\033[0m, \033[4mR\033[0m. \033[1mOnly `python` supported\033[0m. `python` BY DEFAULT: ")
    stack = stack if len(stack) else stack_default
    creds_user = input('\033[93mEnter the git \033[1mcredentials username/email id\033[0m:    ')
    creds_pass = input('\033[93mEnter the git credentials \033[1mpassword/api_token\033[0m for normal/2FA authentication respectively:    ')
    print(ack_code_deps % os.getcwd())
    certs_desc = input("\033[93mEnter an optional description to identify the `Certificates Generation Task` with\033[0m. PRESS ENTER:  ")
    certs_desc = certs_desc if len(certs_desc) else certs_desc_default
    certs_mode = input(get_cert_mode_input)
    certs_mode = 'self-signed' if certs_mode == "1" else 'from-CA'
    certs_action = input(get_cert_action_input)
    certs_action = 'create' if certs_action == "1" else 'fetch'
    certs_path = input('\n\n\033[93mEnter the path containing / going to contain \033[1mcertificates.\033[0m  ')
    certs_name = input('\n\033[93mEnter name of the certificates\033[0m: formatted / created as : `\033[4m<cert>-privkey.pem>\033[0m`, `\033[4m<cert>-pubkey.pem\033[0m`:  ')
    if not len(certs_name):
        print("\033[91mThe certificate name cannot be empty. \033[1mExitting\033[0m")
        sys.exit(1)
    print(ack_cert_conf % (
        certs_path,
        certs_name,
        certs_name
    ))
    print(msg_success % (
        state["project"]["dir"],
        state["project"]["path"],
        state["project"]["dir"]
    ))
    print(br)
    print(inputs_ack_lvl1)
    access_key = get_credentials('ACCESS_KEY')
    secret_key = get_credentials('SECRET_KEY')
    sandbox_desc = input("\n\n\033[93mEnter an optional description to identify the `Sandbox Specification` with.\033[0m PRESS ENTER:   ")
    sandbox_desc = sandbox_desc if len(sandbox_desc) else sandbox_desc_default
    templates = get_allowed_platform_templates(access_key, secret_key)
    templates_dict = {}
    for t in templates:
        templates_dict[t[0]] = t[2]
    templates_str = "\n".join(["%s %s (%s)" % (r[0], r[1], r[2]) for r in templates])
    platform_template_id = templates_dict["choose `%s` for" % input(get_sandbox_input % templates_str)]
    pl_certs_path = input(certs_path_for_platform_input)
    pl_certs_path = '{{ cert_metadata "path" }}' if pl_certs_path == "1" else pl_certs_path
    pl_certs_name = input(certs_name_for_platform_input % (
        certs_name,
        certs_name,
        certs_name
    ))
    pl_certs_name = '{{ cert_metadata "cert" }}' if pl_certs_name == "1" else pl_certs_name
    pl_ca_certs_path = pl_ca_certs_path_default
    pl_ca_certs_name = pl_ca_certs_name_default
    print(br)
    print(inputs_ack_lvl2)
    print(docker_details_input % (
        code_folder,
        sensoriant_docker_registry
    ))
    algo_desc = input("\033[93mEnter an optional description to identify the `Dockerization Task` with.\033[0m Otherwise, PRESS ENTER  ")
    algo_desc = algo_desc if len(algo_desc) else dockerize_desc_default
    docker_repo = input("\033[0mPlease enter Name of the Docker Repo:  \033[0m")
    docker_image = input("\033[93mPlease enter Name of the Docker Image:    \033[0m")
    docker_tag = input("\033[93mPlease enter Tag associated with the Docker Image: \033[0m")
    algo_certs_path = input(
        "\033[93mSpecify the path to certs, code needs to be signed with.\033[0m PRESS ENTER to use ones create above:  ")
    algo_certs_name = input(
        "\033[93mSpecify the name of certs, code needs to be signed with.\033[0m PRESS ENTER to use ones create above: ")
    algo_certs_name = algo_certs_name if len(algo_certs_name) else certificate_regexp
    algo_certs_path = algo_certs_path if len(algo_certs_path) else cert_path_regexp
    algo_ca_cert_name = algo_ca_cert_name_default
    algo_ca_cert_path = algo_ca_cert_path_default
    algo_domain = input("\033[93mPlease enter your org's domain.\033[0m This will be deprecated soon.  ")
    print(docker_details_ack % (
        sensoriant_docker_registry,
        docker_repo,
        docker_image,
        docker_tag
    ))
    print(br)
    print(inputs_ack_lvl3)
    datasets = get_allowed_dataset_projections(access_key, secret_key)
    datasets_dict1 = {}
    datasets_dict2 = {}
    for d in datasets:
        datasets_dict1[d[0]] = d[1]
        datasets_dict2[d[0]] = d[2]
    datasets_str = "\n".join(["%s %s (%s)" % (r[0], r[1], r[2]) for r in datasets])
    dataset_input_no = input(get_dataset_input % datasets_str)
    dataset_projection_id = datasets_dict2["choose `%s` for" % dataset_input_no]
    dataset_projection_name = datasets_dict1["choose `%s` for" % dataset_input_no]
    print(dataset_conf_ack % (
        dataset_projection_id,
        dataset_projection_name
    ))
    data_desc = input("\033[93mEnter an optional description to identify the `Data Projection Task` with\033[0m. Otherwise, PRESS ENTER    ")
    data_desc = data_desc if len(data_desc) else data_desc_default
    data_certs_path = input(
        "\033[93mSpecify the path to certs, code needs to be signed with\033[0m. PRESS ENTER to \033[1muse ones create above\033[0m  ")
    data_certs_name = input(
        "\033[93mSpecify the name of certs, code needs to be signed with\033[0m. PRESS ENTER to \033[1muse ones create above\033[0m  ")
    data_certs_name = data_certs_name if len(data_certs_name) else certificate_regexp
    # data_certs_path = data_certs_path if len(data_certs_name) else cert_path_regexp
    data_certs_path = cert_path_regexp
    data_ca_cert_name = data_ca_cert_name_default
    data_ca_cert_path = data_ca_cert_path_default
    print(br)
    print(inputs_ack_lvl4)
    pipeline_templates = get_allowed_pipeline_templates(access_key, secret_key)
    pipeline_templates_dict1 = {}
    pipeline_templates_dict2 = {}
    for t in pipeline_templates:
        pipeline_templates_dict1[t[0]] = t[2]
        pipeline_templates_dict2[t[0]] = t[1]
    pipeline_templates_str = "\n".join(["%s %s (%s)" % (r[0], r[1], r[2]) for r in pipeline_templates])
    pipeline_input_no = input("""
    \033[93mPlease enter the policy template id\033[0m. By default, we only choose the below:
    
    \033[94m%s\033[0m
    
    """ % pipeline_templates_str)
    pipeline_template_id = pipeline_templates_dict1["choose `%s` for" % pipeline_input_no]
    os.makedirs("keys", exist_ok=True)
    os.makedirs("algo/app", exist_ok=True)
    os.makedirs("algo/deps", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("certs", exist_ok=True)
    os.makedirs("docker-images", exist_ok=True)
    os.makedirs("docker-files", exist_ok=True)
    os.makedirs("policy", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/empty-output", exist_ok=True)
    print(inputs_ack_lvl5 % (
        code_folder,
        deps_folder,
        certs_name,
        certs_name
    ))
    pipeline_conf = {
        "name": project_name,
        "verbose": verbpose_default
    }
    codebase_conf = {
        "desc": codebase_desc,
        "mode": codebase_mode,
        "url": git_url,
        "code_path": code_folder,
        "main_file": main_file,
        "deps_path": deps_folder,
        "deps_file": deps_file,
        "stack": stack,
        "credentials": {
            "username": creds_user,
            "password": creds_pass
        }
    }
    certs_conf = {
        "desc": certs_desc,
        "mode": certs_mode,
        "action": certs_action,
        "path": certs_path,
        "name": certs_name
    }
    sandbox_conf = {
        "desc": sandbox_desc,
        "template_id": platform_template_id,
        "cert_path": pl_certs_path,
        "certificate": pl_certs_name,
        "ca_cert_path": pl_ca_certs_path,
        "ca_certificate": pl_ca_certs_name
    }
    algo_conf = {
        "desc": algo_desc,
        "lang": algo_lang_default,
        "app_dir": algo_apps_dir_default,
        "deps_dir": algo_deps_dir_default,
        "key_algo": key_algo_default,
        "sdbx_pubkey": sdbx_pubkey_default,
        "cert_path": algo_certs_path,
        "certificate": algo_certs_priv_regexp,
        "ca_certificate": algo_ca_cert_name,
        "ca_cert_path": algo_ca_cert_path,
        "domain": algo_domain,
        "image_name": docker_image,
        "image_tag": docker_tag,
        "image_repo": docker_repo
    }
    data_conf = {
        "desc": data_desc,
        "sdbx_pubkey": sdbx_pubkey_default,
        "cert_path": data_certs_path,
        "certificate": data_certs_name,
        "ca_cert_path": data_ca_cert_path,
        "ca_certificate": data_ca_cert_name,
        "projection_id": dataset_projection_id,
        "data_identifier": dataset_projection_name
    }
    output_conf = {
        "desc": output_encr_desc_default,
        "name": "%s-%s-output" % (algo_domain, project_name),
        "id": str(uuid.uuid4()),
    }
    policy_conf = {
        "desc": policy_prep_desc_default,
        "template_id": pipeline_template_id,
        "cert_path": cert_path_regexp,
        "certificate": certificate_regexp,
        "ca_cert_path": ca_cert_path_regexp,
        "ca_certificate": ca_certificate_regexp,
        "algo_image": algo_image_regexp,
        "data_loc": data_loc_regexp,
        "pub_client": pub_client_regexp,
        "key_algo": key_algo_regexp,
        "platform_measurement": sandbox_measurement_regexp,
        "algo_fspf_key": algo_fspf_key_regexp,
        "algo_fspf_tag": algo_fspf_tag_regexp,
        "mrenclave": mrenclave_regexp,
        "out_fspf_key": out_fspf_key_regexp,
        "sdbx_pubkey": sdbx_pubkey_default,
        "pipeline_name": pipeline_name_regexp,
        "domain": domain_regexp,
        "output_name": output_conf["name"],
        "dataset_name": dataset_name_regexp,
        "dataset_cid": dataset_cid_regexp,
        "data_sym_ekey": data_sym_ekey_regexp,
        "instance_name": sandbox_name_default,
        "instance_id": sandbox_id_default,
    }
    config = get_starter_config(
        pipeline_conf, codebase_conf, certs_conf, sandbox_conf,
        algo_conf, data_conf, output_conf, policy_conf
    )
    with open("main.yml", 'w') as file:
        documents = yaml.dump(config, file)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def setup():
    logger.setLevel(logging.INFO)
    print(msg_intro)
    state = init_setup_state()
    driver(state)
