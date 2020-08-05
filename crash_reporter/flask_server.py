from datetime import datetime
from flask import Flask, request, send_file
from os import listdir
from os.path import exists, isfile, join
import json
app = Flask(__name__)

crash_dir = None

@app.route("/report", methods=["POST"])
def report():
    report = request.get_json()
    id = 0
    idstr = None
    date = datetime.today().strftime('%Y-%m-%d')
    while True:
      idstr = str(id).zfill(4)
      filename = 'crash-' + date + "-" +  idstr + '.json'
      crashfile = join(crash_dir, filename)
      if not exists(crashfile):
        break;
      id += 1
    with open(crashfile, 'w') as outfile:
      json.dump(report, outfile)
      return (date + "-" + idstr, 200)

@app.route("/list", methods=["GET"])
def list():
    crash_files = [f for f in listdir(crash_dir) if isfile(join(crash_dir, f)) and f.startswith("crash-")]
    crash_ids = map(lambda f: f.replace("crash-","").replace(".json", ""), crash_files)
    lis = map(lambda i: '<li><a href="./query?id=' + i + '">' + i + '</a></li>', crash_ids)
    html = "<ul>" + '\n'.join(lis) + "</ul>"
    return (html, 200)

@app.route("/query", methods=["GET"])
def query():
    if 'id' in request.args:
        id = request.args['id']
        filename = 'crash-' + id + '.json'
        crashfile = join(crash_dir, filename)
        return send_file(crashfile)
    return ('', 404)

def main():
    with open('config.json') as f:
        config = json.loads(f.read())
        assert('port' in config)
        assert('crash_dir' in config)
        global crash_dir
        crash_dir = config['crash_dir']
    app.run(port=config['port'])

if __name__ == "__main__":
    main()
