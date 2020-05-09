#!/usr/bin/env python

#PYTHON 3
from __future__ import division
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys


def find_best_match(q_lines):
    best_match = 0
    for i in q_lines:
        if int(i[0]) > best_match:
            best_match = int(i[0])
            best = i
    return best


with open(sys.argv[1], 'r') as blat:
    ratio = []
     
    is_first= True 
    q_lines = []
    overall = []
    for line in blat:
        df = line.split('\t')
        q = df[9].split('.')[0]
        
        if is_first:
            q_prev = q
            q_lines.append(df)
            is_first = False
        elif q == q_prev:
            q_lines.append(df)
        else:
            best = find_best_match(q_lines)
            if int(best[10]) > int(best[14]):
                ratio.append([int(best[14]),int(best[14])])
            else:
                ratio.append([int(best[10]),int(best[14])])
            del q_lines[:]
            q_lines.append(df)

        q_prev = q
        if int(df[10]) > int(df[14]):
            overall.append([int(df[14]),int(df[14])])
        else:
            overall.append([int(df[10]),int(df[14])])

best_ratios = [(x[0]/x[1]) for x in ratio]
overall_ratios = [(x[0]/x[1]) for x in overall]

b_ratios = np.array(best_ratios)
o_ratios = np.array(overall_ratios)

# Statistics.txt displays a summary of query matches
outfile = open("statistics.txt",'w')

outfile.write("********************\n")
outfile.write("BEST MATCHES ONLY:\n********************\n")
outfile.write("\tMean query length: " + str(sum(x[0] for x in ratio)/len(ratio)) + "\n")
outfile.write("\tMean reference length: " + str(sum(x[1] for x in ratio)/len(ratio)) + "\n")
outfile.write("\tMean %: " + str(np.mean(b_ratios)) + "\n")
outfile.write("\tStandard deviation: " + str(np.std(b_ratios)) + "\n")
outfile.write("\tMinimum: " + str(min(best_ratios)) + "\n")
outfile.write("\tMaximum: " + str(max(best_ratios)) + "\n\n")

outfile.write("********************\n")
outfile.write("OVERALL:\n********************\n")
outfile.write("\tMean query length: " + str(sum(x[0] for x in overall)/len(overall)) + "\n")
outfile.write("\tMean reference length: " + str(sum(x[1] for x in overall)/len(overall)) + "\n")
outfile.write("\tMean %: " + str(np.mean(o_ratios)) + "\n")
outfile.write("\tStandard deviation: " + str(np.std(o_ratios)) + "\n")
outfile.write("\tMinimum: " + str(min(overall_ratios)) + "\n")
outfile.write("\tMaximum: " + str(max(overall_ratios)) + "\n\n")

outfile.close()

plt.figure(figsize=(12, 9))
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.ylim(0,180)
plt.xticks(fontsize=16)
plt.yticks(range(20,200,20), fontsize=16)
plt.hist(best_ratios, bins=70, color="#3F5D7D")
plt.title('Best Matches Only', fontsize=24)
plt.ylabel('Frequency', fontsize=16)
plt.xlabel('Ratio of Query Size to Gene Size', fontsize=16)
plt.savefig('figure_bests.png',bbox_inches='tight')
plt.close()

plt.figure(figsize=(12, 9))
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.xticks(fontsize=16)
plt.ylim(0,2000000)
plt.yticks(range(500000,2000001,500000), fontsize=16)
plt.hist(overall_ratios, bins=70, color="#3F5D7D")
plt.title('All Queries', fontsize=24)
plt.ylabel('Frequency', fontsize=16)
plt.xlabel('Ratio of Query Size to Gene Size', fontsize=16)
plt.savefig('figure_overall.png',bbox_inches='tight')
plt.close()


blat.close()


















