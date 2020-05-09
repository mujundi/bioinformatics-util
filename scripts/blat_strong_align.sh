#!/bin/bash
#SBATCH --job-name=100
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_HERE
#SBATCH --ntasks=1
#SBATCH --mem=4gb
#SBATCH --time=00:40:00
#SBATCH --output=blat_%j.out

date;hostname;pwd

module load blat

echo "Checking if temp_nh.pslx already exists..."
if [ ! -f temp_nh.pslx ]
then
    echo "Running BLAT..."
    blat -minIdentity=90 -noHead -out=pslx /ufrc/boucher/mjundi/datasets/megares_database_v1.01.fasta /ufrc/boucher/share/100/flat.fasta temp_nh.pslx
else
    echo "File found."
fi

/ufrc/boucher/mjundi/reads_test/align_to_db.py temp_nh.pslx /ufrc/boucher/share/100/flat.fasta

date
