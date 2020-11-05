from flask import Flask, request, redirect, session, url_for, render_template, abort, send_from_directory, send_file
from flask.json import jsonify
import os
import base64

import slurm

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", message="Please use the /submit, /state, or /result URLs.")


@app.route('/submit')
def submit():
    swe = int(request.args.get("swe", 1))
    runoff = int(request.args.get("runoff", 1))
    job_id = slurm.submit(swe, runoff)
    return redirect(url_for('run', run_id=job_id))


@app.route('/run/<run_id>')
def run(run_id):
    return render_template("run.html", runid=run_id, state=slurm.state(run_id))


@app.route('/state/<job_id>')
def state(job_id):
    return jsonify(state=slurm.state(job_id))


@app.route('/result/<run_id>')
def result(run_id):
    try:
        image_path = os.path.join(os.getenv('HOME'), f'RESULTS/pfclm.{run_id}/plots/plot.png')
        img = open(image_path, 'rb').read()
        return render_template('result.html', run_id=run_id, img=base64.encodebytes(img).decode('ascii'))
    except FileNotFoundError:
        abort(404)
