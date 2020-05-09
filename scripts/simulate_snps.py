#!/usr/bin/env python

# Simulates SNPs from FASTA file


import random

def generate_snp(line):

	max = len(line) - 2
	index = random.randint(1, max)	
	
	ref_base = line[index]
	if ref_base == 'A': bases = ['T','G','C']
	elif ref_base == 'T': bases = ['A','G','C']
	elif ref_base == 'G': bases = ['A','T','C']
	else: bases = ['A','T','G']
		
	new_base = random.choice(bases)
	
	sequence = line[:index] + new_base + line[index + 1:]
	
	return index, ref_base, new_base, sequence
	
	
def generate_copies(header, sequence, outfile, copyfile):
	
	num_of_copies = random.randint(2,8)
	
	copyfile.write(header)
	copyfile.write("Number of copies: {0} \n\n".format(num_of_copies))
	
	for i in range(num_of_copies):
		outfile.write(header)
		outfile.write(sequence)
	
	return num_of_copies
	
		

alpha = 250

random.seed()


infile = open('../megares_database_v1.01.fasta', 'r')
outfile = open('simulated_variations.fasta', 'w')
outfile_copyless = open('genes.fasta', 'w')
logfile = open('snp_log.txt', 'w')
copyfile = open('gene_counts.txt', 'w')
countfile = open('snp_count.txt', 'w')

counter = 0
num_of_SNPs = 0
total_gene_count = 0
depth = 0

for line in infile:

	if counter % 2:
	
		header = temp[:-1] + "|REF\n"
		
		outfile_copyless.write(header)
		outfile_copyless.write(line)
		
		total_gene_count += generate_copies(header, line, outfile, copyfile)
		
		x = random.random() * (1 - alpha*(1 / len(line)))
		
		if x > 0.85:
			var_num = 1
			
			while x > 0.85:
			
				if var_num > depth:
					depth = var_num
				logfile.write(temp)
				header = temp[:-1] + "|VAR_{0}\n".format(var_num)
				
				index, ref_base, new_base, sequence = generate_snp(line)
				
				outfile_copyless.write(header)
				outfile_copyless.write(sequence)				
								
				total_gene_count += generate_copies(header, sequence, outfile, copyfile)

				logfile.write("Index: {0} \n".format(index))
				logfile.write("SNP: {0} ---> {1} \n\n".format(ref_base, new_base))
				
				x = random.random() * (1 - alpha*(1 / len(line)))
				var_num += 1
				num_of_SNPs += 1
		
	else:
		temp = line
		
		
	counter += 1

countfile.write("Total number of SNPs: {0}\n".format(num_of_SNPs))
countfile.write("Total gene count: {0}\n".format(total_gene_count))
countfile.write("Max depth: {0}\n".format(depth))

ecoli = open("../ecoli.fasta", 'r')
salm = open("../salmonella.fasta", 'r')

lines = ecoli.readlines()
counter = 1
outfile.write(lines[0])
for i in range(2):
	for base in lines[1]:
		if not counter % 1000:
			outfile.write("\n")
			outfile.write(lines[0])
			outfile.write(base)
		else:
			outfile.write(base)
	
		counter += 1

del lines[:]

lines = salm.readlines()
counter = 1
outfile.write(lines[0])
for i in range(2):
	for base in lines[1]:
        	if not counter % 1550:
                	outfile.write("\n")
                	outfile.write(lines[0])
                	outfile.write(base)
        	else:
        	        outfile.write(base)
	
        	counter += 1


ecoli.close()
salm.close()
infile.close()
outfile.close()
outfile_copyless.close()
logfile.close()
copyfile.close()
countfile.close()

#
