import os
import sys
#!{sys.executable} -m pip install Bio
from Bio import SeqIO
#see options on site https://biopython.org/docs/1.75/api/Bio.SeqIO.QualityIO.html

arguments = sys.argv
input_file = sys.argv[1] # input file name
output_folder = sys.argv[2] # output folder
output_file_name=sys.argv[3] # output file name

os.system('mkdir '+output_folder)

nucles_from_start=int(20)
nucles_from_end=int(50)

for record in SeqIO.parse(input_file, "fastq"):
    #print(record.name,record.seq,sep='\n')
    read_array=record.format("fastq").split('\n')
    #for item in read_array:
    #    print(item)

    output_file = open(output_folder+output_file_name, 'w+')
    output_file.write(read_array[0]+'\n')
    output_file.write(read_array[1][nucles_from_start-1:nucles_from_end]+'\n')
    output_file.write(read_array[2]+'\n')
    output_file.write(read_array[3][nucles_from_start-1:nucles_from_end]+'\n')
    #read_name = read_array[0]
    #read_seq = read_array[1]
    #read_orient = read_array[2]
    #read_phred = read_array[3]
    output_file.close()
