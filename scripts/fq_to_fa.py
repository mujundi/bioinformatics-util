#!/usr/bin/env python

# Converts fastq to fasta
# ./fq_to_fa.py <input> <output>

import sys


with open(sys.argv[1], 'r') as infile:
	with open(sys.argv[2], 'w') as outfile:
		counter = 1
		for line in infile:
			if counter%4 == 1:
				outfile.write(">" + line[1:])
			elif counter%4 == 2:
				outfile.write(line)
			counter += 1		



		
		#lines = infile.readlines()
		#for id, seq in zip(lines[0::4],lines[1::4]):
		#	outfile.write(">" + id.split()[2] + "\n")	# use this for IDs of "Read #: 1"
		#	outfile.write(">" + id[1:])  # for IDs of "@1", "@2", etc.
		#	outfile.write(seq)
		
infile.close()
outfile.close()
