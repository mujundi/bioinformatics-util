#!/usr/bin/env python


import sys


with open(sys.argv[1], 'r') as infile:
	with open(sys.argv[2], 'w') as outfile:
		for line in infile:
			if line[0] == "@":
				x = line.split()
		 		outfile.write("@" + x[2] + "\n")
		 	else:
		 		outfile.write(line)

infile.close()
outfile.close()
