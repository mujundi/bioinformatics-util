#!/bin/bash
#SBATCH --job-name=samtools
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_HERE
#SBATCH --ntasks=1
#SBATCH --mem=16gb
#SBATCH --time=08:00:00
#SBATCH --output=sam_%j.out

date;hostname;pwd

module load samtools
module load bwa



echo
echo

/usr/bin/time -v bwa index ../ref.fasta
/usr/bin/time -v bwa aln ../ref.fasta ../ref.fastq > out.sai
/usr/bin/time -v bwa samse ../ref.fasta out.sai 2m_reads.fastq > out.sam

/usr/bin/time -v samtools view -S -b out.sam > out.bam
/usr/bin/time -v samtools sort out.bam -o out-sorted.bam
/usr/bin/time -v samtools faidx ../ref.fasta
/usr/bin/time -v samtools mpileup -g -f ../ref.fasta out-sorted.bam > raw.bcf

module load bcftools
module load samtools

/usr/bin/time -v bcftools view -v snps -m2 raw.bcf -o var.bcf
/usr/bin/time -v bcftools view var.bcf | vcfutils.pl varFilter -d 5 > var-final.vcf

module load picard
module load gatk

/usr/bin/time -v picard CreateSequenceDictionary R=../ref.fasta O= ../gene_bank.dict
/usr/bin/time -v GenomeAnalysisTK -R ../ref.fasta -T VariantsToTable -V var-final.vcf -F CHROM -F POS -F QUAL -F REF -F ALT -o var-table

echo
echo

date
