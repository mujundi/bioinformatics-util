#!/usr/bin/env python

# Creates relative abundance profile with uniform abundance
# Format for running: ./uniform_abundance.py <fasta input> <count file> <output file>
# Format for output:  <fasta header> \t <abundance percentage>

from decimal import *
import sys


infile = open(sys.argv[1],'r')
countfile = open(sys.argv[2], 'r')

lines = countfile.readlines()
words = lines[1].split()

gene_count = int(words[3]) + 4642 + 3103
print(gene_count)
percentage = Decimal(1) / Decimal(gene_count)
print(percentage)
counter = 1

with open(sys.argv[3],'w') as outfile:
	for line in infile:
		if counter % 2:
			outfile.write(line[:-1] + "\t" + str(percentage) + "\n")
		
		counter += 1		

print(percentage * gene_count)

infile.close()
countfile.close()
outfile.close()			
