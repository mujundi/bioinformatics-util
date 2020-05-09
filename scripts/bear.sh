#!/bin/bash
#SBATCH --job-name=bear_test
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_HERE
#SBATCH --ntasks=1
#SBATCH --mem=4gb
#SBATCH --time=01:00:00
#SBATCH --output=bear_test_%j.out

date;hostname;pwd

module load bear


echo "Preparing abundance profile..."
./uniform_abundance.py simulated_variations.fasta snp_count.txt abundance_profile.txt
echo "Profile complete."

echo "Generating reads..."
generate_reads.py -r simulated_variations.fasta -a abundance_profile.txt -o 2m_reads.fasta -t 2000000 -l 150
echo "Reads complete."

echo "Converting to reads to FASTQ format..."
./fa_to_fq.py 2m_reads.fasta 2m_reads.fastq
echo "Conversion complete." 

date
