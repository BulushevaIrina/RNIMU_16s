import os
import sys
import downsampling_filtration_function
import qiime2_function
import taxonomy_build_whole_table_function
import xlwt
from xlwt import Workbook
#import pathlib

arguments=sys.argv
input1=sys.argv[1] #first read
input2=sys.argv[2] #second read
number_of_reads=int(sys.argv[3]) #number of downsapling reads
number_of_max_mismatches=int(sys.argv[4]) #number of max primer mismatches
umi_or_not=sys.argv[5] #umi_yes/umi_no
pr1=sys.argv[6] #primer 1
pr2=sys.argv[7] #primer 2
folder_for_output=sys.argv[8] # where all results exept downsampling-filtration will be
barcode=sys.argv[9] #name of sample, run etc, ex run_42_barcode_59

#downsampling_filtration_with_umi_and_primer_option
if not os.path.exists(folder_for_output):
    os.makedirs(folder_for_output)
out_file=folder_for_output+'/filtr_output_'+str(barcode)+'.txt'
filtr_output_1, filtr_output_2 = downsampling_filtration_function.downsampling_filtration(input1, input2, number_of_reads, number_of_max_mismatches, out_file, umi_or_not, pr1, pr2)
os.system('conda activate qiime2-2020.2')
print(filtr_output_1)
print(filtr_output_2)
print('rdp_classifier -o '+ folder_for_output+'/RDP_features_'+barcode+'.tsv -q '+folder_for_output+'/feature_sequense_' +barcode+'.fasta')
qiime2_function.qiime2_function(filtr_output_1, filtr_output_2, folder_for_output, barcode, umi_or_not)
print('qiime2 done')
print('RDP start')
os.system('rdp_classifier -o '+ folder_for_output+'/RDP_features_'+barcode+'.tsv -q '+folder_for_output+'/feature_sequense_' +barcode+'.fasta')

print('RDP done')
os.system('cp /home/irinab/Desktop/16s/blast_taxdb/taxdb.btd '+str(os.path.abspath(os.getcwd())))
os.system('cp /home/irinab/Desktop/16s/blast_taxdb/taxdb.bti '+str(os.path.abspath(os.getcwd())))
print('blast start')
os.system('blastn -task megablast -db rRNA_typestrains/16S_ribosomal_RNA -query '+folder_for_output+'/feature_sequense_' +barcode+'.fasta -out '+ folder_for_output+'/blast_features_'+barcode+'.tsv -outfmt "6 qaccver sscinames sblastnames ppos evalue bitscore score staxid" -max_target_seqs 4 -remote')
print('blast done')
#os.system('rm '+str(os.path.abspath(os.getcwd()))+'/taxdb.btd')
#os.system('rm '+str(os.path.abspath(os.getcwd()))+'/taxdb.bti')

qiime_result=folder_for_output+'/feature_info_'+str(barcode)+'.csv'
blast_result=folder_for_output+'/blast_features_'+barcode+'.tsv'
RDP_result=folder_for_output+'/RDP_features_'+barcode+'.tsv'
output_file_table=folder_for_output+'/taxonomy_result_table_'+barcode
taxonomy_build_whole_table_function.make_table(qiime_result,blast_result,RDP_result,output_file_table)

print('Result table done')
