from utils.logging.logger import log
from utils.sensoriant.configuration.conf import *
from shutil import copyfile
import subprocess
import sys
import os
import logging


def init(lvl):
    os.makedirs(ref_algo_dir, exist_ok=True)
    f_dcmp = open("docker-compose.yml", "w")
    f_dcmp.write("""
version: '3.2'
services:
    SensCli:
        image: sensoriant.azurecr.io/nference/scli:%s
        network_mode: "host"
        command: bash -c "./start.sh"
        volumes:
            - %s:/algo"""%(version, os.getcwd()))
    f_dcmp.close()
    logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                               'message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(lvl)
    logger.debug(
        "\033[96mInitializing The 'Client System' with a local Docker Registry a.k.a '\033[4mClient Registry\033[0m', \033[96mand pushing few helper images like `\033[4msenscli\033[0m` \033[96metc.\033[0m")  # TODO maybe remove this
    checkout, checkerr = subprocess.Popen(["docker", "ps", "-aq", "-f", "status=running", "-f", "name=clientregistry"],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT).communicate()  # TODO maybe remove this
    if checkout.decode('utf-8') == "":
        logger.debug("\033[96mLocal registry is \033[4mnot running\033[0m; \033[96mStarting now ...\033[0m")
        regout, regerr = subprocess.Popen(["docker", "pull", "registry:latest"], stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT).communicate()
        if regout.decode('utf-8') != '':
            [logger.debug('\033[94m' + s + '\033[0m') for s in regout.decode("utf-8").split("\n")]
            logger.debug("\033[96mPulled the Docker Registry `latest` version onto Local System ...\033[0m")
        else:
            logger.error(
                "\033[91mSome problems in pulling up docker registry : issues with command - '\033[4m%s\033[0m'\033[0m" % (
                    ' '.join(["docker", "pull", "registry:latest"]),
                ))
            logger.error("\033[91m\033[1mExitting!\033[0m")
            sys.exit()
        logger.debug("\n\n\033[96mStarting the Local Docker Registry on port : 5000 ...\033[0m\n\n")
        startout, starterr = subprocess.Popen(
            ["docker", "run", "-d", "-p", "5000:5000", "--restart=always", "--name", "clientregistry", "registry"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
        [logger.debug(s) for s in startout.decode("utf-8").split("\n")]
        if startout.decode('utf-8') == "":
            logger.debug(
                "\033[91mProblems starting the docker registry. Error executing command : '\033[4m%s\033[0m'\033[0m" % ' '.join(
                    ["docker", "run", "-d", "-p", "5000:5000", "--restart=always", "--name", "clientregistry",
                     "registry"]))
        else:
            logger.debug(
                "\033[92mA Local Docker Registry container has been started at port - 5000 : container id - `\033[4m%s\033[0m` ...\033[0m" % startout.decode(
                    'utf-8').strip())
    else:
        logger.debug("\033[92mLocal docker registry is \033[1mup and running\033[0m\033[0m")
        scliout, sclierr = subprocess.Popen(["docker", "images", "-q", "scli:latest"], stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT).communicate()
        if scliout.decode('utf-8') != "":
            logger.debug(
                "\033[92mThe Image \033[4mscli:latest\033[0m \033[92mimage is already pulled. Image ID : '\033[4m%s\033[0m'. \033[0m" % scliout.decode(
                    'utf-8').strip())
        else:
            logger.debug("\033[96mLogging into our registry, to pull the '\033[4mscli\033[0m' \033[96mimage ...\033[0m")
            logout, logerr = subprocess.Popen(
                ["docker", "login", "-u", sensoriant_docker_login_user, "-p", sensoriant_docker_login_passwd,
                 sensoriant_docker_registry],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
            if logout.decode('utf-8').split('\n')[-2] == "Login Succeeded":
                [logger.debug('\033[96m' + s + '\033[0m') for s in logout.decode("utf-8").split("\n")]
            else:
                logger.error(
                    "\033[91mSome problems logging into the `\033[4m%s\033[0m\033[91m`. Message: `\033[91m%s\033[0m`\033[0m" % (
                        sensoriant_docker_registry,
                        logout.decode('utf-8')
                    ))
                pullout, pullerr = subprocess.Popen(
                    ["docker", "pull", "sensoriant.azurecr.io/nference/scli:VERSION_1_1_0"], stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT).communicate()
                if not pullout.decode("utf-8").startswith('Error'):
                    [logger.debug('\033[96m' + s + '\033[0m') for s in pullout.decode("utf-8").split("\n")]
                else:
                    logger.error(
                        "\033[91mSome errors pulling the `\033[4mscli:latest\033[0m` \033[91mImage. The command run was : '\033[4m%s\033[0m'" % (
                            ' '.join(["docker", "pull", "sensoriant.azurecr.io/scli:latest"])))
                    sys.exit(1)
                tagout, tagerr = subprocess.Popen(["docker", "tag", "sensoriant.azurecr.io/scli:latest", "scli:latest"],
                                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
                if not tagout.decode('utf-8').startswith('Error'):
                    logger.debug("\033[92mThe image `\033[4mscli:latest\033[0m` \033[92mhas been tagged.\033[0m")
                else:
                    logger.error(
                        "\033[91mSome problems tagging the image `\033[4msensoriant.azurecr.io\033[0m` \033[91mwith tag `\033[4mscli:latest\033[0m`\033[0m")
                    sys.exit(1)
                logger.debug(
                    "\033[92m\033[1mThe Initialization\033[0m \033[92mwith Docker Registry, scli Image has been completed.\033[0m")
        #     idg = subprocess.Popen(["id", "-g"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').split("\n")[0]
        #     idu = subprocess.Popen(["id", "-u"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').split("\n")[0]
        #     cpout, cperr = subprocess.Popen(
        #         ["docker", "run", "--rm", "-e", "HUSER=%s" % idu, "-e", "HGRP=%s" % idg, "-it", "-v",
        #          "%s:/scripts" % (os.getcwd()), "scli:latest", "bash", "-c", "'/scripts/cpscli.sh'"],
        #         stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
        #     [logger.debug('\033[94m'+s+'\033[0m') for s in cpout.decode('utf-8').split("\n")]
    os.environ['SCLI_ALGO_DIR'] = ref_algo_dir
    os.makedirs(os.environ['SCLI_ALGO_DIR'], exist_ok=True)
    pullout, pullerr = subprocess.Popen(["docker", "pull", "sensoriant.azurecr.io/nference/scli:%s" % version],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    [logger.debug(s) for s in pullout.decode('utf-8').split("\n")]
    if not os.path.exists("%s/%s" % (ref_algo_dir, ref_algo_tar)):
        tarout, tarerr = subprocess.Popen(["scli.sh", "sensec", "mktar", "-scred",
                                           "%s:%s" % (sensoriant_docker_login_user, sensoriant_docker_login_passwd),
                                           "-tf", "%s/%s" % (ref_algo_dir, ref_algo_tar),
                                           scli_ref_algo_image], stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT).communicate()
        [logger.debug(s) for s in tarout.decode('utf-8').split("\n")]
        copyfile(ref_algo_tar, "%s/%s" % (ref_algo_dir, ref_algo_tar))
    else:
        if not os.path.exists(ref_algo_tar):
            logger.debug("\033[92mThe ref tar already exists at path : %s/%s ..."%("%s/%s" % (ref_algo_dir, ref_algo_tar)))
            copyfile("%s/%s" % (ref_algo_dir, ref_algo_tar), ref_algo_tar)
        else:
            logger.debug("\033[92mThe ref image is available at path(s) : `%s` and `%s`\033[0m" % (
                "%s/%s" % (ref_algo_dir, ref_algo_tar),
                ref_algo_tar
            ))
