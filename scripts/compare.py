#!/usr/bin/env python

# Takes in a pslx file (w/ no header) and comparison file
# Usage: ./compare.py <pslx file> <compare file>
# Output 1: Gene, index, SNP bases.
# Output 2: SNPs not found in Output 1


import sys



def find_best_match(bests, q_lines):
     best_match = 0
     best = []
     for i in q_lines:
          # Takes care of ties
          if int(i[0]) > best_match:
               del best[:]
               best.append(i)
               best_match = int(i[0])
          elif int(i[0]) == best_match:
               best.append(i)
               
     bests.append(best)
     return 0,0,0,0



def is_SNP(branch1, branch2):
     for i in branch1:
          for j in branch2:
               # Are the gene names the same?
               if i[13] == j[13]:
                    count = int(i[9].split('.')[2]) - 1
                    index = int(i[15])-int(i[11]) + count
                    base1 = i[21][count]
                    count = int(j[9].split('.')[2]) - 1
                    base2 = j[21][count]
                    return i[13], index, base1, base2
     return None,None,None,None
                         


with open(sys.argv[1], 'r') as blat_file:
     
     counter = 0
     q_lines = []
     bests = []
     
     for line in blat_file:
          try:
               data = line.split('\t')
               q = data[9].split('.')

               q_name = q[0]
               index = int(q[2]) - 1
               base = data[21][int(index) - int(data[11])]
               if index < int(data[11]):
                    continue            
                
               if counter == 0:
                    q_prev = q_name
                    base_prev = base
                    q_lines.append(data)
                    counter += 1
               
               if q_name == q_prev and base == base_prev:
                    q_lines.append(data)
               else:
                    find_best_match(bests, q_lines)    
                    del q_lines[:]
                    q_lines.append(data)
               
               q_prev = q_name
               base_prev = base
          except Exception:
               continue       

     find_best_match(bests, q_lines)
     
     snp_file = open("blat_SNPs.txt", 'w')
     
     for b1, b2 in zip(bests[0::2], bests[1::2]):
          gene, index, letter1, letter2 = is_SNP(b1, b2)
          
          if gene is not None:
               snp_file.write(">" + gene)
               snp_file.write("\nIndex: {0} \n".format(index))
               snp_file.write("SNP: {0} <--> {1} \n\n".format(letter1,letter2).upper())
               
snp_file.close()         
blat_file.close()

with open(sys.argv[2], 'r') as log_file:
     with open("blat_SNPs.txt", 'r') as snp_file:
          lines = log_file.readlines()
          log_genes = [line for line in lines[0::4]]
          temp = [line.split() for line in lines[1::4]]          
          log_indexes = [x[1] for x in temp]
          temp = [line.split() for line in lines[2::4]]
          log_snps = [[x[1],x[3]] for x in temp]
          used = [0]*len(log_genes)
          log_data = [list(x) for x in zip(log_genes, log_indexes, log_snps, used)]
          
          del lines[:]
          del used[:]

          lines = snp_file.readlines()
          blat_genes = [line for line in lines[0::4]]
          temp = [line.split() for line in lines[1::4]]          
          blat_indexes = [x[1] for x in temp]
          temp = [line.split() for line in lines[2::4]]
          blat_snps = [[x[1],x[3]] for x in temp]
          used = [0]*len(blat_genes)
          blat_data = [list(x) for x in zip(blat_genes, blat_indexes, blat_snps, used)]
          
          for l_snp in log_data:
               for b_snp in blat_data:
                    if (l_snp[0] == b_snp[0]) and (l_snp[1] == b_snp[1]):
                         if (l_snp[2][0] in b_snp[2]) and (l_snp[2][1] in b_snp[2]):
                              l_snp[3] = 1
                              b_snp[3] = 1
                              
          l_used = [x[3] for x in log_data]
          b_used = [x[3] for x in blat_data]

          found = l_used.count(1)
          missed = l_used.count(0)
          false_pos = b_used.count(0)

          outfile = open("missed.txt", 'w')
          fp_file = open("fp.txt", 'w')
          for log, used in zip(log_data,l_used):
               if not used:
                    outfile.write(log[0])
                    outfile.write("Index: " + log[1] + "\n")
                    outfile.write("SNP: " + str(log[2]) + "\n\n")
          for log, used in zip(blat_data,b_used):
               if not used:
                    fp_file.write(log[0])
                    fp_file.write("Index: " + log[1] + "\n")
                    fp_file.write("SNP: " + str(log[2]) + "\n\n")


          result_file = open("results.txt", 'w')
          result_file.write("Found: " + str(found) + "\n")
          result_file.write("Missed: " + str(missed) + "\n")
          result_file.write("False positives: " + str(false_pos) + "\n")
          result_file.close()

          outfile.close()
          fp_file.close()
snp_file.close()
log_file.close()
          
                              
