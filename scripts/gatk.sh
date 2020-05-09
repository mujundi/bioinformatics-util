#!/bin/bash
#SBATCH --job-name=samtools
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_HERE
#SBATCH --ntasks=1
#SBATCH --mem=16gb
#SBATCH --time=03:00:00
#SBATCH --output=sam_%j.out

date;hostname;pwd

module load gatk
module load picard
module load bwa



echo
echo

/usr/bin/time -v bwa mem -R "@RG\tSM:TEST" ../megares_database_v1.01.fasta ../2m_reads.fastq > aln.sam

/usr/bin/time -v picard CreateSequenceDictionary R=../megares_database_v1.01.fasta O= ../megares_database_v1.01.dict

/usr/bin/time -v picard SortSam I=aln.sam O=sorted.bam SORT_ORDER=coordinate

/usr/bin/time -v picard MarkDuplicates I=sorted.bam O=dedup.bam METRICS_FILE=metrics.txt

/usr/bin/time -v picard BuildBamIndex INPUT=dedup.bam

/usr/bin/time -v GenomeAnalysisTK -T RealignerTargetCreator -R ../megares_database_v1.01.fasta -I dedup.bam -o targetintervals.list

/usr/bin/time -v GenomeAnalysisTK -T IndelRealigner -R ../megares_database_v1.01.fasta -I dedup.bam -targetIntervals targetintervals.list -o realigned.bam

/usr/bin/time -v GenomeAnalysisTK -T HaplotypeCaller -R ../megares_database_v1.01.fasta -I realigned.bam -ploidy 1 -stand_call_conf 30 -stand_emit_conf 10 -o rawg.vcf

/usr/bin/time -v GenomeAnalysisTK -T SelectVariants -R ../megares_database_v1.01.fasta -V rawg.vcf -selectType SNP -o snps.vcf

/usr/bin/time -v GenomeAnalysisTK -R ../megares_database_v1.01.fasta -T VariantsToTable -V snps.vcf -F CHROM -F POS -F QUAL -F REF -F ALT -o snps-table

echo
echo

date
