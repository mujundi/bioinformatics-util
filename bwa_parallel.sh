#!/bin/bash
#SBATCH --job-name=bwa
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_HERE
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32gb
#SBATCH --time=00:50:00
#SBATCH --output=bwa%j.out


# To use this script, just replace all of the pair.fasta and sim.fasta with
# whichever kmer file and reads file you want to use. The files it produces
# take up a few GB of space, and the final output will be named "kmers.txt".


date;hostname;pwd

echo
echo

module load bwa
module load gcc


bwa index sim.fasta       

#split into temp_aa,...,temp_ad
declare -i t
lines=($(wc -l pair.fasta))
t=${lines[0]}/4
split -l $t pair.fasta temp_
wc -l temp_*
declare -i u
v=($(wc -l temp_ad))
u=${v[0]}
t=$t-500
u=$u-500
{
declare -i a
declare -i counta
counta=0
while [ $counta -le $t ]
do
    a=counta+500
    head -n $a temp_aa | tail -500 > temp1
    bwa aln -n 0.001 sim.fasta temp1 > out1.sai
    bwa samse -n 100000 sim.fasta out1.sai temp1 > out1.sam
    sed '/^@/ d' < out1.sam > out1_nh.sam
    ./extract_kmers.py out1_nh.sam kmers1.txt
    rm out1*
    rm temp1
    counta+=500
done
diffa=$(($t%500))
tail -n $diffa temp_aa > temp1
bwa aln -n 0.001 sim.fasta temp1 > out1.sai
bwa samse -n 100000 sim.fasta out1.sai temp1 > out1.sam
sed '/^@/ d' < out1.sam > out1_nh.sam
./extract_kmers.py out1_nh.sam kmers1.txt
rm out1*
rm temp1

} &

{
declare -i b
declare -i countb
countb=0
while [ $countb -le $t ]
do
    b=countb+500
    head -n $b temp_ab | tail -500 > temp2
    bwa aln -n 0.001 sim.fasta temp2 > out2.sai
    bwa samse -n 100000 sim.fasta out2.sai temp2 > out2.sam
    sed '/^@/ d' < out2.sam > out2_nh.sam
    ./extract_kmers.py out2_nh.sam kmers2.txt
    rm out2*
    rm temp2
    countb+=500
done
diffb=$(($t%500))
tail -n $diffb temp_ab > temp2
bwa aln -n 0.001 sim.fasta temp2 > out2.sai
bwa samse -n 100000 sim.fasta out2.sai temp2 > out2.sam
sed '/^@/ d' < out2.sam > out2_nh.sam
./extract_kmers.py out2_nh.sam kmers2.txt
rm out2*
rm temp2
} &

{
declare -i c
declare -i countc
countc=0
while [ $countc -le $t ]
do
    c=countc+500
    head -n $c temp_ac | tail -500 > temp3
    bwa aln -n 0.001 sim.fasta temp3 > out3.sai
    bwa samse -n 100000 sim.fasta out3.sai temp3 > out3.sam
    sed '/^@/ d' < out3.sam > out3_nh.sam
    ./extract_kmers.py out3_nh.sam kmers3.txt
    rm out3*
    rm temp3
    countc+=500
done
diffc=$(($t%500))
tail -n $diffc temp_ac > temp3
bwa aln -n 0.001 sim.fasta temp3 > out3.sai
bwa samse -n 100000 sim.fasta out3.sai temp3 > out3.sam
sed '/^@/ d' < out3.sam > out3_nh.sam
./extract_kmers.py out3_nh.sam kmers3.txt
rm out3*
rm temp3
} &

{
declare -i d
declare -i countd
countd=0
while [ $countd -le $u ]
do
    d=countd+500
    head -n $d temp_ad | tail -500 > temp4
    bwa aln -n 0.001 sim.fasta temp4 > out4.sai
    bwa samse -n 100000 sim.fasta out4.sai temp4 > out4.sam
    sed '/^@/ d' < out4.sam > out4_nh.sam
    ./extract_kmers.py out4_nh.sam kmers4.txt
    rm out4*
    rm temp4
    countd+=500
done
diffd=$(($u%500))
tail -n $diffd temp_ad > temp4
bwa aln -n 0.001 sim.fasta temp4 > out4.sai
bwa samse -n 100000 sim.fasta out4.sai temp4 > out4.sam
sed '/^@/ d' < out4.sam > out4_nh.sam
./extract_kmers.py out4_nh.sam kmers4.txt
rm out4*
rm temp4
} &

echo "Running BWA..."
wait
rm *.fasta.{amb,ann,bwt,pac,sa}
wc -l kmers*
cat kmers1.txt kmers2.txt kmers3.txt kmers4.txt > kmers.txt
rm kmers{1,2,3,4}.txt
rm temp_*
echo "Kmers stored in kmers.txt."


#bwa aln -n 0.001 sim.fasta pair.fasta > out.sai
#bwa samse -n 100000 sim.fasta out.sai pair.fasta > out.sam
#sed '/^@/ d' < out.sam > out_nh.sam
#./extract_kmers.py out_nh.sam

date
