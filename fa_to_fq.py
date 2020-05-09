#!/usr/bin/env python

# Takes in a FASTA file of reads and converts the format to FASTQ

import sys
import random

random.seed()

infile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')

counter = 1
read_num = 1

for line in infile:
	if counter % 2:
		outfile.write("@{0}\n".format(read_num))
		read_num += 1
	else:
		for i,base in enumerate(line[:-1]):
			if random.random() > 0.999:
				if base == 'A': bases = ['T','G','C']
				elif base == 'T': bases = ['A','G','C']
				elif base == 'G': bases = ['A','T','C']
				else: bases = ['A','T','G']
				
				error_base = random.choice(bases)
				line = line[:i] + error_base + line[i+1:]

				
		outfile.write(line)
		outfile.write("+\n")
		outfile.write("~"*(len(line)-1) + "\n")
		
	counter += 1


infile.close()
outfile.close()
