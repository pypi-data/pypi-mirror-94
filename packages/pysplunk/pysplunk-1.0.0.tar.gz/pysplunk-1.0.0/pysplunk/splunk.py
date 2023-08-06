import logging
import os
import sys
import traceback
from datetime import datetime
from urllib.parse import urlencode
from uuid import uuid4

import requests

from . import aerospikeclient
from .settings import *


SPLUNK_CHANNEL = str(uuid4())
if not SPLUNK_LOG_FORMAT:
    SPLUNK_LOG_FORMAT = '%(customasctime)s ' + SPLUNK_LOG_HANDLER_NAME + \
        ',%(logindex)s,%(instance)s,%(logtype)s,%(logtype)s,'\
        '"%(workflow_type)s","%(workflow_instance)s",%(account)s,'\
        '%(version)s message="%(message)s" %(custom_fields)s'


class Level(object):
    debug = ["DEBUG"]
    info = ["DEBUG", "INFO"]
    warn = ["DEBUG", "INFO", "WARN"]
    error = ["DEBUG", "INFO", "WARN", "ERROR"]


class Settings(object):
    LOG_NAME = 'splunk'
    LOG_LEVEL = logging.DEBUG
    INDEX = os.getenv('SPLUNK_INDEX')
    VERSION = '0.0.1'
    INSTANCE = 'local'
    ENV = 'beta'
    TOKEN = os.getenv('SPLUNK_TOKEN')


class SplunkLogHandler(logging.Handler):
    def emit(self, record):
        if not Settings.INDEX or not Settings.TOKEN:
            return

        params = {'channel': SPLUNK_CHANNEL}
        splunk_url = '{}?{}'.format(SPLUNK_URL, urlencode(params))

        log_entry = self.format(record)

        headers = {
            'Content-Type': 'text/plain',
            'Authorization': 'Splunk ' + Settings.TOKEN
        }

        return requests.post(
            splunk_url,
            data=log_entry,
            verify=False,
            headers=headers)


# Make a global logging object.
log = logging.getLogger(Settings.LOG_NAME)

# Max 50mb
splunk_handler = SplunkLogHandler()
splunk_handler.setFormatter(logging.Formatter(SPLUNK_LOG_FORMAT))
log.addHandler(splunk_handler)


def datetimeparsed():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + 'Z'


def format_custom_fields(custom_fields):
    fields = ['{}="{}"'.format(k, str(v).replace('"', r'\"'))
              for k, v in custom_fields.items()]
    return ' '.join(fields)


async def pack_exception(e, account):
    stack_trace = None
    exc_type, exc_value, trace_back = sys.exc_info()
    try:
        if exc_type:
            stack_trace_list = traceback.format_exception(
                exc_type, exc_value, trace_back)
            stack_trace = "".join(stack_trace_list)
    except Exception as ex:
        stack_trace = "Error packaging exception: {}".format(ex)

    if not stack_trace:
        return ""

    # Send to aerospike.
    return await aerospikeclient.saveAsync(
        str(Settings.INDEX), str(account), str(stack_trace))


def configure_logger(index, token, version, env, level=logging.DEBUG):
    if level:
        Settings.LOG_LEVEL = level
    log.setLevel(Settings.LOG_LEVEL)

    if index:
        Settings.INDEX = index.lower().strip()

    if token:
        Settings.TOKEN = token.strip()

    if version:
        Settings.VERSION = version.lower().strip()

    if env:
        Settings.ENV = env.lower().strip()

    get_instance()


def get_instance():
    try:
        url = 'http://169.254.169.254/latest/meta-data/instance-id'
        r = requests.get(url, timeout=0.8)
        instance = r.text
    except Exception:
        instance = 'local'

    Settings.INSTANCE = instance


async def _log(level, account, workflow_type, workflow_instance, msg,
               custom_fields=None, evidence=None):
    if custom_fields is None:
        custom_fields = {}

    custom_fields["env"] = Settings.ENV

    evidence_hash = None
    if evidence is not None and Settings.LOG_LEVEL in Level.warn:
        evidence_hash = await aerospikeclient.saveAsync(
            Settings.INDEX, account, evidence)
    elif evidence is not None and Settings.LOG_LEVEL in Level.error:
        evidence_hash = await pack_exception(evidence, account)

    if evidence_hash:
        custom_fields["evidence"] = evidence_hash

    custom = format_custom_fields(custom_fields)

    _log_function = getattr(log, level)
    _log_function(msg.replace('"', r'\"'), extra={
        'customasctime': datetimeparsed(),
        'logindex': Settings.INDEX,
        'logtype': level,
        'instance': Settings.INSTANCE,
        'version': Settings.VERSION,
        'workflow_type': str(workflow_type).strip(),
        'workflow_instance': str(workflow_instance).strip(),
        'account': str(account).lower().strip(),
        'custom_fields': custom,
    })


async def logdebug(account, workflow_type, workflow_instance, msg,
                   custom_fields=None, evidence=None):
    await _log(
        'debug', account, workflow_type, workflow_instance, msg,
        custom_fields, evidence)


async def loginfo(account, workflow_type, workflow_instance, msg,
                  custom_fields=None, evidence=None):
    await _log(
        'info', account, workflow_type, workflow_instance, msg,
        custom_fields, evidence)


async def logwarn(account, workflow_type, workflow_instance, msg,
                  custom_fields=None, evidence=None):
    await _log(
        'warn', account, workflow_type, workflow_instance, msg,
        custom_fields, evidence)


async def logerror(account, workflow_type, workflow_instance, msg,
                   custom_fields=None, evidence=None):
    await _log(
        'error', account, workflow_type, workflow_instance, msg,
        custom_fields, evidence)
