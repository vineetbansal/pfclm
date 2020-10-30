from flask import Flask, request, redirect, session, url_for, render_template, abort
from flask.json import jsonify
import os

import slurm

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", message="Please use the /submit, /state, or /result URLs.")

@app.route("/submit")
def submit():
    i = int(request.args.get("i", 1))
    j = int(request.args.get("j", 1))
    t = int(request.args.get("t", 20))
    return jsonify(job_id=slurm.submit(i, j, t))


@app.route("/state/<job_id>")
def state(job_id):
    return jsonify(state=slurm.state(job_id))


@app.route("/result/<job_id>")
def result(job_id):
    return jsonify(result=slurm.result(job_id))

