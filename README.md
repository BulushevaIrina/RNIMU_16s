# 16s

# Описание версий

v.0 Ниже приведено описание для базовой версии и всех составляющих, где по-очереди запускались все скрипты.

В v.1 версии whole_pipe запуск осуществляется сразу всего пайплайна, объединяющего скрипты v.0, для одного образца. Подробнее - в README_16s_pipe.md https://github.com/genomecenter/16s/blob/master/whole_pipe/README_16s_pipe.md

В v.2 версии добавлена фильтрация по длине и сохранение результатов в более удобном формате https://github.com/genomecenter/16s/releases/tag/TaxonList_V.2

# SCRIPT downsampling_filtration_with_umi_option.py with UMI option (UMI = 8 nucl)
output will be in the folder with input file, output txt file with results - in your current folder
you can run command as written below for all samples and take statistics about all samples in output_file.txt file
crashes in case number of reads are smaller then needed for downsampling option

input info:
python downsampling_filtration.py [first read] [second read] [number of downsapling reads] [number of max primer mismatches] [output txt file] [umi_yes/umi_no]

python downsampling_filtration.py v300056283_run32_L04_127_1.fq.gz v300056283_run32_L04_127_2.fq.gz 100000 3 output_file.txt umi_yes

# SCRIPT downsampling_filtration_with_umi_and_primer_option.py with UMI and primer option (UMI = 8 nucl)
output will be in the folder with input file, output txt file with results - in your current folder
you can run command as written below for all samples and take statistics about all samples in output_file.txt file
in case number of reads are smaller then needed for downsampling option [number of downsapling reads] - run without downsampling

input info:
python downsampling_filtration.py [first read] [second read] [number of downsapling reads] [number of max primer mismatches] [output txt file] [umi_yes/umi_no] [primer 1] [primer 2]

python downsampling_filtration.py v300056283_run32_L04_127_1.fq.gz v300056283_run32_L04_127_2.fq.gz 100000 3 output_file.txt umi_yes TGTGCATTCGTCTTTTCCAGAGC ACACCTCCTTTGCAGCCACAA


# SCRIPT downsampling_filtration.py (UMI = 8 nucl)
output will be in the folder with input file, output txt file with results - in your current folder
you can run command as written below for all samples and take statistics about all samples in output_file.txt file

input info:
python downsampling_filtration.py [first read] [second read] [number of downsapling reads] [number of max primer mismatches] [output txt file]

python downsampling_filtration.py v300056283_run32_L04_127_1.fq.gz v300056283_run32_L04_127_2.fq.gz 100000 3 output_file.txt

# SCRIPT qiime2.py
скрипт, который обсчитывает образец в qiime2, переводит результат по фичам в текстовый вид и создает таблицу с информацией (feature name, frequency, length, procent of total frequency, blast top 3 results, sequence). Предпоследний столбец в этой версии пустой.
использует файл code_qiime.sh (проверить путь в qiime2.sh)

python qiime2.py [first read] [second read] [output folder] [custom name of sample]
python qiime2.py v300009398_run36_2_L04_125_1_100000_reads_filtered.fq v300009398_run36_2_L04_125_2_100000_reads_filtered.fq 36_run_qiime2 125

В скрипте code_qiime.sh (который вызывается в qiime2.py) по умолчанию стоит обработка с umi. Если же umi отсутствует - надо поменять строки
     --p-trim-left-f 27 \
     --p-trim-left-r 28 \
на строки
     --p-trim-left-f 19 \
     --p-trim-left-r 20 \

# SCRIPT taxonomy_family_genus_from_feature_table.py

script takes family and genus info from file like feature_info_blast_64_just_conc_FALSE.csv and make table with such info:
|family|	% confidence family |	genus |	% confidence genus |	% total |	all taxonomy path	|feature seq|

before calling it user should: 
1) go to http://rdp.cme.msu.edu/classifier/classifier.jsp
2) select fasta file with features and sequences (generated from qiime2.py script)
3) submit
4) go to [show assignment detail for Root only ]
5) select ''download allrank/fixrank(no matter what) result'
6) open downloaded file, copy taxonomy info and paste it in column 'taxonomy' of  file like feature_info_blast_64_just_conc_FALSE.csv

пример запуска:
python taxonomy_family_genus_from_feature_table.py feature_info_blast_64_just_conc_FALSE.csv taxonomy_64_just_conc_FALSE.csv 0.5

python taxonomy_family_genus_from_feature_table.py [features table path] [output file path] [treshhold % total]



# SCRIPT qiime2_SE.py
аналогичный скрипт для одноконцевого чтения
пример запуска:
python qiime2_SE.py v300009398_run36_2_L04_125_1_100000_reads_filtered.fq 36_run_SE_qiime2 125_SE
использует файл code_qiime_SE.sh

# SCRIPT find_bacterials.py
поиск конкретных бактерий в образце с заданным числом мисматчей. Словарь дополняется вручную в самом скрипте
примеры запуска:
python find_bacterials.py v300056283_run32_L04_125_1_100000_reads.fq v300056283_run32_L04_125_2_100000_reads.fq Sm 6

python find_bacterials.py v300009398_run36_2_L04_128_1_100000_reads_filtered.fq v300009398_run36_2_L04_128_2_100000_reads_filtered.fq Lf 15


# EXAMPLE from raw data to result tables
Если сшивание с N, то в файле  
/home/irinab/miniconda3/pkgs/q2-dada2-2020.2.0-py36_0/bin/run_dada_paired.R
в строке 
mergers[[j]] <- mergePairs(ddF, drpF, ddR, drpR, justConcatenate=TRUE)
должно стоять TRUE.
Если же используем сшивание с перекрытием - FALSE

Даунсемплинг и фильтрация по праймерам:
python /home/irinab/Desktop/16s/scripts/downsampling_filtration_with_umi_option.py /home/irinab/Desktop/16s/42_run_59_64_good/v300083131_run42_L01_64_1.fq.gz /home/irinab/Desktop/16s/42_run_59_64_good/v300083131_run42_L01_64_2.fq.gz 100000 3 downs_filtr_output_42_run_59_and_64.txt umi_no

QIIME:
В скрипте code_qiime.sh (который вызывается в qiime2.py) по умолчанию стоит обработка с umi. Если же umi отсутствует - надо поменять строки
     --p-trim-left-f 27 \
     --p-trim-left-r 28 \
на строки
     --p-trim-left-f 19 \
     --p-trim-left-r 20 \
затем
python /home/irinab/Desktop/16s/scripts/qiime2.py /home/irinab/Desktop/16s/42_run_59_64_good/v300083131_run42_L01_64_1_100000_reads_filtered.fq /home/irinab/Desktop/16s/42_run_59_64_good/v300083131_run42_L01_64_2_100000_reads_filtered.fq /home/irinab/Desktop/16s/42_run_59_64_good/42_run_dada2_just_conc_FALSE 64_just_conc_FALSE

Определение таксономии:
1) go to http://rdp.cme.msu.edu/classifier/classifier.jsp
2) select fasta file with features and sequences (generated from qiime2.py script)
3) submit
4) go to [show assignment detail for Root only ]
5) select ''download allrank/fixrank(no matter what) result'
6) open downloaded file, copy taxonomy info and paste it in column 'taxonomy' of  file feature_info_blast_64_just_conc_FALSE.csv

Построение итоговой таблицы:
python taxonomy_family_genus_from_feature_table.py feature_info_blast_64_just_conc_FALSE.csv taxonomy_64_just_conc_FALSE.csv 0.5

#Если есть необходимость альтернативы RDP и определения до вида, то fasta-файл с фичами можно скормить бласту.
пример команды бласта ниже. Опция -remote позволяет считать на удаленном сервере ncbi, а не локально.

blastn -task megablast -db rRNA_typestrains/16S_ribosomal_RNA -query feature_sequense_64_just_conc_FALSE_first4.fasta -out outputfile7_6.csv -outfmt "6 qaccver sscinames sblastnames ppos evalue bitscore score staxid" -max_target_seqs 4 -remote

На выходе получится csv-таблица с топ 4 хитами по каждой фиче со следующими полями:
qaccver (название фичи), 
sscinames (название хита по бласту), 
sblastnames (тоже название по бласту), 
ppos (процент совпадения), 
evalue, 
bitscore, 
score, 
staxid (какой-то уникальный номер хита)

Описание команд см выше в описании каждого скрипта


