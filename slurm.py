import os.path
import subprocess
import tempfile
from flask import render_template
from flask.json import dumps


def submit(swe, runoff):
    s = render_template('sbatch.sh', swe=swe, runoff=runoff)
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(s.encode('utf8'))
    f.close()

    stdout, stderr = subprocess.Popen(["sbatch", f.name], stdout=subprocess.PIPE, shell=False).communicate()
    job_id = stdout.decode('utf8').split()[-1]

    return job_id

def state(job_id):
    stdout, stderr = subprocess.Popen(["sacct", "-j", f"{job_id}", "--format", "jobid,state"], stdout=subprocess.PIPE, shell=False).communicate()
    stdout = stdout.decode('utf8')
    status = 'UNKNOWN'
    for line in stdout.split('\n'):
        if line.startswith(f'{job_id}.batch'):
            status = line.split()[-1].strip()

    return status

def result(job_id):
    contents = ''
    outfile = f'out/slurm-{job_id}.out'
    if os.path.exists(outfile):
        contents = open(outfile, 'r').read().strip()

    return contents

