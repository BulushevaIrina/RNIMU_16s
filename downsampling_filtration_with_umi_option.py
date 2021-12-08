import os
import sys
from itertools import islice


arguments=sys.argv
input1=sys.argv[1]
input2=sys.argv[2]
number_of_reads=int(sys.argv[3])
number_of_max_mismatches=int(sys.argv[4])
out_file=sys.argv[5]
umi_or_not=sys.argv[6]

#input1 = '/home/irinab/Desktop/16s/downsampling/127_0,2ng/v300056283_run32_L04_127_1.fq.gz'
#input2 = '/home/irinab/Desktop/16s/downsampling/127_0,2ng/v300056283_run32_L04_127_2.fq.gz'
#number_of_reads=100000
#number_of_max_mismatches=3

umi_len=0

if umi_or_not=="umi_yes":
    umi_len=8

#Make downsampling
print('\nstart making downsampling')
output1=input1[:-6]+'_'+str(number_of_reads)+'_reads.fq'
output2=input2[:-6]+'_'+str(number_of_reads)+'_reads.fq'
#print(str('\n\nseqtk sample -s100 ' + input1 + ' ' + str(number_of_reads) + ' > ' + output1+'\n\n'))
os.system(str('seqtk sample -s100 ' + input1 + ' ' + str(number_of_reads) + ' > ' + output1))
print('finish making downsampling 1 read')
os.system(str('seqtk sample -s100 ' + input2 + ' ' + str(number_of_reads) + ' > ' + output2))
print('finish making downsampling both reads')

#PRIMER FILTRATION
print('\nstart filtration')
#find primer 1
def primer_mism_1(read1):
    #print(len(read1))
    pr1='GTGYCAGCMGCCGCGGTAA'
    mism=-2
    for i in range (0,19):
        if read1[i]!=pr1[i]:
            mism+=1
    #print(mism)
    if not (read1[3]=='T' or read1[3]=='C'):
        mism+=1
    if not (read1[8]=='A' or read1[3]=='C'):
        mism+=1
    #print(read1,mism)
    return mism
        #print (i)

#find primer 2
def primer_mism_2(read2):
    pr2='GGACTACNVGGGTWTCTAAT'
    mism=-3
    for i in range (0,20):
        if read2[i]!=pr2[i]:
            mism+=1
    #print(mism)
    if read2[8]=='T':
        mism+=1
    if not (read2[13]=='A' or read2[13]=='T'):
        mism+=1
    #print(read1,mism)
    return mism
        #print (i)

filtr_input_1 = output1#'/home/irinab/Desktop/16s/downsampling/125_5ng/v300056283_run32_L04_125_1_250_reads.fq'#
filtr_input_2 = output2#'/home/irinab/Desktop/16s/downsampling/125_5ng/v300056283_run32_L04_125_2_250_reads.fq'#

filtr_output_1 = filtr_input_1[:-3]+'_filtered.fq'
filtr_output_2 = filtr_input_2[:-3]+'_filtered.fq'

number_of_good_reads = 0
number_of_bed_reads = 0
number_of_good_reads_1=0
number_of_good_reads_2=0

#number_of_reads_filtering=number_of_reads
#number_of_max_mismatches=3

with open(filtr_input_1) as f1, open(filtr_input_2) as f2:
    content1 = f1.readlines()
    content2 = f2.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content1 = [x.strip() for x in content1]
content2 = [x.strip() for x in content2]

print('primers GTGYCAGCMGCCGCGGTAA  GGACTACNVGGGTWTCTAAT\n')

for i in range (0, number_of_reads):

    current_read1=content1[i*4:i*4+4]
    current_read2=content2[i*4:i*4+4]
    #print(i,current_read1,'\n\n', current_read2)
    current_primer1=current_read1[1][umi_len:19 + umi_len]
    current_primer2=current_read2[1][umi_len:20 + umi_len]
    #print(i,current_primer1, current_primer2)
    #print((primer_mism_1(current_primer1)),(primer_mism_2(current_primer2)))
    if (primer_mism_1(current_primer1)<=number_of_max_mismatches) and (primer_mism_2(current_primer2) <=number_of_max_mismatches):
        number_of_good_reads+=1
        f_out_1 = open(filtr_output_1, 'a')
        for item1 in current_read1:
            f_out_1.write(item1+'\n')
        f_out_1.close()
        f_out_2 = open(filtr_output_2, 'a')
        for item2 in current_read2:
            f_out_2.write(item2+'\n')
        f_out_2.close()
    else:
        number_of_bed_reads+=1
    if (primer_mism_1(current_primer1)<=number_of_max_mismatches): number_of_good_reads_1+=1
    if (primer_mism_2(current_primer2)<=number_of_max_mismatches): number_of_good_reads_2+=1
    #for item in current_read:
    #    print(item)
print('\nfinish filtration')
print('number of good reads',number_of_good_reads,'\nnumber of bed reads',number_of_bed_reads,'\n')
print('max permitted number of mismatches',number_of_max_mismatches)
print(100*number_of_good_reads_1/number_of_reads,'% good first reads')
print(100*number_of_good_reads_2/number_of_reads,'% good second reads')
if number_of_bed_reads!=0:
    print(number_of_good_reads*100/(number_of_good_reads+number_of_bed_reads),'% total reads good')
else:
    print('100% good')

output_file = open(out_file, 'a')
output_file.write('input files: '+'\n'+str(input1)+'\n'+str(input2)+'\n')
output_file.write('parameters: number of reads - '+str(number_of_reads)+', max permitted number of primer mismatches - '+str(number_of_max_mismatches)+'\n')
output_file.write('primers: GTGYCAGCMGCCGCGGTAA  GGACTACNVGGGTWTCTAAT\n\n')
output_file.write('results:\n')
output_file.write('number of good reads - '+str(number_of_good_reads)+'\nnumber of bed reads - '+str(number_of_bed_reads))
#output_file.write('max permitted number of mismatches '+str(number_of_max_mismatches))
output_file.write('\n'+str(100*number_of_good_reads_1/number_of_reads)+'% good first reads')
output_file.write('\n'+str(100*number_of_good_reads_2/number_of_reads)+'% good second reads')
if number_of_bed_reads!=0:
    output_file.write('\n'+str(number_of_good_reads*100/(number_of_good_reads+number_of_bed_reads))+'% total reads good\n\n\n')
else:
    output_file.write('\n'+'100% good\n\n\n')
