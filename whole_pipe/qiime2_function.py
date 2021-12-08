import os
import sys
import csv

def qiime2_function(input1, input2, folder_for_output, barcode, umi_or_not):

    os.system('mkdir '+folder_for_output)
    os.system('cd '+folder_for_output)

    #make manifest files
    manifest_file = open('manifest'+str(barcode)+'.txt', 'w+')
    manifest_file.write('# paired-end fastq manifest file\n')
    manifest_file.write('sample-id,absolute-filepath,direction\n')
    manifest_file.write('sample-1,' + input1 + ',forward\n')
    manifest_file.write('sample-1,' + input2 + ',reverse\n')
    manifest_file.close()
    #print ('manifest file have had made')
    #os.system('conda init bash')
    os.system('conda activate qiime2-2020.2')
    os.system('cd ..')

    if umi_or_not=='umi_no':
        os.system('bash /home/irinab/Desktop/16s/scripts/make_whole_pipe_parallel/code_qiime_umi_startend.sh 19 20 '+str(barcode))
    elif umi_or_not=='umi_yes':
        os.system('bash /home/irinab/Desktop/16s/scripts/make_whole_pipe_parallel/code_qiime_umi_startend.sh 27 28 '+str(barcode))

    os.system('cp UM-exp'+str(barcode)+'.qzv '+folder_for_output+'/feature_frequency_'+str(barcode)+'.qzv')
    os.system('cp UMrep-seqsO'+str(barcode)+'.qzv '+folder_for_output+'/feature_sequense_and_len_'+str(barcode)+'.qzv')
    os.system('cp feature_frequency'+str(barcode)+'/feature-frequency-detail.csv '+folder_for_output+'/feature-frequency_'+str(barcode)+'.csv')
    os.system('cp feature_sequences'+str(barcode)+'/sequences.fasta '+folder_for_output+'/feature_sequense_'+str(barcode)+'.fasta')

    os.system('rm UMdenoising-stats'+str(barcode)+'.qza')
    os.system('rm UM-exp'+str(barcode)+'.qzv')
    os.system('rm UMrep-seqs-dada2O'+str(barcode)+'.qza')
    os.system('rm UMrep-seqsO'+str(barcode)+'.qzv')
    os.system('rm UMtable-dada2O'+str(barcode)+'.qza')
    os.system('rm -r feature_frequency'+str(barcode))
    os.system('rm -r feature_sequences'+str(barcode))
    os.system('rm manifest'+str(barcode)+'.txt')
    os.system('rm UMtutorial-demux-paired-end'+str(barcode)+'.qzv')
    os.system('rm UMtutorial-demux-paired-end'+str(barcode)+'.qza')
    ###make feature whole table
    frequency_csv = folder_for_output+'/feature-frequency_'+str(barcode)+'.csv'
    sequence_fasta = folder_for_output+'/feature_sequense_'+str(barcode)+'.fasta'
    output_csv = folder_for_output+'/feature_info_'+str(barcode)+'.csv'

    #path='/home/irinab/Desktop/16s/36_run/36_run_125/'

    with open(frequency_csv) as f1, open(sequence_fasta) as f2:
        content_frequency = f1.readlines()
        content_sequence = f2.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content_frequency = [x.strip() for x in content_frequency]
    content_sequence = [x.strip() for x in content_sequence]

    col1_feature_name=[]
    col2_frequency=[]
    col6_sequence=[]
    col3_length=[]
    col5_blast=[]
    for i in range(0,len(content_frequency)):
        col1_feature_name.append(content_frequency[i].split(',')[0])
        col2_frequency.append(int(content_frequency[i].split(',')[1].split('.')[0]))
        col6_sequence.append(content_sequence[content_sequence.index('>'+str(col1_feature_name[i]))+1])
        col3_length.append(len(col6_sequence[i]))
        #print('start blast '+str(i))
        #os.system('echo ">d\n'+col6_sequence[i]+'" > '+path+'fasta.fa')
        #os.system('blastn -db nt -query '+path+'fasta.fa -out '+path+'align.txt -remote')
        #os.system('grep -n "Sequences producing significant alignments:" '+path+'align.txt | cut -d : -f 1 | xargs -I{} awk "NR >= {}+2 && NR <= {}+11" ' +path+'align.txt > '+path+'aligncut.txt')
        #with open(path+'aligncut.txt', 'r') as file:
         #   col5_blast.append(file.read().replace('\n', ''))
          #  print(col5_blast[i])
    total_frequency=sum(col2_frequency)

    with open(output_csv, 'w', newline='\n') as file_output:
        writer = csv.writer(file_output)
        writer.writerow(["feature name", "frequency", "length","procent of total frequency","taxonomy","sequence"])
        for i in range(0,len(content_frequency)):
            writer.writerow([col1_feature_name[i], col2_frequency[i], col3_length[i],col2_frequency[i]*100/total_frequency,'',col6_sequence[i]])#col5_blast[i],col6_sequence[i]])

    print('done')
