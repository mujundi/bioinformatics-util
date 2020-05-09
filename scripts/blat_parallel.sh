#!/bin/bash
#SBATCH --job-name=86
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_HERE
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4gb
#SBATCH --time=00:45:00
#SBATCH --output=bulge%j.out


# To use this script, just replace all of the pair.fasta and flat.fasta with
# whichever kmer file and reads file you want to use. The files it produces
# take up a few GB of space, and the final output will be named "kmers.txt".


date;hostname;pwd
echo
echo

module load blat
module load gcc

#set -xe 
#mkdir -p kmc_temp
#cat *.fastq > all.flat
#rm *.fastq
#python /ufrc/boucher/baharpan/cosmo/id_convert.py all.flat id_all.flat
#rm all.flat
#wc -l id_all.flat > subreads_info
#ls -1 --color=no *.flat |xargs -l -i echo "/ufrc/boucher/baharpan/cosmo/3rd_party_src/KMC/bin/kmc -b -fq -ci12 -k32  {} {}.kmc kmc_temp" >kmercount.sh
#source kmercount.sh
#ls -1 --color=no *.flat |xargs -l -i echo "/ufrc/boucher/baharpan/cosmo/3rd_party_src/KMC/bin/kmc_tools sort {}.kmc {}.kmc.sorted " >kmercountsort.sh
#source kmercountsort.sh
#ls -1 --color=no *.flat |xargs -l -i echo "{}.kmc.sorted" > filtered_kmc2_list
#
#numactl --interleave=all  /ufrc/boucher/baharpan/cosmo/cosmo-pack -k filtered_kmc2_list
#python /ufrc/boucher/baharpan/oak/notebooks/fasta.py pair pair.fasta


#split into temp_aa,...,temp_ad
declare -i t
lines=($(wc -l pair.fasta))
t=${lines[0]}/4
split -l $t pair.fasta temp_
wc -l temp_*
declare -i u
declare -i n_lines
n_lines=10000
v=($(wc -l temp_ad))
u=${v[0]}
t=$t-$n_lines
u=$u-$n_lines
{
declare -i a
declare -i counta
counta=0
while [ $counta -le $t ]
do
    a=counta+$n_lines
    head -n $a temp_aa | tail -$n_lines > temp1
    blat -minIdentity=100 -minScore=32 -tileSize=8 -noHead -out=psl flat.fasta temp_aa out1_nh.psl
    /ufrc/boucher/mjundi/kmer_blat/kmer_in_reads.py out1_nh.psl kmers1.txt
    rm out1*
    rm temp1
    counta+=$n_lines
done
diffa=$(($t%$n_lines))
tail -n $diffa temp_aa > temp1
blat -minIdentity=100 -minScore=32 -tileSize=8 -noHead -out=psl flat.fasta temp_aa out1_nh.psl
/ufrc/boucher/mjundi/kmer_blat/kmer_in_reads.py out1_nh.psl kmers1.txt
rm out1*    
rm temp1
} &

{
declare -i b
declare -i countb
countb=0
while [ $countb -le $t ]
do
    b=countb+$n_lines
    head -n $b temp_ab | tail -$n_lines > temp2
    blat -minIdentity=100 -minScore=32 -tileSize=8 -noHead -out=psl flat.fasta temp_ab out2_nh.psl
    /ufrc/boucher/mjundi/kmer_blat/kmer_in_reads.py out2_nh.psl kmers2.txt
    rm out2*
    rm temp2
    countb+=$n_lines
done
diffb=$(($t%$n_lines))
tail -n $diffb temp_ab > temp2
blat -minIdentity=100 -minScore=32 -tileSize=8 -noHead -out=psl flat.fasta temp_ab out2_nh.psl
/ufrc/boucher/mjundi/kmer_blat/kmer_in_reads.py out2_nh.psl kmers2.txt
rm out2*
rm temp2
} &

{
declare -i c
declare -i countc
countc=0
while [ $countc -le $t ]
do
    c=countc+$n_lines
    head -n $c temp_ac | tail -$n_lines > temp3
    blat -minIdentity=100 -minScore=32 -tileSize=8 -noHead -out=psl flat.fasta temp_ac out3_nh.psl
    /ufrc/boucher/mjundi/kmer_blat/kmer_in_reads.py out3_nh.psl kmers3.txt
    rm out3*
    rm temp3
    countc+=$n_lines
done
diffc=$(($t%$n_lines))
tail -n $diffc temp_ac > temp3
blat -minIdentity=100 -minScore=32 -tileSize=8 -noHead -out=psl flat.fasta temp_ac out3_nh.psl
/ufrc/boucher/mjundi/kmer_blat/kmer_in_reads.py out3_nh.psl kmers3.txt
rm out3*
rm temp3
} &

{
declare -i d
declare -i countd
countd=0
while [ $countd -le $u ]
do
    d=countd+$n_lines
    head -n $d temp_ad | tail -$n_lines > temp4
    blat -minIdentity=100 -minScore=32 -tileSize=8 -noHead -out=psl flat.fasta temp_ad out4_nh.psl
    /ufrc/boucher/mjundi/kmer_blat/kmer_in_reads.py out4_nh.psl kmers4.txt
    rm out4*
    rm temp4
    countd+=$n_lines
done
diffd=$(($u%$n_lines))
tail -n $diffd temp_ad > temp4
blat -minIdentity=100 -minScore=32 -tileSize=8 -noHead -out=psl flat.fasta temp_ad out4_nh.psl
/ufrc/boucher/mjundi/kmer_blat/kmer_in_reads.py out4_nh.psl kmers4.txt
rm out4*
rm temp4
} &

echo "Running BLAT..."
wait
wc -l kmers*
cat kmers1.txt kmers2.txt kmers3.txt kmers4.txt > KMERS_TEMP.txt
rm kmers{1,2,3,4}.txt
rm temp_*
echo "Kmers stored in kmers.txt."


#bwa aln -n 0.001 sim.fasta pair.fasta > out.sai
#bwa samse -n 100000 sim.fasta out.sai pair.fasta > out.sam
#sed '/^@/ d' < out.sam > out_nh.sam
#./extract_kmers.py out_nh.sam
echo
#/usr/bin/time -v /ufrc/boucher/baharpan/cosmo/fast_matrix
#/usr/bin/time -v /ufrc/boucher/baharpan/cosmo/bubbles
#date

date
