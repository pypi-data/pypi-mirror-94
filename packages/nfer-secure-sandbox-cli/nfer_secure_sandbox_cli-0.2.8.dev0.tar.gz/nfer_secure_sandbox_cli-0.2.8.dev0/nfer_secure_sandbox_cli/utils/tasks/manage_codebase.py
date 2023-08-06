import os
import sys
import grp
import shutil
import random
import getpass

from utils.display.artefacts_utils import publish
from utils.state.manage_state import read_state, persist_state
from utils.logging.logger import log
from utils.state.manage_state import register
from utils.sensoriant.configuration.conf import *
from utils.sensoriant.algo.algo_utils import prepare_base_dockerfile, prepare_algo_dockerfile, generate_code_entrypoint
import git
import traceback
import subprocess
import logging

logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def populate_codebase(task, verbosity):
    logging.root.setLevel(verbosity)
    if read_state(task, verbosity, 'codebase'):
        if task["populate-codebase"]["mode"] == "git":
            os.makedirs(clone_temp_dir, exist_ok=True)
            repo = str(task["populate-codebase"]["url"]).split("/")[-1] if "tree" not in str(
                task["populate-codebase"]["url"]) else str(task["populate-codebase"]["url"]).split("/")[-3]
            git_url = str(task["populate-codebase"]["url"]).replace(git_replace_from, git_replace_to % (
                task["populate-codebase"]["credentials"]["username"],
                task["populate-codebase"]["credentials"]["password"]
            ))
            try:
                git.Git("%s/" % clone_temp_dir).clone("%s.git" % git_url)
            except Exception as e:
                logger.error(
                    "\033[91msome exception encountered while cloning/pulling repo `%s` to `temp`\033[0m" % git_url)
                traceback.print_exc()
                sys.exit(1)
            shutil.chown("app", user=getpass.getuser(), group=grp.getgrgid(os.getegid()).gr_name)
            shutil.chown(clone_temp_dir, user=getpass.getuser(), group=grp.getgrgid(os.getegid()).gr_name)
            appout, apperr = subprocess.Popen(
                ["cp", "-r", "%s/%s/%s" % (clone_temp_dir, repo, task["populate-codebase"]["code_path"]),
                 "%s/%s" % (algo_app_dir, task["populate-codebase"]["code_path"])],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
            shutil.chown("app", user=getpass.getuser(), group=grp.getgrgid(os.getegid()).gr_name)
            shutil.chown(clone_temp_dir, user=getpass.getuser(), group=grp.getgrgid(os.getegid()).gr_name)
            shutil.rmtree("%s/%s/.git"%(clone_temp_dir,repo))
            depout, deperr = subprocess.Popen(
                ["cp", "-r", "%s/%s/%s" % (clone_temp_dir, repo, task["populate-codebase"]["deps_path"]),
                 "%s/%s" % (algo_deps_dir, task["populate-codebase"]["deps_path"])],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
            reqout, reqerr = subprocess.Popen(
                ["cp", "%s/%s/%s" % (
                    algo_deps_dir,
                    task["populate-codebase"]["deps_path"],
                    task["populate-codebase"]["deps_file"]
                ), "app/requirements.txt"]
                ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
            [logger.debug(s) for s in reqout.decode('utf-8').split("\n")]
            if appout.decode("utf-8") != '' or depout.decode("utf-8") != '':
                logger.error(
                    "\033[91mSome problems copying code+dep files into `app` folder. Debug Messages : `%s` for algo and `%s` for deps\033[0m" % (
                        appout.decode("utf-8"),
                        depout.decode("utf-8")
                    ))
                #sys.exit(1)
            else:
                logger.debug(
                    "\033[92mSuccessfully copied Code and Dependencies from git repo `\033[4m%s\033[0m\033[92m` inside `\033[4mapp\033[0m\033[92m` and `\033[4mdeps\033[0m\033[92m` dirs under '\033[1malgo/\033[0m\033[92m' folder\033[0m" % (
                        git_url
                    ))
            shutil.rmtree("temp")
        elif task["populate-codebase"]["mode"] == "scp":
            pass
            # TODO
        else:
            logger.error(
                "\033[91mThis mode of code pull `%s` not supported. Choose amongst [`git`, `scp`]" %
                task["populate-codebase"][
                    "mode"])
            sys.exit(1)
        confobj = {
            "src_code": "%s/%s" % (task["populate-codebase"]["url"], task["populate-codebase"]["code_path"]),
            "file_code": "%s" % (task["populate-codebase"]["main_file"]),
            "src_deps": "%s/%s" % (task["populate-codebase"]["url"], task["populate-codebase"]["deps_path"]),
            "file_deps": "%s" % (task["populate-codebase"]["deps_file"]),
            "dest_code": "%s/%s" % (algo_app_dir, task["populate-codebase"]["code_path"]),
            "dest_deps": "%s/%s" % (algo_deps_dir, task["populate-codebase"]["deps_path"]),
            "dest_code_file": "%s/%s/%s" % (
                algo_app_dir, task["populate-codebase"]["code_path"], task["populate-codebase"]["main_file"]),
            "dest_deps_file": "%s/%s/%s" % (
                algo_deps_dir, task["populate-codebase"]["deps_path"], task["populate-codebase"]["deps_file"]),
            "stack": task["populate-codebase"]["stack"],
            "mode": task["populate-codebase"]["mode"],
            "repo": repo
        }
        #generate_code_entrypoint(confobj)
        prepare_base_dockerfile(confobj)
        prepare_algo_dockerfile(confobj)
        register(confobj, task)
        persist_state(task, verbosity, "codebase", confobj)
        publish("codebase",task,confobj)
