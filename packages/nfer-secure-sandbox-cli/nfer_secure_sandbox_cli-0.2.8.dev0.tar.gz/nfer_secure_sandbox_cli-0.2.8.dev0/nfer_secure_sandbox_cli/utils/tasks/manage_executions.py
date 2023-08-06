from utils.display.artefacts_utils import publish
from utils.state.manage_state import read_state, register
from utils.state.manage_state import persist_state
from utils.sensoriant.execution.exec_utils import exec_and_manage
from utils.sensoriant.configuration.conf import *
import requests
import sys
import json
import time
import logging
logging.basicConfig(format='[%(asctime)s : %(levelname)s Line No. : %(lineno)d %(funcName)5s() %(filename)5s] - %('
                           'message)s')
logger = logging.getLogger(__name__)


def get_exec_status(pipeline_id):
    """

    :param pipeline_id: # TODO bring in the concept of Authentication here too!
    :return:
    """
    response = requests.get('%s/pipelines/by_id/%s' % (nfer_sdbx_url, pipeline_id),headers={'cookie':'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1',})
    return json.loads(response.content)["response"]['status']


def persist_logs_batch(pipeline_id, start_ts, end_ts):
    """

    :param pipeline_id:
    :param start_ts:
    :param end_ts:
    :return:
    """
    params = (
        ('limit', '10'),
        ('skip', '0'),
    )
    response = requests.get('%s/logs/start_timestamp/%s/end_timestamp_ms/%s' % (
        nfer_sdbx_url,
        start_ts,
        end_ts
    ), params=params, headers={'cookie':'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1',})
    f = open("logs/execution-%s.log" % pipeline_id, 'a')
    f.write(str(json.loads(response.content)))
    f.close()
    return {
        "ts": int(time.time()),
        "SUCCESS": True
    }


def persist_logs(pipeline_id, ts):
    """

    :param pipeline_id:
    :param ts:
    :return:
    """
    params = (
        ('limit', '10'),
        ('skip', '0'),
    )
    response = requests.get('%s/logs/end_timestamp_ms/%s' % (nfer_sdbx_url, ts), params=params, headers={'cookie':'sessionid=15oywchr2xnad1v17isrt0vo5gsx1yy1',})
    f = open("logs/execution-%s.log" % pipeline_id, 'a')
    f.write(str(json.loads(response.content)))
    f.close()
    return {
        "ts": int(time.time()),
        "SUCCESS": True
    }


def execute_policy(task, verbosity):
    logging.root.setLevel(verbosity)
    if read_state(task, verbosity, 'execute-policy'):
        exec_specs = exec_and_manage(task["execute-policy"], verbosity)
        if exec_specs["SUCCESS"]:
            confobj = {
                "name": exec_specs["response"]["name"],
                "id": exec_specs["response"]["id"],
                "template_name": exec_specs["response"]["template"]["name"],
                "template_id": exec_specs["response"]["template"]["id"],
                "execution_started_at": exec_specs["response"]["creationDate"],
                "logfile": "logs/%s" % exec_specs["response"]["id"],
                "status": exec_specs["response"]["status"]
            }
            status = get_exec_status(confobj["id"])
            first = False
            while status not in ["READY", "FAILED"]:
                status = get_exec_status(confobj["id"])
                if first:
                    ts = persist_logs(confobj["id"], int(time.time()))
                else:
                    ts = persist_logs_batch(confobj['id'], ts, int(time.time()))
            register(confobj, task)
            persist_state(task, verbosity, "execute-policy", confobj)
            publish("execute-policy", task, confobj)
        else:
            logger.error("The Creation of Pipeline was unsuccessful with message `%s`" % (
                exec_specs["response"]["message"]
            ))
            logger.error("Exitting ...")
            sys.exit(1)
