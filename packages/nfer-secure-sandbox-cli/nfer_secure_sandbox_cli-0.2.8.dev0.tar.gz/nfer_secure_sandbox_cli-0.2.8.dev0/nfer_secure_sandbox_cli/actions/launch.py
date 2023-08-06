import time
import webbrowser
import socket, errno
import subprocess
import getpass
import os
import sys
import time
from datetime import datetime, timedelta
from utils.sensoriant.configuration.conf import *
import platform
import nfer_secure_sandbox_cli


def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))


major = sys.version_info.major
minor = sys.version_info.minor

if platform.system() == "Linux":
    command = "netstat -tulpn | grep %d" % setup_server_port
    if is_venv():
        os.environ["NFER_PATH"] = "/".join(nfer_secure_sandbox_cli.__file__.split("/")[:-1])
    else:
        os.environ["NFER_PATH"] = "/".join(nfer_secure_sandbox_cli.__file__.split("/")[:-1])
elif platform.system() == 'Darwin':
    command = "lsof -i tcp:%d"%setup_server_port
    if is_venv():
        os.environ["NFER_PATH"] = "/".join(nfer_secure_sandbox_cli.__file__.split("/")[:-1])
    else:
        os.environ["NFER_PATH"] = "/usr/local/lib/python%s.%s/site-packages/nfer_secure_sandbox_cli"%(major, minor)


def print_msg():
    print(os.getcwd())
    print("""
[I %s Nfer-Sandbox-CLI] \033[93mNfer-Sandbox-CLI Launcher is running at:\033[0m
[I %s Nfer-Sandbox-CLI] \033[96mhttp://localhost:3000/\033[0m
[I %s Nfer-Sandbox-CLI]  or \033[96mhttp://127.0.0.1:3000/\033[0m
[I %s Nfer-Sandbox-CLI] There is also a server spun up along at \033[94mhttp://127.0.0.1:5112 \033[0m. Kill it explicitly.
[I %s Nfer-Sandbox-CLI] \033[93mUse Control-C to stop this server and shut down all kernels (twice to skip confirmation).\033[0m
[C %s Nfer-Sandbox-CLI] 

    \033[92mTo access the notebook, copy and paste one of these URLs:\033[0m
        \033[94mhttp://localhost:3000/\033[0m
     or \033[94mhttp://127.0.0.1:3000/\033[0m
    """ % (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S.%s"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S.%s"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S.%s"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S.%s"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S.%s"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S.%s")
    ))


def launch():
    nfer_cli_home = NFER_CLI_HOME % getpass.getuser() # NFER_CLI_HOME % os.environ["USER"]
    cwd = os.getcwd()
    fout = open("%s/%s" % (setup_conf_path % (getpass.getuser()), setup_conf_file), "a")
    fout.write("%s | %s\n" % (int(time.time()), cwd))
    fout.close()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((setup_server_addr, setup_server_port))
        s.close()
        serp = subprocess.Popen(["python3", "%s/webapp/server/server.py" % os.environ["NFER_PATH"]], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        time.sleep(10)
        global command
        c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = c.communicate()
        if platform.system() == "Linux":
            pid = stdout.decode().strip().split(' ')[-1]
        elif platform.system() == 'Darwin':
            pid = stdout.decode().split("\n")[-2].strip().split(' ')[2]
        print(
            "[I %s Nfer-Sandbox-CLI] \033[94mThe setup flask server now running at \033[4mport : %d by the process : %s\033[0m" % (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%s"), setup_server_port, pid))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
            stdout, stderr = c.communicate()
            stdout.decode('utf-8')
            pid = stdout.decode().strip().split(' ')[-1] # stdout.decode().split("\n")[-2].strip().split(' ')[2]
            print("[I %s Nfer-Sandbox-CLI] \033[94mThe setup flask server seems already to be running at \033[4mport : %d by the process : %s\033[0m"%(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%s"),setup_server_port,pid))
        else:
            print(
                "[I %s Nfer-Sandbox-CLI] \033[91mFATAL! Could not start setup server at %s:%s... \033[1mExitting\033[0m\n" % (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S.%s"), setup_server_addr, setup_server_port
                ))
            sys.exit(1)
    os.chdir("%s/webapp" % os.environ["NFER_PATH"])
    iout, ierr = subprocess.Popen(["npm", "install"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()
    print_msg()
    cliout, clerr = subprocess.Popen(["npm", "start","HOST=0.0.0.0"], stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT).communicate()
    [print(s) for s in cliout.decode("utf-8").split("\n")]
    os.chdir(cwd)
    # webbrowser.open('localhost:3000', new=2)
