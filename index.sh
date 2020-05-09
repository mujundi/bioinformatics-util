#SBATCH --job-name=index
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_HERE
#SBATCH --ntasks=1
#SBATCH --mem=4gb
#SBATCH --time=00:15:00
#SBATCH --output=index_%j.out



date;hostname;pwd

echo

module load bwa


/usr/bin/time -v bwa index sim.fasta

echo

date
