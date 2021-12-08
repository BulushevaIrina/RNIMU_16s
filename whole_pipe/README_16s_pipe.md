# УСТАНОВКА RDP, blast и qiime2

install RDP

https://anaconda.org/bioconda/rdp_classifier

conda install bioconda

conda install -c bioconda rdp_classifier

Также может потребоваться установка дополнительных пакетов для работы в python3:

pip install xlwt 


# ПЕРЕД ЗАПУСКОМ 
Перед запуском скрипта, включающего в себя работу с qiime2, нужно поменять среду работы.
Это производится командой

conda activate qiime2-2020.2

Главный файл 16s_pipeline.py

и остальные файлы, содержащие функции, а именно:

downsampling_filtration_function.py

qiime2_function.py

taxonomy_build_whole_table_function.py

должны находиться в одной папке.

в файле qiime2_function.py в строках 23 и 25 пропишите свой путь к файлу code_qiime_umi_startend.sh, куда его сохранили

Скрипт по созданию таблицы taxonomy_build_whole_table.py приведен на случай, если последняя ступень пайплайна по объединению таблиц из qiime, blast и RDP упадет. Он работает независимо от пайпа и может быть сохранен где угодно (описание команды ниже)

для отображения названий таксономических единиц ступени blast в файле 16s_pipeline.py в 37 и 38 строке нужно прописать путь к файлам taxdb.btd и taxdb.bti. Это файлы доступные для скачивания ftp://ftp.ncbi.nlm.nih.gov/blast/db/taxdb.tar.gz


# Запуск всего пайплайна целиком

Пример команды:

python /home/irinab/Desktop/16s/scripts/make_whole_pipe_parallel/16s_pipeline.py /home/irinab/Desktop/16s/45_run/v300068121_run45_L01_57_1.fq.gz /home/irinab/Desktop/16s/45_run/v300068121_run45_L01_57_2.fq.gz 100000 3 umi_yes GTGYCAGCMGCCGCGGTAA GGACTACNVGGGTWTCTAAT /home/irinab/Desktop/16s/45_run/R45_L01_B57_output R45_L01_B57

Опции команды:

input1=sys.argv[1] #first read

input2=sys.argv[2] #second read

number_of_reads=int(sys.argv[3]) #number of downsapling reads

number_of_max_mismatches=int(sys.argv[4]) #number of max primer mismatches

umi_or_not=sys.argv[5] # наличие или отсутствие UMI в образце (длина 8 букв)

pr1=sys.argv[6] #primer 1 (длина 19)

pr2=sys.argv[7] #primer 2 (длина 20)

folder_for_output=sys.argv[8] # путь и название директории с результатами для образца (создается в пайплайне)

barcode=sys.argv[9] #Уникальное название образца, используется в названиях файлов пайпа. Например, run_42_barcode_59 или R45_L01_B57.


! Пайплайн позволяет единовременно запускать несколько образцов в разных терминалах. Количество зависит от производительности и характеристик вычислительного устройства


По умолчанию на стации сшивания ридов в qiime идет сшивание с перекрытием. Если перекрытия нет, то сшивать надо с N:
Если сшивание с N, то в файле
/home/irinab/miniconda3/pkgs/q2-dada2-2020.2.0-py36_0/bin/run_dada_paired.R в строке mergers[[j]] <- mergePairs(ddF, drpF, ddR, drpR, justConcatenate=TRUE) должно стоять TRUE. Если же используем сшивание с перекрытием - FALSE

# Что на выходе?

Для образца создается папка с файлами с результатами.
Пусть уникальное название образца было "R45_L01_B121", тогда файлы и их наазначение следующие:


filtr_output_R45_L01_B121.txt - информация по фильтрации

feature_sequense_and_len_R45_L01_B121.qzv - qiime-файл по последовательности фичей. открывается перестаскиванием на https://view.qiime2.org/

feature_frequency_R45_L01_B121.qzv - qiime-файл по частоте фичей. открывается перестаскиванием на https://view.qiime2.org/

feature_sequense_R45_L01_B121.fasta - обработка qiime, стандартный файл с последовательностями фичей

feature-frequency_R45_L01_B121.csv - обработка qiime, стандартный файл с частотами фичей

feature_info_R45_L01_B121.csv - сводная таблица с итогами обработки фичей в qiime

RDP_features_R45_L01_B121.tsv - сводная таблица с итогами обработки фичей в PDP

blast_features_R45_L01_B121.tsv - сводная таблица с итогами обработки фичей в blast. Содержимое колонок ниже в этом файле.

taxonomy_result_table_R45_L01_B121.xls - итоговая таблица, объединяющая результаты из qiime, blast и RDP. Общий вид содержимого таблицы и пример для одной фичи приведен в файлах "example_output_taxonomy_table.png" и "example_output_for_one_feature.png"


# Запуск скрипта по созданию таблицы из 3 файлов (qiime2, blast и RDP)
python ~/Desktop/16s/scripts/make_whole_pipe_parallel/taxonomy_build_whole_table.py feature_info_R45_L01_B61.csv blast_features_R45_L01_B61.tsv RDP_features_R45_L01_B61.tsv taxonomy_result_table_R45_L01_B61

опции команды

qiime_result = sys.argv[1] # файл с результатами qiime-анализа

blast_result = sys.argv[2] # файл с результатами blastn-анализа

RDP_result = sys.argv[3] # файл с результатами RDP-анализа

output_file = sys.argv[4] # название файла с результатом (расширение писать не надо)

# EXAMPLE FOR RDP
rdp_classifier -o RDP_features_62 -q feature_sequense_62.fasta 

# EXAMPLE FOR BLAST
blastn -task megablast -db rRNA_typestrains/16S_ribosomal_RNA -query feature_sequense_62.fasta -out blast_features_62.csv -outfmt "6 qaccver sscinames sblastnames ppos evalue bitscore score staxid" -max_target_seqs 4 -remote

содержимое колонок:

qaccver (название фичи)

sscinames (название хита по бласту)

sblastnames (тоже название по бласту)

ppos (процент совпадения)

evalue

bitscore

score

staxid (какой-то уникальный номер хита)




