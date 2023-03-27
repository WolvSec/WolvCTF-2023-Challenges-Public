
import flask
from pathlib import Path
import subprocess
import tempfile

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return flask.send_file('index.html')

import re

@app.route('/compile', methods=['POST'])
def flag():
  code = flask.request.form.get('code')
  print(code)
  print(code.encode().hex())

  with tempfile.TemporaryDirectory() as d:
    with open(d + "/flag", 'w') as f:
      with open('flag') as flag:
        f.write(flag.read())
    with open(d + "/code.c", 'wb') as f:
      f.write(code.encode())
    output = subprocess.run(['gcc', '-fpreprocessed', d + "/code.c", '-o', d + "/code"], capture_output=True)
    if not (Path(d) / 'code').exists():
      return "Compilation failed: " + output.stderr.decode('utf-8')
    output = subprocess.run(['xxd', d + "/code"], capture_output=True).stdout.decode('utf-8')
    output = re.sub(r'\n', '<br/>', output)
    return output
