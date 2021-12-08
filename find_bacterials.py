import os
import sys
import csv

arguments=sys.argv
taxonomic_input_1=sys.argv[1]
taxonomic_input_2=sys.argv[2]
Bac=sys.argv[3]
number_of_max_mismatches=int(sys.argv[4])

dict={}
dict['Sm_1']='TACGAAGGGTGCAAGCGTTACTCGGAATTACTGGGCGTAAAGCGTGCGTAGGTGGTCGTTTAAGTCCGTTGTGAAAGCCCTGGGCTCAACCTGGGAACTGCAGTGGATACTGGACGACTAGAGTGTGGTAGAGGGTAGCGGAATTCCTGGTGTAGCAGTGAAATGCGTAGAGAT'
dict['Sm_2']='CCTGTTTGCTCCCCACGCTTTCGTGCCTCAGTGTCAGTGTTGGTCCAGGTAGCTGCCTTCGCCATGGATGTTCCTCCTGATCTCTACGCATTTCACTGCTACACCAGGAATTCCGCTACCCTCTACCACACTCTAGTCGTCCAGTATCCACTGCAGTTCCCAGGTTGAGCCC'

dict['Pa_1']='TACGAAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTCAGCAAGTTGGATGTGAAATCCCCGGGCTCAACCTGGGAACTGCATCCAAAACTACTGAGCTAGAGTACGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATA'
dict['Pa_2']='CCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCGTACTCTAGCTCAGTAGTTTTGGATGCAGTTCCCAGGTTGAGCCC'

dict['Bc_1']='TACGTAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGTGCGCAGGCGGTTTGCTAAGACCGATGTGAAATCCCCGGGCTCAACCTGGGAACTGCATTGGTGACTGGCAGGCTAGAGTATGGCAGAGGGGGGTAGAATTCCACGTGTAGCAGTGAAATGCGTAGAGA'
dict['Bc_2']='CCTGTTTGCTCCCCACGCTTTCGTGCATGAGCGTCAGTATTGGCCCAGGGGGCTGCCTTCGCCATCGGTATTCCTCCACATCTCTACGCATTTCACTGCTACACGTGGAATTCTACCCCCCTCTGCCATACTCTAGCCTGCCAGTCACCAATGCAGTTCCCAGGTTGAGCCC'

dict['Lf_1']='TACGTAGGTGGCAAGCGTTATCCGGATTTATTGGGCGTAAAGAGAGTGCAGGCGGTTTTCTAAGTCTGATGTGAAAGCCTTCGGCTTAACCGGAGAAGTGCATCGGAAACTGGATAACTTGAGTGCAGAAGAGGGTAGTGGAACTCCATGTGTAGCGGTGGAATGCGTAGATA'
dict['Lf_2']='CCTGTTCGCTACCCATGCTTTCGAGTCTCAGCGTCAGTTGCAGACCAGGTAGCCGCCTTCGCCACTGGTGTTCTTCCATATATCTACGCATTCCACCGCTACACATGGAGTTCCACTACCCTCTTCTGCACTCAAGTTATCCAGTTTCCGATGCACTTCTCCGGTTAAGCCG'

dict['Human_1'] = 'TTCCAGCTCCAATAGCGTATATTAAAGTTGCTGCAGTTAAAAAGCTCGTAGTTGGATCTTGGGAGCGGGCGGGCGGTCCGCCGCGAGGCGAGCCACCGCCCGTCCCCGCCCCTTGCCTCTCGGCGCCCCCTCGATGCTCTTAGCTGAGTGTCCCGCGGGGCCCGAAGCGTTTACTTTGAAAAAATTAGAGTG'
dict['Human_2'] = 'CGTCTTCGAACCTCCGACTTTCGTTCTTGATTAATGAAAACATTCTTGGCAAATGCTTTCGCTCTGGTCCGTCTTGCGCCGGTCCAAGAATTTCACCTCTAGCGGCGCAATACGAATGCCCCCGGCCGTCCCTCTTAATCATGGCCTCAGTTCCGAAAACCAACAAAATAGAACCGCGGTCCTATTCCATTA'

Bac_1=Bac+'_1'
Bac_2=Bac+'_2'

def mismatches (seq1,seq2):
    count = sum(1 for a, b in zip(seq1, seq2) if a != b)
    return count

def procent_bacteria(taxonomic_input_1,taxonomic_input_2,Bac_1,Bac_2,number_of_max_mismatches):
    print(Bac_1,Bac_2)
    number_of_good_reads = 0
    number_of_bed_reads = 0
    number_of_good_reads_1=0
    number_of_good_reads_2=0

    with open(taxonomic_input_1) as f1, open(taxonomic_input_2) as f2:
        content1 = f1.readlines()
        content2 = f2.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content1 = [x.strip() for x in content1]
    content2 = [x.strip() for x in content2]
    number_of_reads_filtering=int(len(content1)/4)
    print(number_of_reads_filtering, ' reads total')
    #print(title,'\n')

    for i in range (0, number_of_reads_filtering):

        current_read1=content1[i*4:i*4+4]
        current_read2=content2[i*4:i*4+4]
        #print(i,current_read1,'\n\n', current_read2)
        current_primer1=current_read1[1][27:27+len(Bac_1)]
        current_primer2=current_read2[1][28:28+len(Bac_2)]
        #print(i,current_primer1, current_primer2)
        #print((primer_mism_1(current_primer1)),(primer_mism_2(current_primer2)))
        if (mismatches(Bac_1,current_primer1)<=number_of_max_mismatches) and (mismatches(Bac_2,current_primer2) <=number_of_max_mismatches):
            number_of_good_reads+=1
            #f_out_1 = open(filtr_output_1, 'a')
            #for item1 in current_read1:
            #    f_out_1.write(item1+'\n')
            #f_out_1.close()
            #f_out_2 = open(filtr_output_2, 'a')
            #for item2 in current_read2:
            #    f_out_2.write(item2+'\n')
            #f_out_2.close()
        else:
            number_of_bed_reads+=1
        if (mismatches(Bac_1,current_primer1) <=number_of_max_mismatches): number_of_good_reads_1+=1
        if (mismatches(Bac_2,current_primer2) <=number_of_max_mismatches): number_of_good_reads_2+=1
        #for item in current_read:
        #    print(item)
    #print(number_of_good_reads,number_of_bed_reads,'\n')
    print(Bac)
    print('max permitted number of mismatches',number_of_max_mismatches)
    print(100*number_of_good_reads_1/number_of_reads_filtering,'% good first reads')
    print(100*number_of_good_reads_2/number_of_reads_filtering,'% good second reads')
    if number_of_bed_reads!=0:
        print(number_of_good_reads*100/(number_of_good_reads+number_of_bed_reads),'% total reads good\n')
    else:
        print('100% good\n')

procent_bacteria(taxonomic_input_1,taxonomic_input_2,dict[Bac_1],dict[Bac_2],number_of_max_mismatches)
