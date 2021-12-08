import sys
#import csv
import xlsxwriter

qiime_result = sys.argv[1]
blast_result = sys.argv[2]
RDP_result = sys.argv[3]
output_file = sys.argv[4]
#treshhold = float(sys.argv[5])


def make_table(qiime_result,blast_result,RDP_result,output_file):
    with open(qiime_result) as f1:
        qiimefile = f1.readlines()
    qiimefile = [x.strip() for x in qiimefile]

    with open(blast_result) as f2:
        blastfile = f2.readlines()
    blastfile = [x.strip() for x in blastfile]

    with open(RDP_result) as f3:
        RDPfile = f3.readlines()
    RDPfile = [x.strip() for x in RDPfile]


    # Workbook is created
    wb = xlsxwriter.Workbook(output_file+'.xlsx')

    # add_sheet 
    sheet1 = wb.add_worksheet('taxonomy')

    #row column both from 0
    sheet1.write(0, 0, 'feature name')
    sheet1.write(0, 1, '% total')
    sheet1.write(0, 9, 'feature length')
    sheet1.write(0, 10, 'feature sequence')
    feature_array=[]
    for i in range(1,len(qiimefile)):
        current_feature = qiimefile[i].split(',')
        sheet1.write(i*4-3, 0, current_feature[0])
        sheet1.write(i*4-3, 1, float(current_feature[3]))
        sheet1.write(i*4-3, 9, current_feature[2])
        sheet1.write(i*4-3, 10, current_feature[5])
        feature_array.append(current_feature[0])

    sheet1.write(0, 2, 'family')
    sheet1.write(0, 3, '% confidence family')
    sheet1.write(0, 4, 'genus')
    sheet1.write(0, 5, '% confidence genus')
    sheet1.write(0, 8, 'RDP whole path')

    for i in range(0,len(RDPfile)):
        current_feature = RDPfile[i].split('\t')
        #print(current_feature[0],feature_array[i],current_feature[0] == feature_array[i])
        #if current_feature[0] == feature_array[i]:
        if current_feature[0] in feature_array:
            index_RDP=feature_array.index(current_feature[0])
            if 'family' in current_feature:
                fam_index=current_feature.index('family')
                sheet1.write(index_RDP*4+1, 2, current_feature[fam_index-1])
                sheet1.write(index_RDP*4+1, 3, 100*float(current_feature[fam_index+1]))
            else:
                sheet1.write(index_RDP*4+1, 2, '-')
                sheet1.write(index_RDP*4+1, 3, '-')
            if 'genus' in current_feature:
                genus_index=current_feature.index('genus')
                sheet1.write(index_RDP*4+1, 4, current_feature[genus_index-1])
                sheet1.write(index_RDP*4+1, 5, 100*float(current_feature[genus_index+1]))
            else:
                sheet1.write(index_RDP*4+1, 4, '-')
                sheet1.write(index_RDP*4+1, 5, '-')
            sheet1.write(index_RDP*4+1, 8, RDPfile[i])

    sheet1.write(0, 6, 'blast top 4 hits')
    sheet1.write(0, 7, '% blast identity')
    for i in range(0,int(len(blastfile)/4)):
        current_feature1 = blastfile[i*4].split('\t')
        current_feature2 = blastfile[i*4+1].split('\t')
        current_feature3 = blastfile[i*4+2].split('\t')
        current_feature4 = blastfile[i*4+3].split('\t')
        feature_index = (feature_array.index(current_feature1[0]))*4+1
        sheet1.write(feature_index, 6, current_feature1[1])
        sheet1.write(feature_index, 7, current_feature1[3])
        sheet1.write(feature_index+1, 6, current_feature2[1])
        sheet1.write(feature_index+1, 7, current_feature2[3])
        sheet1.write(feature_index+2, 6, current_feature3[1])
        sheet1.write(feature_index+2, 7, current_feature3[3])
        sheet1.write(feature_index+3, 6, current_feature4[1])
        sheet1.write(feature_index+3, 7, current_feature4[3])
    wb.close()

make_table(qiime_result,blast_result,RDP_result,output_file)
