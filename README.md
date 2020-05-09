# **Bioinformatics Lab Utilities**

This is a collection of tools developed for wrangling and analyzing metagenomic data, as well as batching jobs to be ran on the HiPerGator supercomputer, simulating reads and SNPs (single-nucleotide polymorphisms), and facilitating the execution of several competing research tools.

All of these scripts are **tested** and **non-destructive**. Under no circumstances will these tools move, delete, or otherwise change datasets that are passed in as parameters.

<hr>

## **Table of Contents**

### [SLURM Scripts](#SLURM)

- #### For simulating reads and SNPs:

  - [bear.sh](#bear.sh)
    - Prepares a uniform abundance profile using [uniform_abundance.py](#uniform_abundance.py), runs BEAR to generate simulated read data, then converts data to FASTQ format.
  - [blat.sh](#blat.sh)
    - Runs BLAT to produce alignment data for reads against a reference database.
  - [blat_parallel.sh](#blat.sh)
    - Same as [blat.sh](#blat.sh), but utilizes multiple threads.
  - [blat_strong_align.sh](#blat_strong_align.sh)
    - Runs BLAT but outputs alignments for stronger matches only.
  - [bwa_parallel.sh](#bwa_parallel.sh)
    - Uses BWA to map kmers to a FASTA file.
  - [extract.sh](#extract.sh)
    - Extracts kmers into their own file from BWA output.
  - [index.sh](#index.sh)
    - Runs the BWA index script on given FASTA file.

- #### Pipelines for competing tools:

  - [gatk.sh](#gatk.sh)
    - Executes the entire chain of necessary scripts for GATK, outputting a file with all detected SNPs.
  - [samtools.sh](#samtools.sh)
    - Prepares alignment data with BWA, then runs SAMtools to analyze the data to detect SNPs.

### Local Scripts

- #### For processing and/or formatting data:

  - [align_to_db.py](#align_to_db.py)
    - Aligns reads to reference database of genome(s).
  - [bloom_kmers.py](#bloom_kmers.py)
    - Processes the output of Bloom to extract kmers data.
  - [compare.py](#compare.py)
    - Compares headerless PSLX file to FASTA genes file to find SNPs.
  - [extract_kmers.py](#extract_kmers.py)
    - Extracts kmers from BWA output.
  - [fa_to_fq.py](#fa_to_fq.py)
    - Converts FASTA files to FASTQ files.
  - [fix_read_labels.py](#fix_read_labels.py)
    - Trims FASTQ read labels to remove unnecessary information.
  - [fq_to_fa.py](#fq_to_fa.py)
    - Converts FASTQ to FASTA.
  - [get_stats_and_histogram.py](#get_stats_and_histogram.py)
    - Takes in Bubbleparse output and produces statistics on matches and identified SNPs.
  - [kmer_in_reads.py](#kmer_in_reads.py)
    - Reports all reads that contain a given kmer.
  - [simulate_snps.py](#simulate_snps.py)
    - Generates simulated reads from a reference genome. The reads are given randomly generated SNPs.
  - [split.sh](#split.sh)
    - Splits FASTA paired-reads files into multiple files.
  - [trim_branches.py](#trim_branches.py)
    - Equalizes branch lengths in FASTA file.
  - [uniform_abundance.py](#uniform_abundance.py)
    - Creates uniform abundance profile for FASTA file.

<br>
<br>
<hr>
<hr>
<hr>
<br>

# SLURM

In each SLURM script, the comments are used by the workload manager to determine where job progress reports should be sent (your email address), the amount of memory to allocate, a time limit (to prevent infinitely running jobs), and where the output containing info regarding your job submission should.

The scripts themselves are only for submitting jobs to the cluster. In order to change which files are being processed, change the arguments in the commands within the files.

The time and memory demands will vary greatly with the size of datasets, so make adjustments as needed. For more info, visit https://help.rc.ufl.edu/doc/Sample_SLURM_Scripts.

<hr>
<br>

## bear.sh

Prepares a uniform abundance profile using [uniform_abundance.py](#uniform_abundance.py), runs BEAR to generate simulated read data, then converts data to FASTQ format.

### Dependencies

- [uniform_abundance.py](#uniform_abundance.py)
- [fa_to_fq.py](#fa_to_fq.py)

### Usage

```
sbatch bear.sh
```

<br>
<br>

## blat.sh

Runs BLAT to produce alignment data for reads against a reference database. The output file is headless and in PSLX format.

### Dependencies

- N/A

### Usage

```
sbatch blat.sh
```

<br>
<br>

## blat_parallel.sh

Splits single FASTA-formatted file into 4 files for BLAT to process concurrently.

### Dependencies

- N/A

### Usage

```
sbatch blat_parallel.sh
```

<br>
<br>

## blat_strong_align.sh

Runs BLAT to produce alignment data for reads against a reference database. The output file is headless and in PSLX format.

### Dependencies

- N/A

### Usage

```
sbatch blat_strong_align.sh
```

<br>
<br>

## bwa_parallel.sh

Produces kmers from paired-end reads FASTA file and metagenomic FASTA datasets using BWA. The script is set up to use 4 threads.

### Dependencies

- [extract_kmers.py](#extract_kmers.py)

### Usage

```
sbatch bwa_parallel.sh
```

<br>
<br>

## extract.sh

Times the kmers extraction script that runs in the BWA pipeline from [bwa_parallel.sh](#bwa_parallel.sh).

### Dependencies

- [extract_kmers.py](#extract_kmers.py)

### Usage

```
sbatch extract.sh
```

<br>
<br>

## index.sh

Indexes FASTA files for the BWA pipeline.

### Dependencies

- N/A

### Usage

```
sbatch index.sh
```

<br>
<br>

## **_Competing Tools_**

## gatk.sh

GenomeAnalysisTK pipeline from start to finish. All it needs is the reference dataset and the reads FASTQ file. It uses Picard to create the necessary intermediate indexed BAM file.

### Dependencies

- BWA
- Picard

### Usage

```
sbatch gatk.sh
```

<br>
<br>

## samtools.sh

Prepares alignment data with BWA, then runs SAMtools to analyze the data to detect SNPs.

### Dependencies

- BWA
- BCFtools
- Picard

### Usage

```
sbatch samtools.sh
```

<br>
<br>

# Local Scripts

<br>

## align_to_db.py

Takes in a headless PSLX (created by BLAT) and comparison file to find best matches to a reference database of gene sequences.

### Usage

```
./align_to_db.py <pslx file> <reference file>
```

<br>
<br>

## bloom_kmers.py

Finds coverage for each kmer from Bloom output file and tallies kmer occurances.

### Usage

```
./bloom_kmers.py <bloom file> <output file>
```

<br>
<br>

## compare.py

Takes in output of BLAT on simulated reads and reference dataset to find matches, and produce statistics for positive, negative, and false positive matches.

### Usage

```
./compare.py <blat file> <snps_file>
```

<br>
<br>

## extract_kmers.py

Copies kmers from BWA output into their own file for use in other scripts and tools.

### Usage

```
./extract_kmers.py <bwa file> <output file>
```

<br>
<br>

## fa_to_fq.py

Takes in a FASTA file and adds dummy confidence data to convert to FASTQ format.

### Usage

```
./fa_to_fq.py <input file> <output file>
```

<br>
<br>

## fix_read_labels.py

Trims superfluous data from labels in FASTA/FASTQ reads files.

### Usage

```
./fix_read_labels.py <input file> <output file>
```

<br>
<br>

## fq_to_fa.py

Takes in a FASTQ file and removes confidence data to convert to FASTA format.

### Usage

```
./fq_to_fa.py <input file> <output file>
```

<br>
<br>

## get_stats_and_histogram.py

Takes in the output of BLAT as input. Finds best matches from SNP detection queries to reference genes, outputs statistics on the lengths of reconstructed gene sequences, and generates a histogram plot with the data.

### Usage

```
./get_stats_and_histogram.py <input BLAT file>
```

<br>
<br>

## kmer_in_reads.py

Finds coverage and occurance of kmers in BLAT file.

### Usage

```
./kmer_in_reads.py <input file> <output file>
```

<br>
<br>

## simulate_snps.py

Uses the MegaRes database to produce simulated SNPs in known AMR-coding genes. SNPs are inserted at random throughout the dataset as it is created.

Takes in a FASTA file and outputs a log of SNP data, gene representation data, and a FASTA file for the genes and gene variants;

### Usage

```
./simulate_snps.py
```

<br>
<br>

## split.sh

Takes in a FASTA file and splits it into 4 files.

### Usage

```
./split.sh <input file> <output file>
```

<br>
<br>

## trim_branches.py

Trims branches of variations fasta file to equalize branch lengths.

### Usage

```
./trim_branches.py <input file> <output file>
```

<br>
<br>

## uniform_abundance.py

Creates relative abundance profile with uniform abundance.

Format for output: `<fasta header> \t <abundance percentage>`

### Usage

```
./uniform_abundance.py <input file> <output file>
```

<br>
<br>
