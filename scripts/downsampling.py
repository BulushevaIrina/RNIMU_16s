#https://stackoverflow.com/questions/5832856/how-to-read-file-n-lines-at-a-time-in-python
filename='small_file.fastq'
N=4
from itertools import islice
with open(filename, 'r') as infile:
    lines_gen = islice(infile, N)
    for line in lines_gen:
        print (line)
