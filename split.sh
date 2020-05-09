#!/bin/bash

declare -i t
declare -i x
lines=($(wc -l $1))
t=${lines[0]}/4
split -l $t pair.fasta temp_
