from datetime import datetime
from flask import Flask, request, send_file, abort
from flask_httpauth import HTTPBasicAuth
from os import listdir
from os.path import exists, isfile, join
import json

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if password == config['read_secret']:
        return "valid_user"

@app.route("/report", methods=["POST"])
def report():
    report = request.get_json()
    if 'secret' not in report or report['secret'] != config['write_secret']:
        abort(403)
        return
    del report['secret']
    id = 0
    idstr = None
    now = datetime.now()
    report["report-time"] = now.isoformat()
    date = now.strftime('%Y-%m-%d')
    while True:
      idstr = str(id).zfill(4)
      filename = 'crash-' + date + "-" +  idstr + '.json'
      crashfile = join(config['crash_dir'], filename)
      try:
          fd = open(crashfile, 'x')
          json.dump(report, fd, indent=2)
          break
      except FileExistsError:
          id += 1
          continue
    return (date + "-" + idstr, 200)

@app.route("/list", methods=["GET"])
def list():
    crash_dir = config['crash_dir']
    crash_files = [f for f in listdir(crash_dir) if isfile(join(crash_dir, f)) and f.startswith("crash-")]
    crash_ids = map(lambda f: f.replace("crash-","").replace(".json", ""), crash_files)
    lis = map(lambda i: '<li><a href="./query?id=' + i + '">' + i + '</a></li>', crash_ids)
    html = "<ul>" + '\n'.join(lis) + "</ul>"
    return (html, 200)

@app.route("/query", methods=["GET"])
@auth.login_required
def query():
    if 'id' in request.args:
        id = request.args['id']
        filename = 'crash-' + id + '.json'
        crashfile = join(config['crash_dir'], filename)
        if exists(crashfile):
          return send_file(crashfile)
        return ('Report not found', 404)
    return ('Missing ID', 400)

def main():
    global config
    with open('config.json') as f:
        config = json.loads(f.read())
        assert('port' in config)
        assert('crash_dir' in config)
        assert('read_secret' in config)
        assert('write_secret' in config)
    app.run(port=config['port'])

if __name__ == "__main__":
    main()
