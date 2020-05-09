#!/bin/bash
#SBATCH --job-name=bwa
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_HERE
#SBATCH --ntasks=1
#SBATCH --mem=8gb
#SBATCH --time=03:00:00
#SBATCH --output=bwa_%j.out



date;hostname;pwd

/usr/bin/time -v ./extract_kmers.py out_nh.sam

date
