#!/bin/bash
#SBATCH --job-name=blat
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_HERE
#SBATCH --ntasks=1
#SBATCH --mem=2gb
#SBATCH --time=03:00:00
#SBATCH --output=blat_%j.out

date;hostname;pwd

module load blat

echo "Running BLAT..."
blat -noHead -out=pslx ../megares_database_v1.01.fasta 2m_var output_nh.pslx

date
