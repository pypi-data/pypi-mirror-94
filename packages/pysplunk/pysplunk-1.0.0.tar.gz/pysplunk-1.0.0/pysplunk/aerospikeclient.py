import asyncio
import hashlib
import json
import traceback
from urllib.parse import urlencode

import aiohttp

from .settings import *


def gethash(evidence):
    try:
        byts = evidence.encode()
        md5bytes = hashlib.md5()
        md5bytes.update(byts)
        return md5bytes.hexdigest()
    except Exception as e:
        return "error-hash:{}".format(e)


async def saveAsync(index, account, evidence):
    try:
        params = {
            'application': index,
            'expirationInSeconds': AEROSPIKE_EVIDENCE_TTL
        }
        url = "{}?{}".format(AEROSPIKE_EVIDENCE_URL, urlencode(params))
        data = json.dumps(evidence)
        headers = {"Content-Type": "text/plain"}
        timeout = aiohttp.ClientTimeout(AEROSPIKE_EVIDENCE_TIMEOUT)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.put(url, data=data, headers=headers) as r:
                return await r.text()
    except asyncio.TimeoutError as t:
        print('timeout: {}'.format(t))
    except Exception:
        msg = "Error in save to aerospike: {}".format(traceback.print_exc())
        print(msg)

    return ''
