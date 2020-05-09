#!/usr/bin/env python

# Takes in a pslx file (w/ no header) and comparison file
# Usage: ./compare.py <pslx file> <compare file>
# Output 1: Gene, index, SNP bases.
# Output 2: SNPs not found in Output 1

from itertools import izip_longest
import sys
import time


def find_best_match(bests, q_lines):
    best_match = 0

    for i in q_lines:
        if best_match == 0:
            best = i
            best_match = int(i[0])
        elif int(i[0]) > best_match:
            del best[:]
            best = i
            best_match = int(i[0])
            
    bests.append(best)
    return 0,0,0,0



with open(sys.argv[1], 'r') as blat_file:
    
    counter = 0
    q_lines = []
    bests = []
    
    for line in blat_file:
        try:
            data = line.split('\t')

            q_name = data[9]
             
            if counter == 0:
                q_prev = q_name
                q_lines.append(data)
                counter += 1
            
            if q_name == q_prev:
                q_lines.append(data)
            else:
                find_best_match(bests, q_lines) 
                del q_lines[:]
                q_lines.append(data)
            
            q_prev = q_name
        except Exception:
            continue

    find_best_match(bests, q_lines)
    
blat_file.close()


gene_file = open("found_genes.txt", 'w')

for q in bests:
    gene_file.write(q[13] + "\n")

gene_file.close()

counter = 0
aln_count = 0
reads_file = open(sys.argv[2], 'r')
aln_reads_file = open("aligned_only.fasta", 'w')

# The way it works is that it goes through the sample reads 2 lines at a time,
# so that the read ID and sequence are taken at the same time. If the name of
# the read matches one in the list of aligned reads, it is written to the new
# FASTA file "aligned_only.fasta". Also, if the read ID is larger than the ID
# of the aligned read it is checking, it breaks the loop and goes to the next
# since both lists are sorted in ascending order.
for read, seq in izip_longest(*[reads_file]*2):    

    temp = read.strip()
    for q in bests:
        if int(temp[1:]) < int(q[9]):
            break

        if (">" + q[9]) == temp:
            aln_reads_file.write(read)
            aln_reads_file.write(seq)
            aln_count += 1
            bests.pop(0)
            break

    if counter % 1000000 == 0:
        print("Reads checked: " + str(counter))
    counter += 1

print("\nExtraction complete.")
print("Total reads checked: " + str(counter))
print("Aligned reads: " + str(aln_count) + "\n")
reads_file.close()
aln_reads_file.close()




                        
