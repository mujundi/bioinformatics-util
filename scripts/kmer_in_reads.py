#!/usr/bin/env python

from __future__ import print_function
import sys


with open(sys.argv[1], 'r') as blat:
	outfile = open(sys.argv[2], 'a')		
	kmer = ""
	reads = ""
	at_start = True
	progress = 1
	for line in blat:
		x = line.split()
		
		if at_start:
			kmer = x[9]
			reads = [x[13]]
			at_start = False
		
		elif x[9] == kmer:
			reads.append(x[13])
		else:
			reads.sort()
			outfile.write(kmer + "\t")
			first = True
			for i in reads:
				if first:
					outfile.write(i)
					first = False
				else: 
					outfile.write("," + i)
			outfile.write("\n")
			
			kmer = x[9]
			del reads[:]
			reads = [x[13]]

		#output = "Progress: {0} ".format(progress)
		#print(output,end='\r')
		#sys.stdout.flush()
		#progress += 1
		
		
	
	outfile.write(kmer + "\t")
	first = True
	for i in reads:
		if first:
			outfile.write(i)
			first = False
		else: 
			outfile.write("," + i)
	outfile.write("\n")
	print("Extraction complete.\n")

blat.close()
outfile.close()
