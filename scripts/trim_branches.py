#!/usr/bin/env python

# Trims branches of variations fasta file to equalize branch lengths


import sys


with open(sys.argv[1], 'r') as infile:
     with open("t_" + sys.argv[1], 'w') as outfile:
          counter = 1
          lines = infile.readlines()
          branches = []
          for q,seq in zip(lines[0::2],lines[1::2]):
               x = q.split('.')
               bulge = x[0]
               base = seq[int(x[2])-1]
               if counter == 1:
                    bulge_prev = bulge
                    base_prev = base
                    counter += 1 

               if (bulge == bulge_prev):
                    branches.append([q,seq.rstrip(),len(seq)-1])
               else:
                    n = min(branches, key=lambda x: x[2])[2] 
                    for branch in branches:
                         outfile.write(branch[0])
                         outfile.write(branch[1][:n] + "\n")
                    del branches [:]
                    branches.append([q,seq.rstrip(),len(seq)-1])


               base_prev = base
               bulge_prev = bulge

                                             

infile.close()
outfile.close()
