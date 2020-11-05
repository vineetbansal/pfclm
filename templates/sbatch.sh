#!/bin/bash
#SBATCH --job-name=pfclm
#SBATCH --ntasks=1
#SBATCH --time=1:00
#SBATCH -o out/slurm-%j.out

module load parflow-anaconda3

python pfclm.py ~/RESULTS/pfclm.$SLURM_JOB_ID
python plots.py ~/RESULTS/pfclm.$SLURM_JOB_ID/output PFCLM_SC ~/RESULTS/pfclm.$SLURM_JOB_ID/plots

