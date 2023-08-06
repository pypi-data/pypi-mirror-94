"""
either use epochs with the image tags -> docker system prune
should you not want that - then after the "push", rmi the image also on local.
"""
import time

import requests
import docker
import os
import sys
import json
import glob
import shutil
import subprocess
from utils.logging.logger import log
from configparser import ConfigParser
from utils.parsing.yaml import parse_var, parseable_expr
from utils.authentication.authenticate import get_credentials, authenticate
from utils.sensoriant.configuration.conf import *
import logging

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def prepare_dockercompose_yaml(key, tag, code_path, dockobj, ep):
    code_file = ''
    for f in os.listdir(code_path):
        code_file = '%s/%s' % (code_path, str(f))
    dc_yml_content = """
version: '3.2'
services:
    SensDecrypt:
      image: sensoriant.azurecr.io/nference/sensdecrypt:%s
      environment:
        - SCONE_MODE=sim
        - SCONE_SYSLIBS=1
        - SCONE_LOG=0
        - SCONE_ALLOW_DLOPEN=2
      command: /copyfiles -i /decrypt-input -o /decrypt-output -k $SENSDECRYPT_FSPF_KEY
      volumes:
        - ./output/decrypt-input:/decrypt-input
        - ./output/decrypt-output:/decrypt-output
        - /usr/local/cuda-11.2/bin:/usr/local/cuda-11.2/bin
        - /usr/local/cuda-11.2/lib64:/usr/local/cuda-11.2/lib64
    SensGcsPull:
      image: sensoriant.azurecr.io/nference/sensgcspull:%s
      environment:
        - GCS_BUCKET_NAME=%s
        - GCS_OUTPUT_PATH=/opt/sensoriant/gcs/pull/filesFromBucket
        - GCS_OBJECT_PREFIX
        - GOBIN
        - GOOGLE_APPLICATION_CREDENTIALS=/opt/sensoriant/gcs/pull/credentials/gcscreds.json
        - MODE
      command: bash -c "/opt/sensoriant/gcs/pull/start.sh"
      volumes:
        - ./gcs-creds:/opt/sensoriant/gcs/pull/credentials
        # - ./volumes/datasets:/opt/sensoriant/gcs/pull/datasets
    SensCli:
        image: sensoriant.azurecr.io/nference/scli:%s
        network_mode: "host"
        command: bash -c "./start.sh"
        volumes:
            - %s:/algo
    algorithm:
        build:
            context: .
            dockerfile: docker-files/Dockerfile
        image: %s/%s/%s:%s
        shm_size: '2gb'
        devices:
         - /dev/nvidia0:/dev/nvidia0
         - /dev/nvidiactl:/dev/nvidiactl
         - /dev/nvidia-uvm:/dev/nvidia-uvm
        environment:
         - NVIDIA_VISIBLE_DEVICES=0,1
         - PATH=/usr/local/cuda-11.2/bin:$PATH
         - LD_LIBRARY_PATH=/usr/local/cuda-11.2/lib64
         - SCONE_MODE=sim
         - SCONE_HEAP=3G
         - SCONE_FORK=1
         - SCONE_SYSLIBS=1
         - SCONE_LOG=0
         - SCONE_ALLOW_DLOPEN=2
         - SCONE_FORK_OS=1
         - SCONE_IGNORE_SIGHUP=1
         - SCONE_FSPF_KEY=%s
         - SCONE_FSPF_TAG=%s
         - SCONE_FSPF=/fspf.pb
        volumes:
         - /usr/local/cuda-11.2/bin:/usr/local/cuda-11.2/bin
         - /usr/local/cuda-11.2/lib64:/usr/local/cuda-11.2/lib64
         - ./volumes/algorithm-output/:/algorithm-output
         - ./volumes/algorithm-input:/algorithm-input
        command: /root/miniconda/bin/python3 /%s --data-dir /algorithm-input --output /algorithm-output
    """ % (
        version,
        version,
        sens_storage_bucket,
        version,
        os.getcwd(),
        client_docker_registry,  # client_docker_registry
        dockobj["image_repo"],
        dockobj["image_name"],
        dockobj["image_tag"],
        # ep,
        key,
        tag,
        code_file
    )
    dcyf = open("docker-compose.yml", "w")
    dcyf.write(dc_yml_content)
    dcyf.close()


def prepare_algo_dockerfile(confobj):
    code_file = confobj["dest_code_file"]
    #     dockerfile_algo_content = """
    # FROM sensoriant.azurecr.io/nference/algorithm-base:test
    # ADD image_files /
    # RUN mkdir /encrypted-output
    # WORKDIR /app
    # CMD python3 /%s --output /encrypted-output
    #     """ % code_file
    #     adf = open("docker-files/Dockerfile", "w")
    #     adf.write(dockerfile_algo_content)
    #     adf.close()
    dockerfile_algo_content = """
FROM algorithm-base:test
ADD image_files /
RUN mkdir /encrypted-output
WORKDIR /algo
CMD python3 /%s --output /encrypted-output
        """ % code_file
    adf = open("docker-files/Dockerfile", "w")
    adf.write(dockerfile_algo_content)
    adf.close()
    logger.debug(
        "\033[92mAn Algo Dockerfile 'Dockerfile' has been created at path : 'docker-files/Dockerfile'\033[0m")


def generate_code_entrypoint(confobj):
    code_file = confobj["dest_code_file"]
    nference_algorithm_file = """
import os
import sys
import argparse
import requests
import subprocess

print("A runner script for the developer's algorithm")
parser = argparse.ArgumentParser(description="Dev's algorithm Runner via subprocess")
parser.add_argument('--data-dir', action='store', dest='data_dir',
                    default='/algorithm-input', type=str, help='Data dir')
parser.add_argument('--mode', action='store', dest='mode',
                    default='train', type=str, help='Train or Test')
parser.add_argument('--output', action='store', dest='out_dir',
                    default='/algorithm-output', type=str, help='Output dir')
args = parser.parse_args(sys.argv[1:])
inputdir = args.data_dir
outputdir = args.out_dir
runout, runerr = subprocess.Popen(
    ["python3", "/%s", "--output", "/encrypted-output"]
    , stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
[print(r) for r in runout.decode("utf-8")]
""" % code_file
    ndf = open("app/nference_algorithm.py", "w")
    ndf.write(nference_algorithm_file)
    ndf.close()


def prepare_base_dockerfile(confobj):
    deps_path = confobj["dest_deps"]
    deps_file = confobj["dest_deps_file"].split("/")[-1]
    dockerfile_base_content = """
ARG algo_base
FROM ${algo_base}
ADD /%s/%s /%s
RUN /root/miniconda/bin/pip install --upgrade pip 
RUN /root/miniconda/bin/pip install --no-cache-dir -r /%s && rm /%s && find /usr/lib -name "*.pyc" -type f -delete

WORKDIR /

#ENTRYPOINT ["/bin/sh"]
""" % (deps_path, deps_file, deps_file, deps_file, deps_file)
    bdf = open("docker-files/Dockerfile.base", "w")
    bdf.write(dockerfile_base_content)
    bdf.close()
    logger.debug(
        "\033[92mA Base Dockerfile 'Dockerfile.base' has been created at path : 'docker-files/Dockerfile.base'\033[0m")


def submit_algo_image(tar_file, dockobj, is_authenticated, email, ep,
                      verbosity):  # TODO Needs to be run from the nference server
    logging.root.setLevel(verbosity)
    #  TODO remove it - the following is in case of DIRECT UPLOAD
    # tarout, tarerr = subprocess.Popen(["scli.sh", "sensec", "sctr", "import", "--imagetar", "/algo/%s" % tar_file,
    #                                    "-dreg", "nferalgos.azurecr.io", "-dcred", "%s:%s" % (
    #                                        sensoriant_docker_login_user,
    #                                        sensoriant_docker_login_passwd)
    #                                    ],
    #                                   stdout=subprocess.PIPE,
    #                                   stderr=subprocess.STDOUT
    #                                   ).communicate()
    # if tarout.decode("utf-8") != "":
    #     logger.debug("uploaded the docker image tar to the repository")
    # else:
    #     logger.debug("some problems uploading the tar onto the docker registry")
    datas = {
        'image_name': dockobj['image_name'],
        'image_repo': dockobj['image_repo'],
        # 'image_tag': "%s_%s" % (dockobj['image_tag'], ep),
        'image_tag': "%s" % (dockobj['image_tag']),
        'authenticated': is_authenticated,
        'email': email
    }
    files = [
        ('tar_file', (tar_file, open("%s/build/%s" % (os.getcwd(), tar_file), 'rb'), 'application/octet')),
        ('datas', ('datas', json.dumps(datas), 'application/json')),
    ]
    response = requests.post("%s/docker/tar-push" % docker_upload_url, files=files,
                             headers={'cookie': 'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1', }, timeout=600)
    if response.status_code == 200:
        # meas_file = "build/%s-%s_%s-enc-meas.txt" % (
        #     dockobj["image_name"],
        #     dockobj["image_tag"],
        #     ep
        # )
        meas_file = "build/%s-%s-enc-meas.txt" % (
            dockobj["image_name"],
            dockobj["image_tag"],
        )
        scli_digest = [line.strip().split("sha256:")[-1].strip() for line in open(meas_file, "r")][0]
        did = response.json()['id']
        """
        response = requests.post("%s/docker/img-upload/%s" % (docker_upload_url, did),
                                 json={'authenticated': is_authenticated, 'email': email})
        """
        response = requests.post("%s/docker/img-uploadv102/%s" % (docker_upload_url, did),
                                 json={
                                     'authenticated': is_authenticated, 'email': email,
                                     'scli_digest': scli_digest
                                 },
                                 headers={'cookie': 'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1', }
                                 )
        if response.status_code == 200:
            logger.debug("The encrypted .tar file of the image has been uploaded to docker registry")
        else:
            logger.error("Some problems persisting the .tar file to registry. Check response: `%s`" % (response.json()))
    else:
        logger.error("Some problems uploading the .tar file. Check response: `%s`" % (response.json()))
        sys.exit(1)
    return {
        "local_path_tar": tar_file,
        "image": dockobj["image_name"],
        # "tag": "%s_%s" % (dockobj["image_tag"], ep),
        "tag": "%s" % (dockobj["image_tag"]),
        "repo": dockobj["image_repo"],
        "docker-identifier": response.json()["docker-identifier"],
    }


def encrypt_dockerize_helper(apps_dir, deps_dir, lang, certificate, domain, dockobj,
                             is_authenticated, email, verbosity):
    logging.root.setLevel(verbosity)
    configparser = ConfigParser()
    configparser.read(".pbstate")
    confobj = dict(configparser["BUILD_ALGO"]) if configparser.has_section("BUILD_ALGO") else {}
    if bool(confobj):
        logger.debug("\033[91mRetrieving tar know-hows from section BUILD_ALGO as: \n%s\n\033[0m" % (confobj))
        tar_file = confobj['tar_file']
        # ep = tar_file.split("_")[-1].replace("-enc.tar", "")
        # submitout = submit_algo_image(tar_file, dockobj, is_authenticated, email, ep, verbosity)
        submitout = submit_algo_image(tar_file, dockobj, is_authenticated, email, "", verbosity)
        submitout['FSPF_TAG'] = confobj['fspf_tag']
        submitout['FSPF_KEY'] = confobj['fspf_key']
        submitout['SUCCESS'] = True
        submitout['mrenclave'] = confobj['mrenclave']
        submitout['DOMAIN'] = domain
        return submitout
    else:
        files = glob.glob('build/*')
        for f in files:
            os.remove(f)
        client = docker.from_env()
        image = "%s/%s/%s:%s" % (client_docker_registry, dockobj["image_repo"], dockobj["image_name"], dockobj["image_tag"])
        im = None
        try:
            im = client.images.get(image)
            client.images.remove(im.attrs['Id'], force=True)
        except Exception as e:
            logger.debug("\033[91mProblems deleting image with name : \033[94m%s\033[0m. \033[91mmsg : \033[94m%s\033[0m" % (image, str(e)))
        os.makedirs("image_files", exist_ok=True)  # TODO A big hack here.
        baseout, baseerr = subprocess.Popen(
            ["docker", "build", ".", "-t", "algorithm-base:test", "-f",
             "docker-files/Dockerfile.base", "--build-arg", "algo_base=%s" % (scli_ref_algo_image)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ).communicate()
        if baseout.decode("utf-8"):  # TODO Need to improve the error handling
            logger.debug("\033[92mThe base image `algorithm-base:test` has been built .. \033[0m")
            [logger.debug('\033[96m' + s + '\033[0m') for s in baseout.decode("utf-8").split("\n")]
        else:
            logger.error("\033[91msome problems building up the base image from docker-files/Dockerfile.base\033[0m")
            sys.exit(1)
        sconeout, sconeerr = subprocess.Popen(
            ["docker", "run", "-it", "--rm", "-e",
             "SCONE_MODE=sim",
             "-e", "SCONE_VERSION=1", "-v", "%s:/algorithm" % os.getcwd(),
             "algorithm-base:test", "sh", "-c",
             "cd /algorithm && rm -rf image_files && mkdir -p image_files/app && cd image_files && scone fspf create "
             "fspf.pb && scone fspf addr fspf.pb / --not-protected --kernel / && scone fspf addr fspf.pb /usr/lib/ "
             "--authenticated --kernel /usr/lib && scone fspf addf fspf.pb /usr/lib/ /usr/lib/ && scone fspf addr fspf.pb "
             "/app --encrypted --kernel /app && scone fspf addf fspf.pb /app /algorithm/app "
             "/algorithm/image_files/app && scone fspf addr fspf.pb /opt/scone/lib --authenticated --kernel "
             "/opt/scone/lib && scone fspf addf fspf.pb /opt/scone/lib /opt/scone/lib  && scone fspf encrypt fspf.pb > "
             "/algorithm/tag_key.txt"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
        if sconeout.decode("utf-8") != "":  # TODO This error handling needs to be improved
            logger.debug("\033[92mencrypt algorithm has run successfully\033[0m")
            [logger.debug('\033[96m' + s + '\033[0m') for s in sconeout.decode("utf-8").split("\n")]
            assert os.path.isdir("image_files") == True, "The Encryption Not Done correctly"
            assert os.path.isfile("tag_key.txt") == True, "The Encryption Not Done correctly"
        else:
            logger.error("\033[91msome problems in scone encrypting the algorithm : `algorithm-base:test`..\033[0m")
            sys.exit(1)
        fspf_tuple = [(str(line.strip().split("key:")[1]).strip(),
                       str(str(line.strip().split("key:")[0]).split("tag:")[1]).strip()) for line in
                      open("tag_key.txt", "r")]
        fspf_key = fspf_tuple[0][0]
        fspf_tag = fspf_tuple[0][1]
        ep = int(time.time())
        # prepare_dockercompose_yaml(fspf_key, fspf_tag, apps_dir, dockobj, ep)
        prepare_dockercompose_yaml(fspf_key, fspf_tag, apps_dir, dockobj, "")
        buildout, builderr = subprocess.Popen(["docker-compose", "build", "algorithm"], stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT).communicate()
        [logger.debug('\033[96m' + s + '\033[0m') for s in buildout.decode('utf-8').split("\n")]
        pushout, pusherr = subprocess.Popen(["docker-compose", "push", "algorithm"], stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT).communicate()
        mrout, mrerr = subprocess.Popen(["docker-compose", "run", "--no-deps", "-e", "SCONE_HASH=1", "algorithm"],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
        # mrenclave = mrout.decode('utf-8').split("[1B")[-1].strip()
        mrenclave = "c009917b3ff6709e673d85c3fa19f878d8cbdbdb029cfd26f5577e197e87fa45"
        [logger.debug('\033[96m' + s + '\033[0m') for s in pushout.decode('utf-8').split("\n")]
        if buildout and pushout:  # TODO Need better error handling here
            logger.debug("\033[92mThen `algorithm` image could successfully be built ..\033[0m")
        else:
            logger.error("Some problems with building and pushing locally, the docker image for the algorithm")
            sys.exit(1)
        os.remove("tag_key.txt")
        shutil.rmtree("image_files")
        os.environ["SCLI_ALGO_DIR"] = os.getcwd()
        # TODO correct the domain , print and check
        esigout, esigerr = subprocess.Popen(
            ["scli.sh", "sensec", "esig", "-sreg", client_docker_registry, "-dom",
             domain, "-skey", "/algo/%s" % certificate, "--outdir", "/algo/build/", "--reftar",
             "%s/%s" % ("/algo/", "REF_ALGO_BASE.tar"), "--outtar",  # SCLI_REF_ALGO_TAR=$SCLI_ALGO_DIR/ref.tar
             # "%s/%s/%s:%s_%s" % (
             #    client_docker_registry, dockobj["image_repo"], dockobj["image_name"], dockobj["image_tag"], ep
             "%s/%s/%s:%s" % (
                 client_docker_registry, dockobj["image_repo"], dockobj["image_name"], dockobj["image_tag"]
             )], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ).communicate()
        [logger.debug('\033[96m' + s + '\033[0m') for s in esigout.decode("utf-8").split("\n")]
        if esigout.decode('utf-8') != "":
            logger.debug("\033[92mThe algorithm image has been signed and encrypted, as command : `%s`\033[0m" % (
                ' '.join(
                    ["scli.sh", "sensec", "esig", "-sreg", client_docker_registry,
                     "-dom", domain, "-skey", "/algo/%s" % certificate, "--outdir", "%s" % os.getcwd(),
                     # "--outtar", "%s/%s/%s:%s_%s" % (
                     #    client_docker_registry, dockobj["image_repo"], dockobj["image_name"], dockobj["image_tag"], ep
                     # )
                     "--outtar", "%s/%s/%s:%s" % (
                         client_docker_registry, dockobj["image_repo"], dockobj["image_name"], dockobj["image_tag"]
                     )
                     ]
                )
            ))
        else:
            logger.error("Some problems with encrypting and signing the algorithm image with command : `%s`.." % (
                ["scli.sh", "sensec", "esig", "-sreg", client_docker_registry,
                 "-dom", domain, "-skey", "/algo/%s" % certificate, "--outdir", "%s" % os.getcwd(),
                 # "--outtar", "%s/%s/%s:%s_%s" % (
                 #    client_docker_registry, dockobj["image_repo"], dockobj["image_name"], dockobj["image_tag"], ep
                 # )
                 "--outtar", "%s/%s/%s:%s" % (
                     client_docker_registry, dockobj["image_repo"], dockobj["image_name"], dockobj["image_tag"]
                 )
                 ]
            ))
            sys.exit(1)
        tar_file = [str(f) for f in os.listdir("%s/build/" % os.getcwd()) if str(f).endswith('enc.tar')][
            0]  # TODO Get this properly please
        config_object = ConfigParser()
        config_object["BUILD_ALGO"] = {
            "fspf_tag": fspf_tag, "fspf_key": fspf_key, "tar_file": tar_file, "mrenclave": mrenclave
        }
        with open('.pbstate', 'a') as conf:
            config_object.write(conf)
        # submitout = submit_algo_image(tar_file, dockobj, is_authenticated, email, ep, verbosity)
        submitout = submit_algo_image(tar_file, dockobj, is_authenticated, email, "", verbosity)
        submitout['FSPF_TAG'] = fspf_tag
        submitout['FSPF_KEY'] = fspf_key
        submitout['SUCCESS'] = True
        submitout['mrenclave'] = mrenclave
        submitout['DOMAIN'] = domain
        return submitout


def encrypt_dockerize_persist(algoobj, verbosity):
    logging.root.setLevel(verbosity)
    public_key = parse_var(algoobj["sdbx_pubkey"]) if parseable_expr(algoobj["sdbx_pubkey"]) else algoobj["sdbx_pubkey"]
    cert_path = parse_var(algoobj["cert_path"]) if parseable_expr(algoobj["cert_path"]) else algoobj[
        "cert_path"]
    certificate = parse_var(algoobj["certificate"]) if parseable_expr(algoobj["certificate"]) else algoobj[
        "certificate"]
    ca_cert_path = parse_var(algoobj["ca_cert_path"]) if parseable_expr(algoobj["ca_cert_path"]) else algoobj[
        "ca_cert_path"]
    ca_certificate = parse_var(algoobj["ca_certificate"]) if parseable_expr(algoobj["ca_certificate"]) else algoobj[
        "ca_certificate"]
    domain = parse_var(algoobj["domain"]) if parseable_expr(algoobj["domain"]) else algoobj[
        "domain"]
    certificate = "%s/%s" % (cert_path, certificate)
    ca_certificate = "%s/%s" % (ca_cert_path, ca_certificate)
    access_key = get_credentials('ACCESS_KEY')
    secret_key = get_credentials('SECRET_KEY')
    authobj = authenticate({
        "access_key": access_key,
        "secret_key": secret_key
    })
    dockobj = {
        "image_name": parse_var(algoobj["docker"]["image_name"]) if parseable_expr(algoobj["docker"]["image_name"]) else
        algoobj["docker"]["image_name"],
        "image_tag": parse_var(algoobj["docker"]["image_tag"]) if parseable_expr(algoobj["docker"]["image_tag"]) else
        algoobj["docker"]["image_tag"],
        "image_repo": parse_var(algoobj["docker"]["image_repo"]) if parseable_expr(algoobj["docker"]["image_repo"]) else
        algoobj["docker"]["image_repo"]
    }
    if authobj["message"] == 'Authenticated':
        dockout = encrypt_dockerize_helper(
            parse_var(algoobj["app_dir"]) if parseable_expr(algoobj["app_dir"]) else algoobj["app_dir"],
            parse_var(algoobj["deps_dir"]) if parseable_expr(algoobj["deps_dir"]) else algoobj["deps_dir"],
            parse_var(algoobj["lang"]) if parseable_expr(algoobj["lang"]) else algoobj["lang"],
            certificate,
            domain,
            dockobj,
            True if authobj["message"] == "Authenticated" else False,
            authobj['email'],
            verbosity
        )
        if dockout["SUCCESS"]:
            logger.debug(
                "\033[92mthe dockerfile could be created, as .tar of encrypted algo image, inside `pwd`\033[0m")
        else:
            logger.debug("\033[91mthe command `sens-cli %s %s %s %s failed to trigger..\033[0m" % (
                algoobj["apps_dir"], algoobj["deps_dir"], algoobj["key_algo"], algoobj["lang"]))
    else:
        logger.error("\033[91mThe User is not authenticated! Ideally, exitting this from dockerization\033[0m")
        sys.exit(1)
    return dockout

