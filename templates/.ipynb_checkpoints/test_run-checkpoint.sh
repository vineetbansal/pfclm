#!/bin/bash
#SBATCH --job-name=test
#SBATCH --ntasks=1
#SBATCH --time=1:00

module load parflow
module load parflow-anaconda3

cd ~/RESULTS
mkdir sub-test.$SLURM_JOB_ID
cd sub-test.$SLURM_JOB_ID

cp -r /home/reedmm/PFCLM-test/single_column_CLM .
cd single_column_CLM
python3 PFCLM_SC.py
echo args: {{swe}} {{runoff}}
python3 CLM_plots.py {{swe}} {{runoff}} 
cp pfclmplot.png ../../ 
