import sys
import csv

input_for_tree = sys.argv[1]
output_for_tree = sys.argv[2]
treshhold = float(sys.argv[3])


with open(input_for_tree) as f1:
    content_for_tree = f1.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
content_for_tree = [x.strip() for x in content_for_tree]

with open(output_for_tree, 'w', newline='\n') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['family', '% confidence family', 'genus', '% confidence genus', '% total', 'all taxonomy path', 'feature seq'])

    for i in range (1,len(content_for_tree)):
        feature_array=content_for_tree[i].split(',')
        if float(feature_array[3])>=treshhold:

            writer.writerow([feature_array[4].split(';')[-4], feature_array[4].split(';')[-3], feature_array[4].split(';')[-2], feature_array[4].split(';')[-1], feature_array[3], feature_array[4], feature_array[5]])# round(float(feature_array[3]), 2))


##for txt output_file
#output_file = open(output_for_tree,'w')
#output_file.write('family' + '\t' + '% confidence family' + '\t' + 'genus' + '\t' + '% confidence genus' + '\t' + '% total' + '\t' + 'feature seq' + '\n')
#for i in range (1,len(content_for_tree)):
#    feature_array=content_for_tree[i].split(',')
#    if float(feature_array[3])>=treshhold:
#        output_file.write(feature_array[4].split(';')[-4] + '\t' + feature_array[4].split(';')[-3] + '\t' + feature_array[4].split(';')[-2] + '\t' + feature_array[4].split(';')[-1] + '\t' + feature_array[3]  + '\t' + feature_array[5] + '\n' )# round(float(feature_array[3]), 2))
#output_file.close()
