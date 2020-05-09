#!/usr/bin/env python


import sys


with open(sys.argv[1], 'r') as bwa:
	with open(sys.argv[2], 'a') as outfile:
		at_start = True
					
		for line in bwa:
			try:	
				x = line.split('\t')
				kmer = x[0]
				reads = ["aa" + x[2]]

				is_start = True
				matches = x[18].split(',')
				for match in matches[0::3]:
					if is_start:
						reads.append(match[3:])
						is_start = False
					else:
						reads.append(match)

				del reads[-1]
				trimmed = [x[2:] for x in reads]
				outfile.write(kmer + "\t")
				is_start = True
				for read in trimmed:
					if is_start:
						outfile.write(read)
						is_start = False
					else:
						outfile.write("," + read)
				outfile.write("\n")

				del reads[:]
				del matches[:]
			except Exception:
				outfile.write(kmer + "\t")
				outfile.write(x[2] + "\n")
				del reads[:]
				del matches[:]
				continue
					
								 
		print("Extraction for " + sys.argv[2] + " complete.\n")

bwa.close()
outfile.close()

